## main.py --> A menu-driven user interface for the Astronomical Weather application.
import config, fetcher, database
import json, sqlite3
import functions

conn = sqlite3.connect(config.DB_NAME)
cur = conn.cursor()

print('Welcome to the Astronomical Weather Database System!')
print()

print('We need to populate the database first.')
print()

# '2026-08-01', '2026-08-03', '2026-06-20', '2026-07-10'
asteroid_start_date = input('Enter the beginning date from where you want to start searching for asteroids from: ')
asteroid_end_date = input('Enter the ending date from where you want to start searching for asteroids from: ')
flare_start_date = input('Enter the beginning date from where you want to start searching for solar flares from: ')
flare_end_date = input('Enter the ending date from where you want to start searching for solar flares from: ')

# Some default values for quick testing...
if not len(asteroid_start_date):
    asteroid_start_date = '2026-08-01'
    asteroid_end_date = '2026-08-03'
    flare_start_date = '2026-06-20'
    flare_end_date = '2026-07-10'
    
print()

proceed = True
print('Populating database...')
try:
    database.init_db(asteroid_start_date, asteroid_end_date, flare_start_date, flare_end_date)
    print('The Astronomical Weather Database has been successfully created!')
    print()
except:
    print('Error has occurred! Exiting program now...')
    proceed = False

while proceed == True:
    functions.display_menu()

    try:
        ch = int(input('Enter your choice: '))
        print()
    except:
        print()
        print('Bad input: enter an integer.')
        print()
        continue

    if ch == 1:
        stats = functions.display_general_stats()
        print('The created dictionary is:')
        print(stats)


    elif ch == 2:
        returned_velo = functions.search_asteroids_by_speed()

        if returned_velo == -1:
            continue

        if returned_velo[0] == 'min':
            print(f'        The following asteroids were found to have greater velocity than or equal to {returned_velo[1]} m/s:')
            print('FORMAT: (id, name, min_diameter, max_diameter, potentially_hazardous, close_approach_date, relative_velocity, miss_distance)')
            print()
            for record in returned_velo[2]:
                print(record)
            print()


        elif returned_velo[0] == 'max':
            print(f'        The following asteroids were found to have lesser velocity than or equal to {returned_velo[1]} m/s:')
            print('FORMAT: (id, name, min_diameter, max_diameter, potentially_hazardous, close_approach_date, relative_velocity, miss_distance)')
            print()
            for record in returned_velo[2]:
                print(record)
            print()


    elif ch == 3:
        returned_dist = functions.search_asteroids_by_miss_dist()

        if returned_dist == -1:
            continue

        if returned_dist[0] == 'min':
            print(f'        The following asteroids were found to have greater miss distance than or equal to {returned_dist[1]} m/s:')
            print('FORMAT: (id, name, min_diameter, max_diameter, potentially_hazardous, close_approach_date, relative_velocity, miss_distance)')
            print()
            for record in returned_dist[2]:
                print(record)
            print()

        elif returned_dist[0] == 'max':
            print(f'        The following asteroids were found to have lesser miss distance than or equal to {returned_dist[1]} m/s:')
            print('FORMAT: (id, name, min_diameter, max_diameter, potentially_hazardous, close_approach_date, relative_velocity, miss_distance)')
            print()
            for record in returned_dist[2]:
                print(record)
            print()


    elif ch == 4:
        functions.view_pot_hazardous_asteroids()


    elif ch == 5:
        q = input('Would you like to search for solar flares using class, region, or location (default --> class)? ')

        if (q.lower() == 'class') or (q == ''):
            returned_data = functions.search_flares()
            if returned_data == -1:
                continue
            elif returned_data[0] == -2:
                if (not returned_data[1].isalpha()) or (returned_data[1] not in 'ABCMX'):
                    print(f'{returned_data[1]} is not a valid solar flare class.')
                    continue
                print(f'No solar flares of {returned_data[1]} Class were found.')
                print()
                continue
            print(f'        The following flares were found to be of {returned_data[0]} Class:')
            print('FORMAT: (id, begin_time, begin_event_date, peak_time, peak_event_date, end_time, end_event_date, flare_magnitude, flare_class, source_location, active_region_num)')
            print()
            for flare in returned_data[1]:
                print(flare)
            print()

        elif q.lower() == 'region':
            returned_data = functions.search_flares('region')
            if returned_data == -1:
                continue
            elif returned_data[0] == -2:
                print(f'No solar flares from the Active Region Number {returned_data[1]} were found.')
                print()
                continue
            print(f'        The following flares were found to be of Active Region Number {returned_data[0]}:')
            print('FORMAT: (id, begin_time, begin_event_date, peak_time, peak_event_date, end_time, end_event_date, flare_magnitude, flare_class, source_location, active_region_num)')
            print()
            for flare in returned_data[1]:
                print(flare)
            print()

        elif q.lower() == 'location':
            returned_data = functions.search_flares('location')
            if returned_data[0] == -2:
                print(f'No solar flares from the location {returned_data[1]} were found.')
                print()
                continue
            print(f'        The following flares were found to be of Source Location {returned_data[0]}:')
            print('FORMAT: (id, begin_time, begin_event_date, peak_time, peak_event_date, end_time, end_event_date, flare_magnitude, flare_class, source_location, active_region_num)')
            print()
            for flare in returned_data[1]:
                print(flare)
            print()

        else:
            print()
            print('Invalid option, try again.')
            print()
            continue


    elif ch == 7:
        print('Thank you for using the Astronomical Weather Database System!')
        print('Now exiting...')
        break


    else:
        print('Invalid input, please try again...')
        print()
