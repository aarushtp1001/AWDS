# This file contains all the methods that will be used in main.py
import config, fetcher, database
import json, sqlite3

# Menu
def display_menu():
    print()
    print('--------------------------------------------MENU--------------------------------------------')
    print('1. View general space weather statistics using raw data along with a graphical representation.')
    print('2. Search asteroids using speed factor.')
    print('3. Search asteroids using miss-distance factor.')
    print('4. View potentially hazardous asteroids (sorted by miss-distance).')
    print('5. Search solar flares according to class/region.')
    print('6. Find all potentially hazardous asteroids that happened to pass by close to Earth when a dangerous (X-Class) solar flare occurred.')
    print('7. Exit.')
    print()

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
    # Settings default values.
    general_stats['flare_class_data']['A'] = 0
    general_stats['flare_class_data']['B'] = 0
    general_stats['flare_class_data']['C'] = 0
    general_stats['flare_class_data']['M'] = 0
    general_stats['flare_class_data']['X'] = 0
    for flare in returned_flare_class_data:
        general_stats['flare_class_data'][flare[0]] = flare[1]

    cur.execute('''SELECT active_region_num, COUNT(*) as freq FROM solar_flares
                   GROUP BY active_region_num ORDER BY freq DESC LIMIT 1;''')
    most_active_region = cur.fetchone()
    general_stats['most_active_region'] = dict()
    general_stats['most_active_region']['region_num'] = most_active_region[0]
    general_stats['most_active_region']['frequency'] = most_active_region[1]
    
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

    return general_stats

# Choice 2
def search_asteroids_by_speed():
    conn = sqlite3.connect(config.DB_NAME)
    cur = conn.cursor()

    try: 
        q = int(input('Would you like to search by minimum velocity or by maximum velocity (1 for minimum, 2 for maximum)? '))
        print()
    except: 
        print('Bad input, please run the program again.')
        print()
        return -1

    if q == 1:
        min_velo = float(input('Enter the minimum velocity in m/s by which you want to search asteroids: '))
        print()
        cur.execute('SELECT * FROM asteroids WHERE relative_velocity >= ?;', (min_velo,))
        asteroid_list = cur.fetchall()

        if len(asteroid_list) < 1:
            print(f'No asteroid was found to have greater velocity than or equal to {min_velo} m/s.')
            print()
            return -1

        return 'min', min_velo, asteroid_list
            
    elif q == 2:
        max_velo = float(input('Enter the maximum velocity in m/s by which you want to search asteroids: '))
        print()
        cur.execute('SELECT * FROM asteroids WHERE relative_velocity <= ?;', (max_velo,))
        asteroid_list = cur.fetchall()
        
        if len(asteroid_list) < 1:
            print(f'No asteroid was found to have lesser velocity than or equal to {max_velo} m/s.')
            print()
            return -1
        
        return 'max', max_velo, asteroid_list 
            
    else:
        print('Enter either 1 or 2. Please try again...')
        print()
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
        return -1

    if q == 1:
        min_dist = float(input('Enter the minimum distance in meters by which you want to search asteroids: '))
        print()
        cur.execute('SELECT * FROM asteroids WHERE miss_distance >= ?;', (min_dist,))
        asteroid_list = cur.fetchall()

        if len(asteroid_list) < 1:
            print(f'No asteroid was found to have greater miss distance than or equal to {min_dist} m/s.')
            print()
            return -1

        return 'min', min_dist, asteroid_list 
            
    elif q == 2:
        max_dist = float(input('Enter the maximum distance in meters by which you want to search asteroids: '))
        print()
        cur.execute('SELECT * FROM asteroids WHERE miss_distance <= ?;', (max_dist,))
        asteroid_list = cur.fetchall()

        if len(asteroid_list) < 1:
            print(f'No asteroid was found to have lesser miss distance than or equal to {max_dist} m/s.')
            print()
            return -1

        return 'max', max_dist, asteroid_list

    else:
        print('Enter either 1 or 2. Please try again...')
        print()
        return -1
