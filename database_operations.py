import sqlalchemy as sa
import pandas as pd
from secrets import USERNAME, PASSWORD, SERVER, PORT, DATABASE

engine = sa.create_engine(f"mysql+mysqldb://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/"
                          f"{DATABASE}", echo=True)


# DB template for SQLAlchemy queries
users_table = sa.table(
    "userdata",
    sa.Column("name"),
    sa.Column("email"),
)

# SELECT email, name FROM users_table
select_name_email = sa.select(users_table.c.email, users_table.c.name)

user_data_dict = {}


def get_user_data():
    """ getting user email (key) and mail (value) and creating a dictionary of it. Do I really need it? xD """
    with engine.connect() as cnx:
        for row in cnx.execute(select_name_email):
            user_data_dict[row['email']] = row['name']
    return user_data_dict

# DB template for SQLAlchemy queries
flights_table = sa.table(
    "flights",
    sa.Column("id"),
    sa.Column("userdata_id"),
    sa.Column("fly_from"),
    sa.Column("fly_to"),
    sa.Column("price"),
    sa.Column("iata_city_from"),
    sa.Column("iata_port_from"),
    sa.Column("iata_city_to"),
    sa.Column("iata_port_to"),
    sa.Column("iata_stopovers"),
    sa.Column("from_date"),
    sa.Column("to_date"),
    sa.Column("min_nights"),
    sa.Column("nights"),
    sa.Column("airlines"),
)

# SELECT * FROM flights_table, makes pandas DF from SQL
select_all = flights_table.select()

with engine.begin() as connection:
    df1 = pd.read_sql(sql=select_all, con=connection)


# creates list of rows from flights_table as dict(col_name: value)
def get_destination_data():
    flights_db_data = []
    for row in df1.to_dict(orient='records'):
        flights_db_data.append(row)
    return flights_db_data


def update_db_flights(flight_data):
    update_flight_data_query = (sa.update(flights_table).where(flights_table.c.id == flight_data['id']).values(**flight_data))
    with engine.connect() as cnx:
        cnx.execute(update_flight_data_query)

