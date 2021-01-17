import os
import sys
import utils.key_gen as keygen

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.opendata as opendata


class Leisure:

    def __init__(self, leisure_type, l_id=None, name=None, description=None, address=None, url=None,
                 email=None, schedule=None, coordinates=None,):
        self.leisure_type = leisure_type
        self.l_id = l_id
        self.name = name
        self.description = description
        self.address = address
        self.url = url
        self.email = email
        self.schedule = schedule
        self.coordinates = coordinates

    def get_all(self):
        result = []
        leisures = opendata.parse_json_data(self.leisure_type)
        for leisure in leisures.values():
            result.append(Leisure(leisure_type=self.leisure_type, l_id=leisure.get('id'), name=leisure.get('name'),
                                  description=leisure.get('description'), address=leisure.get('address'),
                                  url=leisure.get('url'), email=leisure.get('email'), schedule=leisure.get('schedule'),
                                  coordinates=[leisure.get('coordinates')[0], leisure.get('coordinates')[1]]))
        return result

    def get_by_id(self, l_id):
        # id must be a number, not a string
        leisures = opendata.parse_json_data(self.leisure_type)
        leisure = leisures.get(l_id)
        return Leisure(leisure_type=self.leisure_type, l_id=leisure.get('id'), name=leisure.get('name'),
                                  description=leisure.get('description'), address=leisure.get('address'),
                                  url=leisure.get('url'), email=leisure.get('email'), schedule=leisure.get('schedule'),
                                  coordinates=[leisure.get('coordinates')[0], leisure.get('coordinates')[1]])

    def get_leisure(self, entry, value):
        # entries and values must be a string, except id value. It must be a number
        leisures = opendata.parse_json_data(self.leisure_type).values()
        for leisure in leisures:
            if leisure.get(entry) == value:
                return Leisure(leisure_type=self.leisure_type, l_id=leisure.get('id'), name=leisure.get('name'),
                                  description=leisure.get('description'), address=leisure.get('address'),
                                  url=leisure.get('url'), email=leisure.get('email'), schedule=leisure.get('schedule'),
                                  coordinates=[leisure.get('coordinates')[0], leisure.get('coordinates')[1]])
            else:
                continue


if __name__ == '__main__':
    print(opendata.parse_json_data('MUSEUM'))
    # print(Leisure('MUSEUM').get_all())
    # print(Leisure('MUSEUM').get_by_id(841))
    # print(Leisure('MUSEUM').get_leisure('id', 841))
