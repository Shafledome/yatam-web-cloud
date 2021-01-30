import os
import sys
import utils.key_gen as keygen
import utils.db as db

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class UserLeisure:
    entry = 'usersLeisures/'  # entry of the database

    def __init__(self, key=None, name=None, description=None, address=None, url_photo=None,
                 coordinates=None, schedule=None, user=None):
        self.key = key
        self.name = name
        self.description = description
        self.address = address
        self.url_photo = url_photo
        self.schedule = schedule
        self.coordinates = coordinates
        self.user = user

    def encode(self):
        return self.__dict__

    @staticmethod
    def get_all():
        result = []
        leisures = db.get_dict(UserLeisure.entry)
        for key, value in leisures.items():
            result.append(UserLeisure(key=value.get('key'), description=value.get('description'),
                                      name=value.get('name'), url_photo=value.get('url_photo'),
                                      schedule=value.get('schedule'), user=value.get('user'),
                                      coordinates=value.get('coordinates'), address=value.get('address')))
        return result

    @staticmethod
    def get_by_key(key):
        leisure = db.get_dict(UserLeisure.entry + '/' + key)
        return UserLeisure(key=leisure['key'], description=leisure['description'], name=leisure['name'],
                           address=leisure['address'], url_photo=leisure['url_photo'], user=leisure['user'],
                           schedule=leisure['schedule'], coordinates=leisure['coordinates'])

    @staticmethod
    def get_user_leisure(order=None, value=None):
        # ordered dictionary to list and getting first element
        graffiti = list(db.get_dict(UserLeisure.entry, order=order, value=value).values())[0]
        return UserLeisure(key=graffiti['key'], description=graffiti['description'], name=graffiti['name'],
                           address=graffiti['address'], url_photo=graffiti['url_photo'], user=graffiti['user'],
                           schedule=graffiti['schedule'], coordinates=graffiti['coordinates'])

    @staticmethod
    def create_user_leisure(name, description, address, url_photo, schedule, coordinates, user):
        new_key = keygen.gen_random_key()
        data = {
            'key': new_key,
            'name': name,
            'description': str(description),
            'address': address,
            'url_photo': url_photo,
            'schedule': schedule,
            'coordinates': coordinates,
            'user': user
        }
        db.create(UserLeisure.entry + '/' + new_key, data)
        return UserLeisure(key=new_key, description=description, name=name, address=address, url_photo=url_photo,
                           schedule=schedule, coordinates=coordinates, user=user)

    @staticmethod
    def update_user_leisure(key, data):
        # data must be a dictionary
        if isinstance(data, dict):
            db.update(UserLeisure.entry, key, data)
            return UserLeisure(key=key, description=data['description'], name=data['name'], address=data['address'],
                               url_photo=data['url_photo'], schedule=data['schedule'], coordinates=data['coordinates'],
                               user=data['user'])
        else:
            return None

    @staticmethod
    def delete_rating(key):
        db.delete(UserLeisure.entry, key)
        return 'Data deleted.'


if __name__ == '__main__':
    print('prueba')
