
import sqlite3
import phase_1
import phase_2
import phase_4
import tkinter as tk

class MenuGUI:
    def __init__(window, connection):
        window.connection = connection

        # Create the main window
        window.root = tk.Tk()
        window.root.title("Menu")

        # Create menu options
        menu_options = [
            "Select all Countries",
            "Select all cities",
            "Average Annual Temperature for a Specific City",
            "Average Seven Day Precipitation for a specific city",
            "Average Mean Temperature for all cities",
            "Average Annual Precipitation for each Country",
            "Plot Average Mean Temperature for Cities",
            "Plot Average Annual Precipitation by Country",
            "Ploting Minimun and Maximum Temperatures",
            "Plot Average Annual Temperature by City",
            "Plot Climate Scatter Graph",
            "Insert more information into database",
            "Removing tables from database",
            "Deleting entire database",
            "Quitting Application"
        ]

        # Create buttons for each option
        for index, option in enumerate(menu_options, start=1):
            button = tk.Button(window.root, text=f"{index}. {option}", command=lambda i=index: window.handle_choice(i))
            button.pack()

    def handle_choice(window, choice):
        if choice == 1:
            phase_1.select_all_countries(window.connection)
        elif choice == 2:
            phase_1.select_all_cities(window.connection)
        elif choice == 3:
            city_id = int(input("City number between 1 to 4 ? "))
            year = int(input("Year from 2020-2022 ? "))
            phase_1.average_annual_temperature(window.connection, city_id, year)
        elif choice == 4:
            city_id = int(input("City number between 1 to 4: "))
            start_date = input("Start date (YYYY-MM-DD): ")
            phase_1.average_seven_day_precipitation(window.connection, city_id, start_date)
        elif choice == 5:
            date_from = input("Start date (YYYY-MM-DD): ")
            date_to = input("End date (YYYY-MM-DD): ")
            phase_1.average_mean_temp_by_city(window.connection, date_from, date_to)
        elif choice == 6:
            year = int(input("Year from 2020-2022 ? "))
            phase_1.average_annual_precipitation_by_country(window.connection, year)
        elif choice == 7:
            date_from = input("Start date (YYYY-MM-DD): ")
            date_to = input("End date (YYYY-MM-DD): ")
            phase_2.plot_average_mean_temp_by_city(window.connection, date_from, date_to)
        elif choice == 8:
            year = int(input("Year from 2020-2022 ? "))
            phase_2.plot_average_annual_precipitation_by_country(window.connection, year)
        elif choice == 9:
            city_id = int(input("Select a city ID from 1 to 4: "))
            date_from = input("Select a start date(10 day limit) (YYYY-MM-DD): ")
            date_to = input("Select a end date (YYYY-MM-DD): ")     
            phase_2.plot_min_max_temperatures(window.connection, city_id, date_from, date_to)
        elif choice == 10:
            year = int(input("Select a year from 2020-2022: "))
            phase_2.plot_average_annual_temperature_by_city(window.connection, year)
        elif choice == 11:
            city_id = int(input("Select a city ID from 1 to 4: "))
            phase_2.climate_scatter_graph(window.connection,city_id)   
        elif  choice == 12:
            phase_4.insert_temperature("daily_weather_entries", "cities", "countries")
        elif choice == 13:
            table = input("Select what table to remove from cities,countries, sqlite_sequence and daily_weather_entries: " )
            query= f"DROP TABLE IF EXISTS {table};"
            cursor= window.connection.cursor()
            cursor.execute(query)
            print(f"{table} table deleted sucessfully")
        elif choice == 14:
            confirmation= input("Are you sure you want to delete the entire database?:[Yes/NO] ")
            if confirmation.lower() == 'yes':
                cursor=window.connection.cursor()
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
        elif choice == 15:
            print("Quitting Application.")
            window.root.destroy()
    def run(window):
        window.root.mainloop()
if __name__ == "__main__":
    with sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        menu_gui = MenuGUI(connection)
        menu_gui.run()
