import os
import sys
import utils.key_gen as keygen

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.opendata as opendata


class Event:

    def __init__(self, e_id=None, name=None, description=None, address=None, schedule=None, start_date=None,
                 end_date=None, url=None, email=None, category=None, specialty=None, organizer=None):
        self.e_id = e_id
        self.name = name
        self.description = description
        self.address = address
        self.schedule = schedule
        self.start_date = start_date
        self.end_date = end_date
        self.url = url
        self.email = email
        self.category = category
        self.specialty = specialty
        self.organizer = organizer

    @staticmethod
    def get_all():
        result = []
        events = opendata.parse_csv_data_events()
        for event in events.values():
            result.append(Event(e_id=event.get('ID_ACTIVIDAD'), name=event.get('NOMBRE'),
                                description=event.get('DESCRIPCION'), address=event.get('OTROS_LUGARES'),
                                schedule=event.get('HORARIO'), start_date=event.get('F_INICIO'), end_date=event.get('F_FIN'),
                                url=event.get('DIRECCION_WEB'), email=event.get('E_MAIL'), category=event.get('CATEGORIA'),
                                specialty=event.get('ESPECIALIDAD'), organizer=event.get('ORGANIZA')))
        return result

    @staticmethod
    def get_by_id(e_id):
        # id must be a string, not a number
        events = opendata.parse_csv_data_events()
        event = events.get(e_id)
        print(event)
        return Event(e_id=event.get('ID_ACTIVIDAD'), name=event.get('NOMBRE'),
                                description=event.get('DESCRIPCION'), address=event.get('OTROS_LUGARES'),
                                schedule=event.get('HORARIO'), start_date=event.get('F_INICIO'), end_date=event.get('F_FIN'),
                                url=event.get('DIRECCION_WEB'), email=event.get('E_MAIL'), category=event.get('CATEGORIA'),
                                specialty=event.get('ESPECIALIDAD'), organizer=event.get('ORGANIZA'))

    @staticmethod
    def get_event(entry, value):
        # id and entries must be string, not number or others
        events = opendata.parse_csv_data_events().values()
        for event in events:
            if event.get(entry) == value:
                return Event(e_id=event.get('ID_ACTIVIDAD'), name=event.get('NOMBRE'),
                                description=event.get('DESCRIPCION'), address=event.get('OTROS_LUGARES'),
                                schedule=event.get('HORARIO'), start_date=event.get('F_INICIO'), end_date=event.get('F_FIN'),
                                url=event.get('DIRECCION_WEB'), email=event.get('E_MAIL'), category=event.get('CATEGORIA'),
                                specialty=event.get('ESPECIALIDAD'), organizer=event.get('ORGANIZA'))
            else:
                continue


if __name__ == '__main__':
    # print(opendata.parse_csv_data_events())
    # print(Event().get_all())
    # print(Event().get_by_id('100195'))
    print(Event().get_event('ID_ACTIVIDAD', '100195'))
