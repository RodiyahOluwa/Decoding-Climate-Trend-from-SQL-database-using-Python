# Author: <Rodiyah Oluwa>
# Student ID: <D3127027>
import sqlite3
from datetime import datetime, timedelta
def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        connection.row_factory = sqlite3.Row
        # Define the query
        query = "SELECT * from [countries]"
        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()
        # Execute the query via the cursor object.
        results = cursor.execute(query)
        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")
    except sqlite3.OperationalError as ex:
        print(ex)

def select_all_cities(connection):
    # TODO: Implement this function
    # Queries the database and selects all the cities
    # stored in the cities table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        connection.row_factory = sqlite3.Row
        # Define the query
        query = "SELECT * from [cities]"
        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()
        # Execute the query via the cursor object.
        results = cursor.execute(query)
        # Iterate over the results and display the results.
        for row in results:
            print(f"City Id: {row['id']} -- City Name: {row['name']} -- City Longitude: {row['longitude']}-- City Latitude: {row['latitude']} Country ID: {row['country_id']}")
    except sqlite3.OperationalError as ex:
        print(ex)

def average_annual_temperature(connection, city_id, year):
    try:
        connection.row_factory = sqlite3.Row
        # Define the query
        query = f"SELECT avg(mean_temp) from daily_weather_entries where date >= '{year}-01-01'  and date <= '{year}-12-31' and city_id = {city_id}"       
        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()
        # Execute the query via the cursor object.
        results = cursor.execute(query)
        # Iterate over the results and display the results.
        for row in results:
            print(f"Average annual temperature for city {city_id} in year {year} was {row[0]:.2f}")
    except sqlite3.OperationalError as ex:
        print(ex)

def average_seven_day_precipitation(connection, city_id, start_date):
    try:
        connection.row_factory = sqlite3.Row
        #define end date
        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=6)).strftime("%Y-%m-%d")
        # Define the query
        query = """
        SELECT AVG(precipitation) AS avg_precipitation, cities.name AS city_name
        FROM daily_weather_entries
        JOIN cities ON daily_weather_entries.city_id = cities.id
        WHERE date BETWEEN ? AND ? AND daily_weather_entries.city_id = ?
        GROUP BY cities.name
        """
        # Print the query parameters for debugging
        print(f"Query Parameters: start_date= {start_date}, end_date= {end_date}, city_id= {city_id}")
        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()
        # Execute the query via the cursor object.
        results = cursor.execute(query, (start_date, end_date, city_id))
         # Fetch one row from the results
        row = results.fetchone()
        if row and row['avg_precipitation'] is not None:
        # Iterate over the results and display the results.
             print(f"Average 7-day precipitation starting from {start_date} to {end_date} in {row['city_name']} is {row['avg_precipitation']:.2f}")
        else:
            print(f"No data found for the specified parameters.")    
    except sqlite3.OperationalError as ex:
        print(ex)

def average_mean_temp_by_city(connection, date_from, date_to):
    try:
        connection.row_factory = sqlite3.Row
        # Define the query with a JOIN to retrieve the city name
        query = """
        SELECT AVG(mean_temp) AS avg_temperature, cities.name AS city_name
        FROM daily_weather_entries
        JOIN cities ON daily_weather_entries.city_id = cities.id
        WHERE date BETWEEN ? AND ?
        GROUP BY cities.name
        """
        # Get a cursor object from the database connection
        cursor = connection.cursor()
        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query, (date_from, date_to))
        # Fetch one row from the results
        for row in results:
            if row and row['avg_temperature'] is not None:
                # Check if the value is not None before formatting
                print(f"Average mean temperature for {row['city_name']} from {date_from} to {date_to} is {row['avg_temperature']:.2f}")
            else:
                print(f"No data found for the specified parameters.")
    except sqlite3.OperationalError as ex:
        print(ex)

def average_annual_precipitation_by_country(connection, year):
    try:
        connection.row_factory = sqlite3.Row
        # Define the query with multiple JOINs to retrieve the country name
        query = """
        SELECT AVG(precipitation) AS avg_precipitation, countries.name AS country_name
        FROM daily_weather_entries
        JOIN cities ON daily_weather_entries.city_id = cities.id
        JOIN countries ON cities.country_id = countries.id
        WHERE date BETWEEN ? AND ?
        GROUP BY countries.name
        """
        # Get a cursor object from the database connection
        cursor = connection.cursor()
        # Calculate start and end dates for the specified year
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query, (start_date, end_date))
        # Fetch all rows from the results
        rows = results.fetchall()
        if rows:
            # Iterate over the results and display the average precipitation for each country
            for row in rows:
                avg_precipitation = row['avg_precipitation']
                if avg_precipitation is not None:
                    avg_precipitation_formatted = round(avg_precipitation, 2)
                    print(f"Average annual precipitation for {row['country_name']} in {year}: {avg_precipitation_formatted}")
                else:
                    print(f"No data found for {row['country_name']} in {year}.")
        else:
            print(f"No data found for the specified parameters.")
    except sqlite3.OperationalError as ex:
        print(ex)

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    with sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        select_all_countries(connection)
        print()
        select_all_cities(connection)
        print()
        average_annual_temperature(connection, 1, 2020)
        print()
        average_seven_day_precipitation(connection, 2, '2021-01-01')
        print()
        average_mean_temp_by_city(connection, '2020-01-01', '2020-12-31')
        print()
        average_annual_precipitation_by_country(connection,2020)
        print()