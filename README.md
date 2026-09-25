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
- **NASA NeoWs API :** for obtaining asteroid data.
- **NASA DONKI API :** for obtaining solar flare data.
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
When main.py is executed in the terminal, it prompts the user for dates by which it searches for asteroids and solar flares. Often times the NASA DONKI server experiences a 503 Error, which causes the program to immediately terminate. In that case, the user may run the program 2-3 times until it successfully creates the tables.
For example, if the user chose option 1 and then option 7, the output would look as follows, provided that the default dates work.
### Sample Output
Welcome to the Astronomical Weather Database System AWDS (nasa-space-pipeline)!

We need to populate the database first.

Enter the beginning date from where you want to start searching for asteroids from:
Enter the ending date from where you want to start searching for asteroids from:
Enter the beginning date from where you want to end searching for solar flares from:
Enter the ending date from where you want to end searching for solar flares from:

Populating database...
Both tables were created successfully!
The Astronomical Weather Database has been successfully created!


--------------------------------------------MENU--------------------------------------------
1. View general space weather statistics.
2. Search asteroids using speed factor.
3. Search asteroids using miss-distance factor.
4. View potentially hazardous asteroids (sorted by miss-distance).
5. Search solar flares according to class/region/location.
6. Find all potentially hazardous asteroids that happened to pass by close to Earth when a dangerous (X-Class or M-Class) solar flare occurred.
7. Exit.

Enter your choice: 1

--------------------SUMMARY--------------------
> Number of asteroids returned: 15
> Number of flares returned: 68

> The fastest asteroid was (2021 GR12) with a speed of 36372.26311061919 meters/second.
> The minimum asteroid velocity was 4803.578373623056 meters/second.
> The average asteroid velocity was 14556.48541787483 meters/second.

> The closest asteroid was (2012 DW60) with a miss distance of 11795415646.299294 meters.
> The maximum asteroid miss distance was 71591694775.9536 meters.
> The average asteroid miss distance was 44465130765.123436 meters.

> Number of flares returned by type:
 > A-Class --> 0
 > B-Class --> 0
 > C-Class --> 4
 > M-Class --> 62
 > X-Class --> 2

> The most active region was region number 14479 which occurred 47 times.

The created dictionary is:
{'number_of_asteroids': 15, 'number_of_flares': 68, 'asteroids_velocity_data': {'max_velocity': 36372.26311061919, 'min_velocity': 4803.578373623056, 'avg_velocity': 14556.48541787483}, 'asteroids_miss_distance_data': {'max_miss_distance': 71591694775.9536, 'min_miss_distance': 11795415646.299294, 'avg_miss_distance': 44465130765.123436}, 'fastest_asteroid': '(2021 GR12)', 'closest_asteroid': '(2012 DW60)', 'flare_class_data': {'A': 0, 'B': 0, 'C': 4, 'M': 62, 'X': 2}, 'most_active_region': {'region_num': 14479, 'frequency': 47}}

--------------------------------------------MENU--------------------------------------------
1. View general space weather statistics.
2. Search asteroids using speed factor.
3. Search asteroids using miss-distance factor.
4. View potentially hazardous asteroids (sorted by miss-distance).
5. Search solar flares according to class/region/location.
6. Find all potentially hazardous asteroids that happened to pass by close to Earth when a dangerous (X-Class or M-Class) solar flare occurred.
7. Exit.

Enter your choice: 7

Thank you for using the Astronomical Weather Database System!
Now exiting...
## What I Learnt
I learnt how to utilize built-in Python packages and modules along with their methods in order to create an application that focuses on two aspects of space weather. I understood the procedure behind obtaining JSON data and parsing it to extract the relevant information. I also learnt how to create databases and how to work with them using SQL, through Python. Most importantly, I realized the convenience of adapting the modular approach to big coding project like this one, because not only does this approach make debugging easier, it makes it significantly more intuitive to understand. In addition, I also got over my fear of creating projects with hundreds of lines of code, because projects involving such concepts naturally tend to cross 500 lines of code, so that anxiety of having to forcibly create a long project was gone. 
## Credits / API References
### Learning Resources
- **Coursera** provided a platform for learning Python.
- **PY4E Specialization by The University of Michigan** taught me the concepts which I applied in this project.
- **Dr. Charles Russell Severance** conducted the PY4E lessons.
- **Computer Science with Python Class XII by Preeti Arora** was helpful for reviewing Python built-in functions.
### API References
- **NASA Open APIs :** documentation can be found at https://api.nasa.gov/
