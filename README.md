# Astronomical Weather Database System AWDS (nasa-space-pipeline)
## What It Does
This database system uses NASA's APIs to fetch asteroid and solar flare data. Then, it feeds the relevant data into an SQLite database. After creating the tables in the database, the system provides the user with specialized functions and SQL commands that he/she can perform on the database.
## Features
Using AWDS, one can perform the following tasks:
- **1.** Viewing general space weather statistics.
- **2.** Searching asteroids using speed factor.
- **3.** Searching asteroids using miss-distance factor.
- **4.** Viewing potentially hazardous asteroids (sorted by miss-distance).
- **5.** Searching solar flares according to class/region/location.
- **6.** Finding all potentially hazardous asteroids that happened to pass by close to Earth when a dangerous (X-Class or M-Class) solar flare occurred.
## NASA APIs Used
In AWDS, I used:
- **NASA NeoWs API :** I used this for obtaining asteroid data.
- **NASA DONKI API :** I used this for obtaining solar flare data.
## How It Works
The user runs main.py, which then prompts the user for starting and ending dates of gathering space weather data. If the data is successfully received, the program creates and adds relevant data to an SQLite database into two tables, asteroids and solar_flares. Once the database is created, the program then prompts the user for selecting a command from the given menu. Once the user selects a command, the program executes that command using SQL and returns the relevant data.
## Project Structure
The AMDS encompasses the following modules:
- **1. config.py :**  Used for storing the API demo key, the base URLs for NeoWs and DONKI, and the name of the SQLite database.
- **2. fetcher.py :** Uses the urllib package for fetching the JSON data, and then parses it to extract the useful information which is relevant to the project.
- **3. database.py :** Uses the sqlite3 module to create an SQLite database, and subsequently create two tables, namely asteroids and solar_flares. It then uses all the extracted data from fetcher and feeds it into the created database tables.
- **4. functions.py :** This file houses all the user-defined functions which are used in the project.
- **5. main.py :** The main file which orchestrates all the other 4 files to create a cohesive menu-driven program.
