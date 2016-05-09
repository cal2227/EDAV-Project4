from csv import DictReader

presidents_fname = "../data/presidents.csv"

def get_presidents():
    return [p for p in presidents_generator(presidents_fname)]

def presidents_generator(fname):
    with open(fname, 'r') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            yield row
