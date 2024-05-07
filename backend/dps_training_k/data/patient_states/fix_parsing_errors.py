import csv
for i in range(1001, 1041):
    filename = str(i) + "_tables.csv"
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader: 
            row = [field.replace('\r\n', ' ') for field in row]
            row = [field.replace('Bluttstillung', 'Blutstillung') for field in row]

    filename = str(i) + "_transitions.csv"
    with open(filename, newline='') as csvfile:
        print(f"+++ {filename} +++")
        reader = csv.reader(csvfile)
        end_state_table_ids = set()
        other_state_table_ids = set()
        for row in reader:
            if row[0] == "":
                row[0] = "500"
            row = [field.replace('|', '\n') for field in row]
            if int(row[0]) % 10 == 0:
                if row[24] != '':
                    end_state_table_ids.add(row[24])
            else:
                if row[24] != '':
                    other_state_table_ids.add(row[24])
                else:
                    if row[0] != "502":
                        print(f"no table given for state {row[0]}")
        for table in end_state_table_ids:
            if table not in other_state_table_ids:
                print(f"table {table} not used")

#TODO: 1005 is broken (missing middle part aka 300-636), fixed tables already
#TODO: in 1005 ask Frank where state 551 should lead. State 2 doesn't exist, assumption is 502
#TODO: ask what the difference between "O2" and "O2 Inhalation" is (referring to patient 1013)
#TODO: we need "O2 Inhalation" and "CPAP" to prohibit each other (if not, patient 1013 can break)
#TODO: ask which actions correspond to CPAP and O2 Inhalation
#TODO: add description to state 500, clean up trash in 500 and 502
#TODO: add headers to transitions csvs