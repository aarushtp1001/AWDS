# This file contains all the methods that will be used in main.py
import config, fetcher, database
import json, sqlite3

# Menu
def display_menu():
    print()
    print('--------------------------------------------MENU--------------------------------------------')
    print('1. View general space weather statistics.')
    print('2. Search asteroids using speed factor.')
    print('3. Search asteroids using miss-distance factor.')
    print('4. View potentially hazardous asteroids (sorted by miss-distance).')
    print('5. Search solar flares according to class/region/location.')
    print('6. Find all potentially hazardous asteroids that happened to pass by close to Earth when a dangerous (X-Class or M-Class) solar flare occurred.')
    print('7. Exit.')
    print()

# Note: -1 stands for "invalid input", -2 stands for "no values returned".

# Choice 1
def display_general_stats(): 
    ## no. of asteroids and no. of flares returned
    ## max asteroid speed, min asteroid speed, avg asteroid speed
    ## max asteroid distance, min asteroid distance, avg asteroid distance
    ## closest asteroid, fastest asteroid
    ## no. of flares returned by class type
    ## most active region number on the Sun

    conn = sqlite3.connect(config.DB_NAME)
    cur = conn.cursor()

    general_stats = dict()

    cur.execute('SELECT COUNT(*) FROM asteroids;')
    general_stats['number_of_asteroids'] = (cur.fetchone())[0]

    cur.execute('SELECT COUNT(*) FROM solar_flares;')
    general_stats["number_of_flares"] = (cur.fetchone())[0]

    cur.execute('SELECT MAX(relative_velocity), MIN(relative_velocity), AVG(relative_velocity) FROM asteroids;')
    returned_velo_data = cur.fetchone()
    general_stats['asteroids_velocity_data'] = dict()
    general_stats['asteroids_velocity_data']['max_velocity'] = returned_velo_data[0]
    general_stats['asteroids_velocity_data']['min_velocity'] = returned_velo_data[1]
    general_stats['asteroids_velocity_data']['avg_velocity'] = returned_velo_data[2]

    cur.execute('SELECT MAX(miss_distance), MIN(miss_distance), AVG(miss_distance) FROM asteroids;')
    returned_dist_data = cur.fetchone()
    general_stats['asteroids_miss_distance_data'] = dict() 
    general_stats['asteroids_miss_distance_data']['max_miss_distance'] = returned_dist_data[0]
    general_stats['asteroids_miss_distance_data']['min_miss_distance'] = returned_dist_data[1]
    general_stats['asteroids_miss_distance_data']['avg_miss_distance'] = returned_dist_data[2]
    
    # Unlike other SQL software, SQLite can use non-aggregate columns with the aggregate functions MAX() and MIN(), as shown below.
    cur.execute('SELECT name, MAX(relative_velocity) FROM asteroids;')
    general_stats['fastest_asteroid'] = (cur.fetchone())[0]
    cur.execute('SELECT name, MIN(miss_distance) FROM asteroids;')
    general_stats['closest_asteroid'] = (cur.fetchone())[0]

    cur.execute('SELECT flare_class, COUNT(*) FROM solar_flares GROUP BY flare_class;')
    returned_flare_class_data = cur.fetchall()
    general_stats['flare_class_data'] = dict()

    # Setting default values.
    general_stats['flare_class_data']['A'] = 0
    general_stats['flare_class_data']['B'] = 0
    general_stats['flare_class_data']['C'] = 0
    general_stats['flare_class_data']['M'] = 0
    general_stats['flare_class_data']['X'] = 0
    for flare in returned_flare_class_data:
        general_stats['flare_class_data'][flare[0]] = flare[1]

    cur.execute('''SELECT active_region_num, COUNT(*) as freq FROM solar_flares
                   GROUP BY active_region_num ORDER BY freq DESC LIMIT 1;''')
    most_active_region = cur.fetchone() # possible None error
    general_stats['most_active_region'] = dict()
    try:
        general_stats['most_active_region']['region_num'] = most_active_region[0]
        general_stats['most_active_region']['frequency'] = most_active_region[1]
    except: # if most_active_region is None
        general_stats['most_active_region']['region_num'] = None
        general_stats['most_active_region']['frequency'] = None  
    
    print('--------------------SUMMARY--------------------')
    print(f'> Number of asteroids returned: {general_stats["number_of_asteroids"]}')
    print(f'> Number of flares returned: {general_stats["number_of_flares"]}')
    print()
    print(f'> The fastest asteroid was {general_stats["fastest_asteroid"]} with a speed of {general_stats["asteroids_velocity_data"]["max_velocity"]} meters/second.')
    print(f'> The minimum asteroid velocity was {general_stats["asteroids_velocity_data"]["min_velocity"]} meters/second.')
    print(f'> The average asteroid velocity was {general_stats["asteroids_velocity_data"]["avg_velocity"]} meters/second.')
    print()
    print(f'> The closest asteroid was {general_stats["closest_asteroid"]} with a miss distance of {general_stats["asteroids_miss_distance_data"]["min_miss_distance"]} meters.')
    print(f'> The maximum asteroid miss distance was {general_stats["asteroids_miss_distance_data"]["max_miss_distance"]} meters.')
    print(f'> The average asteroid miss distance was {general_stats["asteroids_miss_distance_data"]["avg_miss_distance"]} meters.')
    print()
    print('> Number of flares returned by type:')
    print(f' > A-Class --> {general_stats["flare_class_data"]["A"]}')
    print(f' > B-Class --> {general_stats["flare_class_data"]["B"]}')
    print(f' > C-Class --> {general_stats["flare_class_data"]["C"]}')
    print(f' > M-Class --> {general_stats["flare_class_data"]["M"]}')
    print(f' > X-Class --> {general_stats["flare_class_data"]["X"]}') 
    print()
    print(f'> The most active region was region number {general_stats["most_active_region"]["region_num"]} which occurred {general_stats["most_active_region"]["frequency"]} times.')
    print()

    conn.close()
    return general_stats

