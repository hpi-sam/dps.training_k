import csv

subconditions = set()

for i in range(1001, 1042):
    filename = str(i) + "_tables.csv"
    data = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        read_next_line = False
        for row in reader:
            if read_next_line and row[0] != "leer":
                for field in row:
                    subconditions.add(field)
            read_next_line = False
            if row[0] == "Tabelle 0:" or row[0] == "Tabelle 1:":
                read_next_line = True
           

for element in subconditions:
    print(element)