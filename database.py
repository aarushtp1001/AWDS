import sqlite3
import config, fetcher

def init_db(start_date_asteroid, end_date_asteroid, start_date_flare, end_date_flare):
    asteroid_list = fetcher.asteroid_data_fetcher(start_date_asteroid, end_date_asteroid)
    flare_list = fetcher.solar_data_fetcher(start_date_flare, end_date_flare)

    # print(flare_list)

    if flare_list and asteroid_list:  
        conn = sqlite3.connect(config.DB_NAME)
        cur = conn.cursor()

        command = '''
DROP TABLE IF EXISTS asteroids;
DROP TABLE IF EXISTS solar_flares;

CREATE TABLE asteroids(
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT,
    min_diameter REAL,
    max_diameter REAL,
    potentially_hazardous INTEGER,
    close_approach_date TEXT,
    relative_velocity REAL,
    miss_distance REAL
);

CREATE TABLE solar_flares(
    id TEXT PRIMARY KEY NOT NULL,
    begin_time TEXT,
    begin_event_date TEXT,
    peak_time TEXT,
    peak_event_date TEXT,
    end_time TEXT,
    end_event_date TEXT,
    flare_magnitude TEXT,
    flare_class TEXT,
    source_location TEXT,
    active_region_num INTEGER
);'''

        cur.executescript(command)
        conn.commit()

        # asteroid_list = fetcher.asteroid_data_fetcher(start_date_asteroid, end_date_asteroid)
        # flare_list = fetcher.solar_data_fetcher(start_date_flare, end_date_flare)

        ## adding data to asteroids table
        for asteroid in asteroid_list:
            id = asteroid[0]
            name = asteroid[1]
            min_diameter = asteroid[2]
            max_diameter = asteroid[3]
            potentially_hazardous = asteroid[4]
            close_approach_date = asteroid[5]
            relative_velocity = asteroid[6]
            miss_distance = asteroid[7]

            # REPLACE is used in order to account for the possibility if NASA corrects its data later.
            cur.execute('''
        INSERT OR REPLACE INTO asteroids(id, name, min_diameter, 
                                         max_diameter, potentially_hazardous, close_approach_date, 
                                         relative_velocity, miss_distance) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ;''', (id, name, min_diameter, max_diameter, potentially_hazardous, close_approach_date, relative_velocity, miss_distance))
            # '?' to prevent SQL injection

        conn.commit()

        ## adding data to solar_flares table
        for flare in flare_list:
            id = flare[0]
            begin_time = flare[1]
            begin_event_date = flare[2]
            peak_time = flare[3]
            peak_event_date = flare[4]
            end_time = flare[5]
            end_event_date = flare[6]
            flare_magnitude = flare[7]
            flare_class = flare[7][0]
            source_location = flare[8]
            active_region_num = flare[9]

            # REPLACE is used in order to account for the possibility if NASA corrects its data later.
            cur.execute('''INSERT OR REPLACE INTO solar_flares(id, begin_time, begin_event_date, 
                                                           peak_time, peak_event_date, end_time, 
                                                           end_event_date, flare_magnitude, flare_class,
                                                           source_location, active_region_num) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ;''', (id, begin_time, begin_event_date, peak_time, peak_event_date, end_time, end_event_date, flare_magnitude, flare_class, source_location, active_region_num))

        conn.commit()
        conn.close()
        print('Both tables were created successfully!')

        proceed = True

    else:
        print('NASA\'s NeoWs/DONKI API returned a 503 Error, i.e., either of their servers are currently down. Please try again after a few hours')
        proceed = False
        