# Choice 2
def search_asteroids_by_speed():
    conn = sqlite3.connect(config.DB_NAME)
    cur = conn.cursor()

    try: 
        q = int(input('Would you like to search by minimum velocity or by maximum velocity (1 for minimum, 2 for maximum)? '))
        print()
    except:
        print() 
        print('Bad input, please run the program again.')
        print()
        conn.close()
        return -1

    if q == 1:
        try: min_velo = float(input('Enter the minimum velocity in m/s by which you want to search asteroids: '))
        except:
            print()
            print('Try again. Enter a floating point number...')
            print()
            conn.close()
            return -1
        
        print()
        
        cur.execute('SELECT * FROM asteroids WHERE relative_velocity >= ?;', (min_velo,))
        asteroid_list = cur.fetchall()

        if len(asteroid_list) < 1:
            print()
            print(f'No asteroid was found to have greater velocity than or equal to {min_velo} m/s.')
            print()
            conn.close()
            return -2

        conn.close()
        return 'min', min_velo, asteroid_list
            
    elif q == 2:
        try: max_velo = float(input('Enter the maximum velocity in m/s by which you want to search asteroids: '))
        except:
            print()
            print('Try again. Enter a floating point number...')
            print()
            conn.close()
            return -1
        
        print()

        cur.execute('SELECT * FROM asteroids WHERE relative_velocity <= ?;', (max_velo,))
        asteroid_list = cur.fetchall()
        
        if len(asteroid_list) < 1:
            print()
            print(f'No asteroid was found to have lesser velocity than or equal to {max_velo} m/s.')
            print()
            conn.close()
            return -2

        conn.close()
        return 'max', max_velo, asteroid_list 
            
    else:
        print('Enter either 1 or 2. Please try again...')
        print()
        conn.close()
        return -1

# Choice 3
def search_asteroids_by_miss_dist():
    conn = sqlite3.connect(config.DB_NAME)
    cur = conn.cursor()

    try:
        q = int(input('Would you like to search for asteroids by minimum miss distance or maximum miss distance (1 for minimum, 2 for maximum)? '))
        print()
    except:
        print()
        print('Bad input, please run the program again.')
        print()
        conn.close()
        return -1

    if q == 1:
        try: min_dist = float(input('Enter the minimum distance in meters by which you want to search asteroids: '))
        except:
            print()
            print('Try again. Enter a floating point number...')
            print()
            conn.close()
            return -1
        
        print()

        cur.execute('SELECT * FROM asteroids WHERE miss_distance >= ?;', (min_dist,))
        asteroid_list = cur.fetchall()

        if len(asteroid_list) < 1:
            print()
            print(f'No asteroid was found to have greater miss distance than or equal to {min_dist} metres.')
            print()
            conn.close()
            return -2

        conn.close()
        return 'min', min_dist, asteroid_list 
            
    elif q == 2:
        try: max_dist = float(input('Enter the maximum distance in meters by which you want to search asteroids: '))
        except:
            print()
            print('Try again. Enter a floating point number...')
            print()
            conn.close()
            return -1
        
        print()

        cur.execute('SELECT * FROM asteroids WHERE miss_distance <= ?;', (max_dist,))
        asteroid_list = cur.fetchall()

        if len(asteroid_list) < 1:
            print()
            print(f'No asteroid was found to have lesser miss distance than or equal to {max_dist} metres.')
            print()
            conn.close()
            return -2

        conn.close()
        return 'max', max_dist, asteroid_list

    else:
        print()
        print('Enter either 1 or 2. Please try again...')
        print()
        conn.close()
        return -1

