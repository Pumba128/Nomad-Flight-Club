import requests
from datetime import date, timedelta
from secrets import API_KEY, END_SEARCH, END_LOCATIONS


class FlightClass:

    def __init__(self, new_flight):
        self.headers = {
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json',
            'apikey': API_KEY
        }
        self.id = new_flight['id']
        self.fly_from = new_flight['fly_from']
        self.fly_to = new_flight['fly_to']
        self.price = new_flight['price']
        self.min_nights = new_flight['min_nights']
        self.iata_city_from = self.get_city_code(self.fly_from)
        self.iata_city_to = self.get_city_code(self.fly_to)

        self.date_from = date.today() + timedelta(days=1)
        self.date_to = self.date_from + timedelta(days=180)

        self.params = {
            'fly_from': f'city:{self.iata_city_from}',
            'fly_to': f'city:{self.iata_city_to}',
            'date_from': self.date_from.strftime("%d/%m/%Y"),
            'date_to': self.date_to.strftime("%d/%m/%Y"),
            'nights_in_dst_from': self.min_nights,
            'nights_in_dst_to': int(self.min_nights) + 7,
            'limit': 1,
            'max_stopovers': 6,
            'stopover_from': '2:00',
            'stopover_to': '12:00',
        }
        self.flight_data = self.get_flight_data()
        try:
            self.new_price = self.flight_data['price']
        except TypeError:
            self.new_price = 99999

    def get_flight_data(self):
        print(self.iata_city_from)
        response = requests.get(url=END_SEARCH, headers=self.headers, params=self.params)
        try:
            data = response.json()['data'][0]
        except IndexError:
            print(f"No flights found for {self.fly_to}.")
            return None

        formatted_flight_data = {
            'id': self.id,
            'price': data['price'],
            'airlines': ' '.join(data['airlines']),
            'from_date': data['route'][0]['local_departure'].split("T")[0],
            'to_date': data['route'][-1]['local_arrival'].split("T")[0],
            'nights': data['nightsInDest'],
            'iata_city_from': self.iata_city_from,
            'iata_port_from': data['flyFrom'],
            'iata_city_to': self.iata_city_to,
            'iata_port_to': data['flyTo'],
            'iata_stopovers': "NULL",
        }
        return formatted_flight_data

    def get_city_code(self, city):
        params = {
            'term': city,
            'location_types': 'city',
            'limit': 1,
        }
        response = requests.get(url=END_LOCATIONS, headers=self.headers, params=params)
        city_code = response.json()["locations"][0]["code"]
        return city_code
