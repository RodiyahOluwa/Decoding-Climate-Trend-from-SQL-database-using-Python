import matplotlib.pyplot as plt
import sqlite3
def plot_average_mean_temp_by_city(connection, date_from, date_to):
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
          # Lists to store data for plotting
        cities = []
        avg_temps = []
        # Fetch all row from the results
        for row in results:
            if row and row['avg_temperature'] is not None:
                # Check if the value is not None before appending to lists
                cities.append(row['city_name'])
                avg_temps.append(row['avg_temperature'])
                print(f"Average mean temperature for {row['city_name']} from {date_from} to {date_to} is {row['avg_temperature']:.2f}")
            else:
                print(f"No data found for the specified parameters.")
         # Plotting
        plt.bar(cities, avg_temps, color='skyblue')
        plt.xlabel('City')
        plt.ylabel('Average Mean Temperature (°C)')
        plt.title(f'Average Mean Temperature for All Cities ({date_from} to {date_to})')
        plt.savefig('Avg_mean_temp.jpg')
        plt.show()
    except sqlite3.OperationalError as ex:
        print(ex)

def plot_average_annual_precipitation_by_country(connection, year):
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
         # Lists to store data for plotting
        countries = []
        avg_precipitation = []
        # Fetch all rows from the results
        rows = results.fetchall()
        if rows:
            # Iterate over the results and display the average precipitation for each country
            for row in rows:
                countries.append(row['country_name'])
                avg_precipitation = row['avg_precipitation']
                if avg_precipitation is not None:
                    avg_precipitation_formatted = round(avg_precipitation, 2)
                    print(f"Average annual precipitation for {row['country_name']} in {year}: {avg_precipitation_formatted}")
                else:
                    print(f"No data found for {row['country_name']} in {year}.")
        else:
            print(f"No data found for the specified parameters.")
             # Plotting
        plt.bar(countries, avg_precipitation, color='skyblue')
        plt.xlabel('Country')
        plt.ylabel('Average Annual Precipitation')
        plt.title(f'Average Annual Precipitation for All Countries in year {year}')
        plt.savefig('Avg_annual_precipitation.jpg')
        plt.show()
    except sqlite3.OperationalError as ex:
        print(ex)

def plot_min_max_temperatures(connection, city_id, date_from, date_to):
    try:
        connection.row_factory = sqlite3.Row
        # Fetch the city name
        city_name_query = f"SELECT name FROM cities WHERE id = {city_id};"
        city_name_result = connection.execute(city_name_query).fetchone()
        city_name = city_name_result['name'] if city_name_result else f"City {city_id}"
        #define the query
        query = f"""
        SELECT date, MIN(min_temp) AS min_temp, MAX(max_temp) AS max_temp
        FROM daily_weather_entries 
        WHERE city_id = {city_id} AND date BETWEEN '{date_from}' AND '{date_to}'
        GROUP BY date;
        """
        # Get a cursor object from the database connection
        cursor = connection.cursor()
        # Execute the query via the cursor object
        results = cursor.execute(query)      
        # store data for plotting
        dates = []
        min_temp = []
        max_temp = []
        # Fetch all rows from the results
        for row in results:
            if row and row['min_temp'] is not None and row['max_temp'] is not None:
                # Check if both values are not None before appending to lists
                dates.append(row['date'])
                min_temp.append(row['min_temp'])
                max_temp.append(row['max_temp'])
                print(f"The min and max temperature in {city_name} on  {row['date']} is Min: {row['min_temp']:.2f} and Max: {row['max_temp']:.2f}")
        # Plotting
        plt.plot(dates, min_temp, marker='o', label= 'Min Temperature', linestyle='-', linewidth=2)
        plt.plot(dates, max_temp, marker='o', label= 'Max Temperature', linestyle='-', linewidth=2)
        plt.xlabel('Dates')
        plt.ylabel('Temperature (°C)')
        plt.title(f'Min & Max Temps for {city_name} from {date_from} to {date_to} ')
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('min_max_temp.jpg')
        plt.show()
    except sqlite3.OperationalError as ex:
        print(ex)

