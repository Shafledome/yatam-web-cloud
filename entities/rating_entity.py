import os
import sys
import utils.key_gen as keygen

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.db as db


class Rating:
    entry = 'ratings/'  # entry of the database

    def __init__(self, key=None, grade=None, description=None, n_likes=None, leisure=None, user=None):
        self.key = key
        self.grade = grade
        self.description = description
        self.n_likes = n_likes
        self.leisure = leisure
        self.user = user

    @staticmethod
    def get_all():
        result = []
        ratings = db.get_dict(Rating.entry)
        for key, value in ratings.items():
            result.append(Rating(key=value.get('key'), grade=value.get('grade'), description=value.get('description'), n_likes=value.get('nlikes'),
                                 leisure=value.get('url'), user=value.get('user')))
        return result

    @staticmethod
    def get_by_key(key):
        rating = db.get_dict(Rating.entry + '/' + key)
        return Rating(key=rating['key'], grade=rating['grade'], description=rating['description'], n_likes=rating['nlikes'], leisure=rating['leisure'], user=rating['user'])

    @staticmethod
    def get_rating(order=None, value=None):
        # ordered dictionary to list and getting first element
        rating = list(db.get_dict(Rating.entry, order=order, value=value).values())[0]
        return Rating(key=rating['key'], description=rating['description'], n_likes=rating['nlikes'], leisure=rating['leisure'], user=rating['user'])

    @staticmethod
    def get_ratings_by_leisure(order=None, value=None):
        # ordered dictionary to list and getting first element
        rating = list(db.get_dict(Rating.entry, order=order, value=value).values())
        return rating
        
    @staticmethod
    def create_rating(grade, description, leisure, user):
        new_key = keygen.gen_random_key()
        data = {
            'key': new_key,
            'grade': grade,
            'description': str(description),
            'nlikes': 0,
            'leisure': leisure,
            'user': user
        }
        db.create(Rating.entry + '/' + new_key, data)
        return Rating(key=new_key, grade=grade, description=description, n_likes=0, leisure=leisure, user=user)

    @staticmethod
    def update_rating(key, data):
        # data must be a dictionary
        if isinstance(data, dict):
            db.update(Rating.entry, key, data)
            return Rating.get_by_key(key)
            # return Rating(key=key, grade=data['grade'], description=data['description'], n_likes=data['nlikes'], leisure=data['leisure'], user=data['user'])
        else:
            return None

    @staticmethod
    def delete_rating(key):
        db.delete(Rating.entry, key)
        return 'Data deleted.'


if __name__ == '__main__':
    print('prueba')
