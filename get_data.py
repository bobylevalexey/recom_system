import pickle

__author__ = 'alexey'


def get_2gis_places_links():
    with open('backup/places_links.pickle') as f:
        return pickle.load(f)

if __name__ == "__main__":
    print get_2gis_places_links().__len__()
