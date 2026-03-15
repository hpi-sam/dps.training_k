import time
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.utils import timezone

from configuration.celery import app as celery_app
from game.consumers import TrainerConsumer
from game.models import Exercise, PatientInstance, Area, User, ScheduledEvent
from template.models import PatientInformation, PatientState


class Command(BaseCommand):
    help = "Creates 100 patients and measures how quickly Celery processes the initial phase changes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--patients",
            type=int,
            default=100,
            help="Number of patients to create (default: 100)",
        )
        parser.add_argument(
            "--poll-interval",
            type=float,
            default=0.05,
            help="Seconds between polling event count (default: 0.05)",
        )
        parser.add_argument(
            "--time-buffer",
            type=float,
            default=0.5,
            help="Seconds between starting the exercise and the phase changes becoming due (default: 0.5)",
        )

    def handle(self, *args, **options):
        num_patients = options["patients"]
        poll_interval = options["poll_interval"]
        time_buffer = options["time_buffer"]

        inspect = celery_app.control.inspect(timeout=2)
        stats = inspect.stats() or {}
        worker_count = len(stats)
        concurrency = sum(
            s.get("pool", {}).get("max-concurrency", 0) for s in stats.values()
        )

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"Performance Test: {num_patients} patients")
        self.stdout.write(
            f"  Celery workers: {worker_count} node(s), {concurrency} total processes"
        )
        self.stdout.write(f"{'='*60}\n")

        # --- Setup ---
        self.stdout.write("Setting up exercise...")
        setup_start = time.perf_counter()

        user, _ = User.objects.get_or_create(
            username="perftest",
            user_type=User.UserType.TRAINER,
        )
        if not user.has_usable_password():
            user.set_password("perftest")
            user.save()

        exercise = Exercise.createExercise(user)
        area = Area.create_area(name="Testbereich", exercise=exercise, isPaused=False)

        patient_infos = list(PatientInformation.objects.all())
        if not patient_infos:
            self.stderr.write(
                self.style.ERROR(
                    "No PatientInformation found. Run import_patient_information first."
                )
            )
            return

        for i in range(num_patients):
            info = patient_infos[i % len(patient_infos)]
            patient_state = PatientState.objects.get(
                code=info.code,
                state_id=info.start_status,
            )
            PatientInstance.objects.create(
                name=f"Testpatient {i+1}",
                static_information=info,
                exercise=exercise,
                area=area,
                patient_state=patient_state,
                frontend_id=settings.ID_GENERATOR.get_patient_frontend_id(),
            )

        setup_duration = time.perf_counter() - setup_start
        self.stdout.write(
            f"Setup complete: {num_patients} patients in {setup_duration:.2f}s\n"
        )

        # --- Start exercise realistically (via TrainerConsumer, same as the UI) ---
        # ToDo: Wrapped in atomic + retry to handle pre-existing LogEntry.local_id race condition
        self.stdout.write(
            "Starting exercise (scheduling state changes for all patients)..."
        )
        schedule_start = time.perf_counter()
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                with transaction.atomic():
                    TrainerConsumer.handle_start_exercise(None, exercise)
                break
            except IntegrityError:
                if attempt == max_attempts - 1:
                    raise
                self.stdout.write(
                    self.style.WARNING(
                        f"  LogEntry race condition hit, retrying ({attempt + 1}/{max_attempts})..."
                    )
                )
        schedule_duration = time.perf_counter() - schedule_start

        total_events = ScheduledEvent.objects.filter(exercise=exercise).count()
        state_change_filter = dict(
            exercise=exercise, method_name="execute_state_change"
        )
        initial_events = ScheduledEvent.objects.filter(**state_change_filter).count()
        self.stdout.write(
            f"{total_events} events scheduled ({initial_events} state changes, "
            f"{total_events - initial_events} pretreatment effects) in {schedule_duration:.2f}s"
        )

        # --- Make only state-change events immediately due ---
        ScheduledEvent.objects.filter(**state_change_filter).update(
            end_date=timezone.now() - timedelta(seconds=time_buffer)
        )
        self.stdout.write(
            f"{initial_events} state-change events shifted to be immediately due with a buffer of {time_buffer}.\n"
        )

        # --- Wait for Celery to process all initial events ---
        self.stdout.write("Waiting for Celery workers to process events...")
        self.stdout.write(f"{'─'*60}")

        process_start = time.perf_counter()
        stall_start = None
        last_total = initial_events
        first_processed_time = None

        while True:
            time.sleep(poll_interval)
            # Only count events that were part of the initial batch (enqueued or not yet claimed).
            # New events from execute_state_change will have end_date far in the future,
            # so they won't be enqueued and won't interfere.
            enqueued = ScheduledEvent.objects.filter(
                **state_change_filter, enqueued=True
            ).count()
            due_not_enqueued = ScheduledEvent.objects.filter(
                **state_change_filter, enqueued=False, end_date__lte=timezone.now()
            ).count()
            in_flight = enqueued + due_not_enqueued
            processed = initial_events - in_flight
            elapsed = time.perf_counter() - process_start

            self.stdout.write(
                f"  [{elapsed:6.2f}s] "
                f"processed: {processed}/{initial_events}  "
                f"enqueued: {enqueued}  "
                f"due (unclaimed): {due_not_enqueued}"
            )

            if first_processed_time is None and processed > 0:
                first_processed_time = time.perf_counter()

            if processed >= initial_events:
                break

            # Safety: abort if no progress for 30s
            if in_flight == last_total:
                if stall_start is None:
                    stall_start = time.perf_counter()
                elif time.perf_counter() - stall_start > 30:
                    self.stderr.write(
                        self.style.WARNING("\nNo progress for 30s. Aborting poll.")
                    )
                    break
            else:
                stall_start = None
                last_total = in_flight

            if elapsed > 300:
                self.stderr.write(
                    self.style.WARNING("\nTimeout after 5 minutes. Aborting.")
                )
                break

        process_duration = time.perf_counter() - process_start
        processing_only = (
            time.perf_counter() - first_processed_time if first_processed_time else 0
        )

        # --- Results ---
        self.stdout.write(f"{'─'*60}")
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"RESULTS")
        self.stdout.write(f"{'='*60}")
        self.stdout.write(f"  Patients:              {num_patients}")
        self.stdout.write(f"  Initial events:        {initial_events}")
        self.stdout.write(f"  Setup time:            {setup_duration:.2f}s")
        self.stdout.write(f"  Scheduling time:       {schedule_duration:.2f}s")
        self.stdout.write(f"  Total wall time:       {process_duration:.2f}s")
        self.stdout.write(f"  Processing time:       {processing_only:.2f}s")
        if initial_events > 0 and processing_only > 0:
            self.stdout.write(
                f"  Throughput:            {initial_events / processing_only:.1f} events/s"
            )
        self.stdout.write(f"{'='*60}\n")

        # --- Cleanup ---
        self.stdout.write("Cleaning up test exercise...")
        # Delete events first to avoid race with post_delete signal on Owner
        # (Celery workers may still be processing when we clean up)
        ScheduledEvent.objects.filter(exercise=exercise).delete()
        exercise.delete()
        self.stdout.write(self.style.SUCCESS("Done.\n"))
