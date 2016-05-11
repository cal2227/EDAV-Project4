import utils
import elections_csv

def gen_elections_by_year(elections):
    elections_by_year = { e['year']: e for e in elections }
    for e in elections:
        e.pop('year')
        e.pop('president')

    return elections_by_year

def main(suas):
    elections = elections_csv.get_elections()
    elections_by_year = gen_elections_by_year(elections)
    year_per_sua = [elections_by_year[year] for year in utils.get_years(suas)]

    utils.enrich_collection(suas, year_per_sua)

if __name__ == '__main__':
    suas = utils.load_json_as_dict(utils.with_presidents_fname)
    main(suas)
    utils.save_as_json(utils.with_elections_fname, suas)