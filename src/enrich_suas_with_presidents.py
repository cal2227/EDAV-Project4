import utils
import presidents_csv

def gen_pres_by_name(presidents):
    pres_by_name = { p['president']: p for p in presidents }
    for p in presidents:
        p.pop('president')

    return pres_by_name

def main(suas):
    presidents = presidents_csv.get_presidents()
    pres_by_name = gen_pres_by_name(presidents)
    president_per_sua = [pres_by_name[pres] for pres in utils.get_presidents(suas)]

    utils.enrich_collection(suas, president_per_sua)

if __name__ == '__main__':
    suas = utils.load_json_as_dict(utils.reading_levels_fname)
    main(suas)
    utils.save_as_json(utils.with_presidents_fname, suas)
