from csv import DictReader

elections_fname = "../data/election_cycle.csv"

def get_elections():
    return [e for e in elections_generator(elections_fname)]

def elections_generator(fname):
    with open(fname, 'r') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            yield {
                'president': row['president'],
                'year': int(row['year']),
                'lame_duck': int(row['lame_duck']) == 1,
                'up_for_reelection': int(row['up_for_reelection']) == 1,
                'midterm_election_year': int(row['midterm_election_year']) == 1,
                'election_year': int(row['election_year']) == 1
            }