# Choice 4
def view_pot_hazardous_asteroids():
    conn = sqlite3.connect(config.DB_NAME)
    cur = conn.cursor()

    cur.execute('SELECT * FROM asteroids WHERE potentially_hazardous = 1 ORDER BY miss_distance;')
    asteroid_list = cur.fetchall()
    asteroid_name_list = []

    if len(asteroid_list) < 1:
        print()
        print('No potentially hazardous asteroids were found in this date range.')
        print()
        return

    print(f'        The following asteroids were found to be potentially hazardous (ordered in ascending order by miss distance in meters):')
    print('FORMAT: (id, name, min_diameter, max_diameter, potentially_hazardous, close_approach_date, relative_velocity, miss_distance)')
    print()
    for asteroid in asteroid_list:
        print(asteroid)
        asteroid_name_list.append(asteroid[1])
    print()

    print('In a nutshell, the asteroids which are potentially hazardous are as follows:')
    print()
    for asteroid_name in asteroid_name_list:
        print(asteroid_name, end=' ')
    print()

    conn.close()

# Choice 5
def search_flares(factor='class'):
    conn = sqlite3.connect(config.DB_NAME)
    cur = conn.cursor()

    # In the return statements, the order in which the values are returned in the tuple are in increasing order of the capacity required to process the value.
    # This was done to ensure maximum speed of the main function, although it might only differ in a few milliseconds.

    if factor == 'class':
        flare_class = input('Enter the flare class you want to search by: ')
        print()

        if (len(flare_class) != 1):
            print()
            print('Try again. Enter a single letter flare class...')
            print()
            conn.close()
            return -1

        else:
            flare_class = flare_class.upper()
            cur.execute('SELECT * FROM solar_flares WHERE flare_class = ?;', (flare_class,))
            flare_list = cur.fetchall()
            if len(flare_list) < 1:
                conn.close()
                return -2, flare_class
            conn.close()
            return flare_class, flare_list
        
    elif factor == 'region':
        try:
            flare_region = int(input('Enter the flare region you want to search by: '))
        except:
            print()
            print('Try again. Enter an integer.')
            print()
            conn.close()
            return -1

        cur.execute('SELECT * FROM solar_flares WHERE active_region_num = ?;', (flare_region,))
        flare_list = cur.fetchall()
        if len(flare_list) < 1:
            conn.close()
            return -2, flare_region

        conn.close()
        return flare_region, flare_list

    else:
        flare_loc = input('Enter the location of the flare: ')
        flare_loc = flare_loc.upper()

        cur.execute('SELECT * FROM solar_flares WHERE source_location = ?', (flare_loc,))
        flare_list = cur.fetchall()

        if len(flare_list) < 1:
            conn.close()
            return -2, flare_loc

        conn.close()
        return flare_loc, flare_list

# Choice 6
def find_coincidence():
    conn = sqlite3.connect(config.DB_NAME)
    cur = conn.cursor()

    # Taking maximum miss distance as 20,000,000,000 meters, and considering X and M Class solar flares.
    command = """
SELECT asteroids.close_approach_date as coincident_date, asteroids.name, asteroids.potentially_hazardous, asteroids.miss_distance, solar_flares.id, solar_flares.flare_class 
FROM asteroids JOIN solar_flares ON asteroids.close_approach_date = solar_flares.peak_event_date
WHERE (asteroids.potentially_hazardous = 1) AND (asteroids.miss_distance <= 20000000000) AND (solar_flares.flare_class = 'X' OR solar_flares.flare_class = 'M')
ORDER BY asteroids.close_approach_date, solar_flares.flare_class DESC, asteroids.miss_distance, asteroids.name; 
"""
    cur.execute(command)
    data = cur.fetchall()

    if len(data) < 1:
        print()
        print("No potentially hazardous asteroid's close flyby (within 2 x 10^10 meters) coincided with an X-Class or M-Class solar flare.")
        print()
        conn.close()
        return -2

    conn.close()
    return data
