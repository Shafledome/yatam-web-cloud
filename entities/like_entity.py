import os
import sys

from entities.graffiti_entity import Graffiti
from entities.rating_entity import Rating
from entities.user_entity import User
from entities.user_leisure_entity import UserLeisure

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.db as db


class Like:
    entry = 'likes/'

    @staticmethod
    def check_like_user(key, uid):
        like = db.get_dict(Like.entry + '/' + str(key) + '/' + uid)
        if like is None:
            return None
        else:
            return like['uid'] == uid  # never returns false

    @staticmethod
    def create_like(key, uid):
        data = {
            'uid': uid
        }
        try:
            db.create(Like.entry + '/' + str(key) + '/' + uid, data)
            return True
        except NameError:
            print(NameError)

    @staticmethod
    def delete_like(key, uid):
        db.delete(Like.entry + '/' + key, uid)

    @staticmethod
    def like_increase_decrease(like_type, key, uid):
        if Like.check_like_user(key, uid):
            if like_type == 'RATING':
                rating = Rating.get_by_key(key)
                data = {
                    'nlikes': rating.n_likes - 1
                }
                Rating.update_rating(key, data)
            elif like_type == 'GRAFFITI':
                graffiti = Graffiti.get_by_key(key)
                data = {
                    'nlikes': graffiti.n_likes - 1
                }
                Graffiti.update_graffiti(key, data)
            elif like_type == 'USER':
                leisure = UserLeisure.get_by_key(key)
                data = {
                    'nlikes': leisure.n_likes - 1
                }
                UserLeisure.update_user_leisure(key, data)
            Like.delete_like(key, uid)
        else:
            Like.create_like(key, uid)
            if like_type == 'RATING':
                rating = Rating.get_by_key(key)
                data = {
                    'nlikes': rating.n_likes + 1
                }
                Rating.update_rating(key, data)
            elif like_type == 'GRAFFITI':
                graffiti = Graffiti.get_by_key(key)
                data = {
                    'nlikes': graffiti.n_likes + 1
                }
                Graffiti.update_graffiti(key, data)
            elif like_type == 'USER':
                leisure = UserLeisure.get_by_key(key)
                data = {
                    'nlikes': leisure.n_likes + 1
                }
                UserLeisure.update_user_leisure(key, data)


if __name__ == '__main__':
    # print(Like.check_like('ratingkeyejemplo'))
    # print(Like.check_like_user('ratingkeyejemplo', 'useridejemplo2'))
    print(Like.create_like('nuevakeyejemplo', 'nuevouidejemplo2'))
    # Like.delete_like('nuevakeyejemplo', 'nuevouidejemplo')
