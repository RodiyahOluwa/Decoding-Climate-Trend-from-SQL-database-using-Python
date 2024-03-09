# Author: <Rodiyah Oluwa>
# Student ID: <D3127027>
import sqlite3
import requests

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 12.0001,
    "longitude": 8.5167,
    "start_date": "2020-01-01",
    "end_date": "2022-12-23",
    "hourly": "temperature_2m",
    "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "precipitation_hours"]
}

results = requests.get(url, params=params)
raw_results = results.json()

date = raw_results['daily']['time']
min_temp = raw_results['daily']['temperature_2m_min']
max_temp = raw_results['daily']['temperature_2m_max']
mean_temp = raw_results['daily']['temperature_2m_mean']
precipitation = raw_results['daily']['precipitation_hours']


def insert_temperature(daily_weather_entries, cities, countries):
    try:
        connection = sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db")
        cursor = connection.cursor()

        # Check if the data already exists in daily_weather_entries table
        existing_data_query = f"SELECT * FROM {daily_weather_entries} WHERE city_id=? AND date=?;"
        existing_data_check = cursor.execute(existing_data_query, (6, date[0])).fetchone()

        if existing_data_check:
            print("Error: Data for this date and city already exists.")
        else:
            # Insert temperature data
            temperature_query = f"""
                INSERT INTO {daily_weather_entries} (city_id, date, min_temp, max_temp, mean_temp, precipitation)
                VALUES (?, ?, ?, ?, ?, ?);
            """
            city_id = 6
            # Zip the data
            data_to_insert = zip([city_id] * len(date), date, min_temp, max_temp, mean_temp, precipitation)
            cursor.executemany(temperature_query, data_to_insert)

            # Check if the data already exists in cities table
            existing_city_query = f"SELECT * FROM {cities} WHERE name=? AND country_id=?;"
            existing_city_check = cursor.execute(existing_city_query, ("Kano", 3)).fetchone()

            if existing_city_check:
                print("Error: City data already exists.")
            else:
                # Insert city data
                # Extract values from the params
                longitude = params.get("longitude")
                latitude = params.get("latitude")
                # Define the query
                city_query = f"""
                    INSERT INTO {cities} (name, longitude, latitude, country_id)
                    VALUES (?, ?, ?, ?);
                """
                country_id = 3
                city_name = "Kano"
                # Execute the query with actual data
                cursor.execute(city_query, (city_name, longitude, latitude, country_id))

                # Check if the data already exists in countries table
                existing_country_query = f"SELECT * FROM {countries} WHERE name=? AND timezone=?;"
                existing_country_check = cursor.execute(existing_country_query, ("Nigeria", "Africa/Lagos")).fetchone()

                if existing_country_check:
                    print("Error: Country data already exists.")
                else:
                    # Insert country data
                    country_query = f"""
                        INSERT INTO {countries} (name, timezone)
                        VALUES (?, ?);
                    """
                    country_data = [("Nigeria", "Africa/Lagos")]
                    cursor.executemany(country_query, country_data)

                    # Commit the changes to the database
                    connection.commit()
                    print("Data inserted successfully.")

    except sqlite3.OperationalError as ex:
        print(ex)

    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()

# Call the function
insert_temperature("daily_weather_entries", "cities", "countries")
