import utils

def main(suas):
    reading_levels = utils.get_reading_levels(suas)
    utils.enrich_collection(suas, reading_levels)

if __name__ == '__main__':
    suas = utils.get_suas_1970()
    main(suas)
    utils.save_as_json(utils.reading_levels_fname, suas)