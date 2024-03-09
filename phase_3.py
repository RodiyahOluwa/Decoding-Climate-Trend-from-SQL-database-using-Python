# Author: <Rodiyah Oluwa>
# Student ID: <D3127027>
import sqlite3
import phase_1
import phase_2
import phase_4

def Menu(connection):
     while True:
            print("\nMenu:")
            print()
            print("FROM PHASE 1")
            print("1. Select all Countries")
            print("2. Select all cities")
            print("3. Average Annual Temperature for a Specific City")
            print("4. Average Seven Day Precipitation for a specific city")
            print("5. Average Mean Temperature for all cities")
            print("6. Average Annual Precipitation for each Country")
            print()
            print("FROM PHASE 2")
            print("7. Plot Average Mean Temperature for Cities")
            print("8. Plot Average Annual Precipitation by Country")
            print("9. Ploting Minimun and Maximum Temperatures")
            print("10. Plot Average Annual Temperature by City")
            print("11. Plot Climate Scatter Graph")
            print()
            print("FROM PHASE 4")
            print("12. Insert more information into database")
            print("13. Removing tables from database")
            print("14. Deleting entire database")
            print("15. Quitting Application")
            choice = input("Select your choice from 1 to 15: ")
            if choice == '1':
               phase_1.select_all_countries(connection)
            elif choice == '2':
                phase_1.select_all_cities(connection)         
            elif choice == '3':
                city_id = int(input("City number between 1 to 4 ? "))
                year = int(input("Year from 2020-2022 ? "))
                phase_1.average_annual_temperature(connection, city_id, year)
            elif choice == "4":
                city_id = int(input("City number between 1 to 4: "))
                start_date = input("Start date (YYYY-MM-DD): ")
                phase_1.average_seven_day_precipitation(connection, city_id, start_date)
            elif choice == "5":               
                date_from = input("Start date (YYYY-MM-DD): ")
                date_to = input("End date (YYYY-MM-DD): ")
                phase_1.average_mean_temp_by_city(connection, date_from, date_to) 
            elif choice == "6":
                year = int(input("Year from 2020-2022 ? "))
                phase_1.average_annual_precipitation_by_country(connection, year)
            elif choice == "7":
                date_from = input("Start date (YYYY-MM-DD): ")
                date_to = input("End date (YYYY-MM-DD): ")
                phase_2.plot_average_mean_temp_by_city(connection, date_from, date_to)
            elif choice == "8":
                year = int(input("Year from 2020-2022 ? "))
                phase_2.plot_average_annual_precipitation_by_country(connection, year)
            elif choice == "9":
                city_id = int(input("Select a city ID from 1 to 4: "))
                date_from = input("Select a start date(10 day limit) (YYYY-MM-DD): ")
                date_to = input("Select a end date (YYYY-MM-DD): ")     
                phase_2.plot_min_max_temperatures(connection, city_id, date_from, date_to)
            elif choice == "10":
                year = int(input("Select a year from 2020-2022: "))
                phase_2.plot_average_annual_temperature_by_city(connection, year)
            elif choice == "11":
                city_id = int(input("Select a city ID from 1 to 4: "))
                phase_2.climate_scatter_graph(connection,city_id)   
            elif  choice == "12":
                phase_4.insert_temperature("daily_weather_entries", "cities", "countries")
            elif choice == "13":
                table = input("Select what table to remove from cities,countries, sqlite_sequence and daily_weather_entries: " )
                query= f"DROP TABLE IF EXISTS {table};"
                cursor= connection.cursor()
                cursor.execute(query)
                print(f"{table} table deleted sucessfully")
            elif choice == "14":
                confirmation= input("Are you sure you want to delete the entire database?:[Yes/NO] ")
                if confirmation.lower() == 'yes':
                    cursor=connection.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    for table in tables:
                        table_name = table[0]
                        if table_name == 'sqlite_sequence':
                            continue
                        query = f"DROP TABLE IF EXISTS {table_name};"
                        cursor.execute(query)    
                    print("Entire tables dropped successfully.")                           
                else:
                    print("Operation cancelled.")
            elif choice == "15":
                print("Quitting Application.")
                break
            else:
                print("Invalid.Please enter a number from the given menu")


if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    with sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        Menu(connection)


