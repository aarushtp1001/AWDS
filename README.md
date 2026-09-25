# Astronomical Weather Database System (AWDS)
## What It Does
This database system uses NASA's APIs to fetch asteroid and solar flare data. Then, it feeds the relevant data into an SQLite database. After creating the tables in the database, the system provides the user with specialized functions and SQL commands that he/she can perform on the database.
## Features
Using AWDS, one can perform the following tasks:
- Viewing general space weather statistics.
- Searching asteroids using speed factor.
- Searching asteroids using miss-distance factor.
- Viewing potentially hazardous asteroids (sorted by miss-distance).
- Searching solar flares according to class/region/location.
- Finding all potentially hazardous asteroids that happened to pass by close to Earth when a dangerous (X-Class or M-Class) solar flare occurred.
## NASA APIs Used
In AWDS, I used:
- **NASA NeoWs API :** I used this for obtaining asteroid data.
- **NASA DONKI API :** I used this for obtaining solar flare data.
## How It Works
The user runs main.py, which then prompts the user for starting and ending dates of gathering space weather data. If the data is successfully received, the program creates and adds relevant data to an SQLite database into two tables, asteroids and solar_flares. Once the database is created, the program then prompts the user for selecting a command from the given menu. Once the user selects a command, the program executes that command using SQL and returns the relevant data.
## Project Structure
The AMDS encompasses the following modules:
- **config.py :**  Used for storing the API demo key, the base URLs for NeoWs and DONKI, and the name of the SQLite database.
- **fetcher.py :** Uses the urllib package for fetching the JSON data, and then parses it to extract the useful information which is relevant to the project.
- **database.py :** Uses the sqlite3 module to create an SQLite database, and subsequently create two tables, namely asteroids and solar_flares. It then uses all the extracted data from fetcher and feeds it into the created database tables.
- **functions.py :** This file houses all the user-defined functions which are used in the project.
- **main.py :** The main file which orchestrates all the other 4 files to create a cohesive menu-driven program.
## Requirements / Setup
### Requirements
For running this system, you need:
- Python 3.x
- An Internet connection for API calls
### Setup
1. Download the ZIP file of the repository.
2. Extract the files in a suitable place on your computer.
3. Open the terminal inside the inner-most folder.
4. Run the command: 'python main.py'
## Example Usage / Output
## What I Learned
I learnt how to utilize built-in Python packages and modules along with their methods in order to create an application that focuses on two aspects of space weather. I understood the procedure behind obtaining JSON data and parsing it to extract the relevant information. I also learnt how to create databases and how to work with them using SQL, through Python. Most importantly, I realized the convenience of adapting the modular approach to big coding project like this one, because not only does this approach make debugging easier, it makes it significantly more intuitive to understand. In addition, I also got over my fear of creating projects with hundreds of lines of code, because projects involving such concepts naturally tend to cross 500 lines of code, so that anxiety of having to forcibly create a long project was gone. 
## Credits / API References
