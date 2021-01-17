import requests, csv

museumJSON = 'https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cultura_ocio_museos-4326.geojson'
artGalleryJSON = 'https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cultura_ocio_galeriasArte-4326.geojson'
dogParkJSON = 'https://datosabiertos.malaga.eu/recursos/ambiente/parquesCaninos/da_parquesCaninos-4326.geojson'
monumentJSON = 'https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cultura_ocio_monumentos-4326.geojson'
trainingParkJSON = 'https://datosabiertos.malaga.eu/recursos/deportes/equipamientos/da_deportesZonasMusculacion-4326.geojson'
libraryJSON = 'https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cultura_ocio_bibliotecas-4326.geojson'
cinemaJSON = 'https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cultura_ocio_cines-4326.geojson'
theaterJSON = 'https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/equipamientos/da_cultura_ocio_teatros-4326.geojson'

events2020CSV = 'https://datosabiertos.malaga.eu/datastore/dump/7f96bcbb-020b-449d-9277-1d86bd11b827'


def download_open_data_json(url):
    response = requests.get(url)

    if response.status_code >= 400:
        raise RuntimeError(f'Error with request. Code: {response.status_code}')

    return response.json()


def download_open_data_csv(url):
    response = requests.get(url)

    if response.status_code >= 400:
        raise RuntimeError(f'Error with request. Code: {response.status_code}')
    csv_file = open('events2020.csv', 'wb')
    csv_file.write(response.content)


def parse_json_data(leisure_type: str):
    switcher = {
        'MUSEUM': museumJSON,
        'ARTGALLERY': artGalleryJSON,
        'DOGPARK': dogParkJSON,
        'MONUMENT': monumentJSON,
        'TRAINING': trainingParkJSON,
        'LIBRARY': libraryJSON,
        'CINEMA': cinemaJSON,
        'THEATER': theaterJSON
    }
    json_url = switcher.get(leisure_type, lambda: 'Invalid type')

    data = download_open_data_json(json_url)
    features = data['features']
    result = {}

    for feature in features:
        longitude = feature['geometry']['coordinates'][0]
        latitude = feature['geometry']['coordinates'][1]
        id_leisure = feature['properties']['ID']
        name = feature['properties']['NOMBRE']
        description = feature['properties']['DESCRIPCION']
        address = feature['properties']['DIRECCION']
        url = feature['properties']['URL']
        email = feature['properties']['EMAIL']
        schedule = feature['properties']['HORARIOS']
        data = {'id': id_leisure, 'name': name, 'description': description, 'type': leisure_type.lower(), 'address': address, 'url': url, 'email': email, 'schedule': schedule, 'coordinates': [latitude, longitude]}
        result[id_leisure] = data

    return result


def parse_csv_data_events():
    download_open_data_csv(events2020CSV)
    result = {}
    # it needs an existing 'events2020.csv' file before downloading and opening it...
    with open('events2020.csv', mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        keys_list = list(next(csv_reader))
        for row in csv_reader:
            result[row[1]] = {
                keys_list[1]: row[1],
                keys_list[2]: row[2],
                keys_list[3]: row[3],
                keys_list[4]: row[4],
                keys_list[5]: row[5],
                keys_list[6]: row[6],
                keys_list[7]: row[7],
                keys_list[8]: row[8],
                keys_list[9]: row[9],
                keys_list[10]: row[10],
                keys_list[11]: row[11],
                keys_list[12]: row[12],
                keys_list[13]: row[13],
                keys_list[14]: row[14],
                keys_list[15]: row[15],
                keys_list[16]: row[16],
                keys_list[17]: row[17],
                keys_list[18]: row[18],
                keys_list[19]: row[19]
            }
    return result


if __name__ == '__main__':
    print(parse_json_data('DOGPARK'))
    print(parse_csv_data_events())