def plot_average_annual_temperature_by_city(connection, year):
    try:
        connection.row_factory = sqlite3.Row
        # Define the query
        query = """
        SELECT AVG(mean_temp) as avg_annual_temp, cities.name AS city_name
        FROM daily_weather_entries 
        JOIN cities ON daily_weather_entries.city_id = cities.id
        WHERE date BETWEEN ? AND ?
        GROUP BY cities.name
        """     
        # Get a cursor object from the database connection
        cursor = connection.cursor()
        # Calculate start and end dates for the specified year
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query, (start_date, end_date))
         # store data for plotting
        cities = []
        avg_annual_temp = []
        # Iterate over the results and display the results.
        for row in results:
            if row and row['avg_annual_temp'] is not None:
        # Check if the value is not None before appending to lists
                cities.append(row['city_name'])
                avg_annual_temp.append(row['avg_annual_temp'])
                print(f"Average annual temperature for {row['city_name']} in year {year} was {row['avg_annual_temp']:.2f}")
            else:
                 print(f"No data found for the specified parameters.")
             # Plotting
        plt.bar(cities, avg_annual_temp, color='skyblue')
        plt.xlabel('City')
        plt.ylabel('Average Annual Temperature')
        plt.title(f'Average Annual Temperature from {year}-01-01 to {year}-12-31')
        plt.savefig('Avg_annual_temp.jpg')
        plt.show()
    except sqlite3.OperationalError as ex:
        print(ex)

def climate_scatter_graph(connection,city_id):
    try:
        connection.row_factory = sqlite3.Row
        # Fetching the city name
        city_name_query = f"SELECT name FROM cities WHERE id = {city_id};"
        city_name_result = connection.execute(city_name_query).fetchone()
        city_name = city_name_result['name'] if city_name_result else f"City {city_id}"
         # Define the query
        query = f"""
        SELECT mean_temp as avg_temperature, precipitation AS avg_precipitation
        FROM daily_weather_entries
        WHERE city_id = {city_id}
        """   
        # Get a cursor object from the database connection
        cursor = connection.cursor()
        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query)
        # Lists to store data for plotting
        avg_precipitation = []
        avg_temperature =[]
        # Fetch all rows from the results
        rows = results.fetchall()
        if rows:
            # Iterate over the results and display the average precipitation for each country
            for row in rows:
                avg_precipitation.append(row['avg_precipitation'])
                avg_temperature.append(row['avg_temperature'])   
                if row and row['avg_temperature'] is not None and row['avg_precipitation'] is not None:
                    print(f"The Precipitation and Temperature in {city_name} is Temp:{row['avg_temperature']:.2f} Precipitation:{row['avg_precipitation']:.2f} ")            
        else:
            print(f"No data found for the specified parameters.")
        plt.scatter(avg_temperature, avg_precipitation, color='red', label=' Temperature')
        plt.scatter(avg_temperature, avg_precipitation, color='skyblue', label='Precipitation')
        plt.xlabel('Average Temperature (°C)')
        plt.ylabel('Average Precipitation')
        plt.title(f'Avg Temperature and Precipitation in {city_name}')
        plt.legend()
        plt.savefig('climate_graph.jpg')
        plt.show()
    except sqlite3.OperationalError as ex:
        print(ex)


if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    with sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        plot_average_mean_temp_by_city(connection, '2020-01-01', '2020-07-14')
        print()
        plot_average_annual_precipitation_by_country(connection, 2020)
        print()
        plot_min_max_temperatures(connection,1,'2020-01-01','2020-01-10')
        print()
        plot_average_annual_temperature_by_city(connection, 2021)
        print()
        climate_scatter_graph(connection,4)
        print()
       

        
