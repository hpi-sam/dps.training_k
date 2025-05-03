def seconds_to_partitioned_time_scales(seconds: int):
    fractioned_time = {}
    time_scales = {"days": 24 * 60 * 60, "hours": 60 * 60, "minutes": 60, "seconds": 1}
    for name, factor in time_scales.items():
        fractioned_time[name] = seconds // factor
        seconds -= fractioned_time[name] * factor
    return fractioned_time
