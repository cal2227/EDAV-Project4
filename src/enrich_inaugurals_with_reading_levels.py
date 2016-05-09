import utils

def main(inaugurals):
    reading_levels = utils.get_reading_levels(inaugurals)
    utils.enrich_collection(inaugurals, reading_levels)

if __name__ == '__main__':
    inaugurals = utils.get_inaugurals()
    main(inaugurals)
    utils.save_as_json(utils.inaugurals_reading_levels_fname, inaugurals)