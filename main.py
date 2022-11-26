from flight_search import FlightClass
from notifications import EmailBody
from database_operations import get_destination_data, update_db_flights
from database_operations import get_user_data

flights = [FlightClass(destination) for destination in get_destination_data()]

for flight in flights:
    if flight.new_price < flight.price:
        update_db_flights(flight.get_flight_data())

        for item in get_user_data().items():
            emailBody = EmailBody(item[0], item[1])
            emailBody.send_email(flight.flight_data)
