import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.db as db


class User:
    entry = 'users/'

    def __init__(self, email=None, uid=None, display_name=None, profile_picture=None):
        self.email = email
        self.uid = uid
        self.display_name = display_name
        self.profile_picture = profile_picture

    def encode(self):
        return self.__dict__

    @staticmethod
    def get_by_uid(uid):
        user = db.get_dict(User.entry + '/' + uid)
        if user is not None:
            return User(email=user['email'], uid=user['uid'], display_name=user['displayName'], profile_picture=user['profilePicture'])
        else:
            return None

    @staticmethod
    def create_user(uid, email, display_name, profile_picture):
        exists = bool(db.get_dict(User.entry, order='uid', value=uid))

        if not exists:
            data = {
                'uid': uid,
                'email': email,
                'displayName': display_name,
                'profilePicture': profile_picture
            }
            db.create(User.entry + '/' + uid, data)
            return User(email=email, uid=uid, display_name=display_name, profile_picture=profile_picture)
        else:
            return None

    @staticmethod
    def change_display_name(key, data):
        # data must be a dictionary
        if isinstance(data, dict):
            db.update(User.entry, key, data)
            return User.get_by_uid(key)
        else:
            return None


if __name__ == '__main__':
    print('prueba')
