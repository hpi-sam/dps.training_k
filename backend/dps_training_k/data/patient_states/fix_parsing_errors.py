import csv

for i in range(1001, 1042):
    filename = str(i) + "_tables.csv"
    data = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row = [field.replace("\r\n", " ") for field in row]
            row = [field.replace("Bluttstillung", "Blutstillung") for field in row]
            data.append(row)
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    filename = str(i) + "_transitions.csv"
    data = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        print(f"+++ {filename} +++")
        reader = csv.reader(csvfile)
        end_state_table_ids = set()
        other_state_table_ids = set()
        for row in reader:
            if row[0] == "502":
                row[7] = "kalt|grau/marmoriert"  # fix typo
                # overwrite useless stuff the parser found
                row[22] = ""
                row[21] = ""
            if row[0] == "":
                row[0] = "500"  # add state number
                row[23] = "0|sichere Todeszeichen"  # add missing description
                # overwrite useless stuff the parser found
                row[22] = ""
                row[21] = ""
            row = [field.replace("feucht|blass|", "feucht|blass") for field in row]
            # find dead tables (result of parsing errors) -> should no longer return anything
            if row[0] != "Status" and int(row[0]) % 10 == 0:
                if row[24] != "":
                    end_state_table_ids.add(row[24])
            else:
                if row[24] != "":
                    other_state_table_ids.add(row[24])
                else:
                    if row[0] != "502":
                        print(f"no table given for state {row[0]}")
            data.append(row)
        for table in end_state_table_ids:
            if table not in other_state_table_ids:
                print(f"table {table} not used")
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if data[0][0] != "Status":
            writer.writerow(
                [
                    "Status",
                    "Airway",
                    "Breathing",
                    "Circulation",
                    "Bewusstsein",
                    "Pupillen",
                    "Psyche",
                    "Haut",
                    "BGA-Oxy",
                    "BGA_SBH",
                    "Hb",
                    "BZ",
                    "Gerinnung",
                    "Leber",
                    "Niere",
                    "Infarkt",
                    "Lactat",
                    "Rö-Extremitäten",
                    "Rö-Thorax",
                    "Trauma-CT",
                    "Ultraschall",
                    "EKG",
                    "ZVD",
                    "Beschreibung",
                    "Übergangstabelle",
                ]
            )
        writer.writerows(data)

# TODO: in 1005 ask Frank where state 551 should lead. State 2 doesn't exist, assumption is 502
# TODO: ask what the difference between "O2" and "O2 Inhalation" is (referring to patient 1013)
# TODO: we need "O2 Inhalation" and "CPAP" to prohibit each other (if not, patient 1013 can break)
# TODO: ask which actions correspond to CPAP and O2 Inhalation
