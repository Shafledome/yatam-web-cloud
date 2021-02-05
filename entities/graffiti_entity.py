import os
import sys
import utils.key_gen as keygen
from entities.user_entity import User

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.db as db


class Graffiti:
    entry = 'graffities/'  # entry of the database

    def __init__(self, key=None, description=None, n_likes=None, url=None, user=None):
        self.key = key
        self.description = description
        self.n_likes = n_likes
        self.url = url
        self.user = user

    def encode(self):
        return self.__dict__

    @staticmethod
    def get_all():
        result = []
        graffities = db.get_dict(Graffiti.entry)
        for key, value in graffities.items():
            result.append(Graffiti(key=value.get('key'), description=value.get('description'), n_likes=value.get('nlikes'),
                                   url=value.get('url'), user=User.get_by_uid(value.get('user'))))
        return result

    @staticmethod
    def get_by_key(key):
        graffiti = db.get_dict(Graffiti.entry + '/' + key)
        return Graffiti(key=graffiti['key'], description=graffiti['description'], n_likes=graffiti['nlikes'],
                        url=graffiti['url'], user=User.get_by_uid(graffiti['user']))

    @staticmethod
    def get_graffiti(order=None, value=None):
        # ordered dictionary to list and getting first element
        graffiti = list(db.get_dict(Graffiti.entry, order=order, value=value).values())[0]
        return Graffiti(key=graffiti['key'], description=graffiti['description'], n_likes=graffiti['nlikes'],
                        url=graffiti['url'], user=User.get_by_uid(graffiti['user']))

    @staticmethod
    def create_graffiti(description, url, user):
        new_key = keygen.gen_random_key()
        data = {
            'key': new_key,
            'description': str(description),
            'nlikes': 0,
            'url': url,
            'user': user
        }
        db.create(Graffiti.entry + '/' + new_key, data)
        return Graffiti(key=new_key, description=description, n_likes=0, url=url, user=User.get_by_uid(user))

    @staticmethod
    def update_graffiti(key, data):
        # data must be a dictionary
        if isinstance(data, dict):
            db.update(Graffiti.entry, key, data)
            return Graffiti(key=key, description=data['description'], n_likes=data['nlikes'],
                            url=data['url'], user=User.get_by_uid(data['user']))
        else:
            return None

    @staticmethod
    def delete_graffiti(key):
        db.delete(Graffiti.entry, key)
        return 'Data deleted.'


if __name__ == '__main__':
    print('prueba')
