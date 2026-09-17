import config
import json
import urllib.request, urllib.parse, urllib.error

def asteroid_data_fetcher(start_date, end_date):
    parms = {'start_date':start_date, 'end_date':end_date, 'api_key':config.NASA_API_KEY}
    base_url = config.NEOWS_BASE_URL
    full_url = base_url + '?' +  urllib.parse.urlencode(parms)

    try: 
        f = urllib.request.urlopen(full_url)
        full_data = f.read().decode()
        dict_data = json.loads(full_data)
    except: 
        return [] 
    
    ## id (primary key), name, min diameter, max diameter, potentially hazardous, close approach date, relative velocity, miss distance
    req_data = dict_data.get("near_earth_objects", {}) # Returns empty dict in case no NEO was found.
    final_data = []
    for date in req_data:
        for asteroid in req_data[date]:
            # The following variables are almost always present in NASA data.
            id = asteroid['id'] # string
            name = asteroid['name']
            min_diameter = asteroid['estimated_diameter']['meters']['estimated_diameter_min'] ## float
            max_diameter = asteroid['estimated_diameter']['meters']['estimated_diameter_max']
            potentially_hazardous = int(asteroid['is_potentially_hazardous_asteroid']) # Converted to int to save space in database.

            # The following variables are sometimes missing in NASA data, hence the try-except.
            try: close_approach_date = asteroid['close_approach_data'][0]['close_approach_date'] ## string
            except: close_approach_date = None ## cleanly maps out to NULL in SQLite

            try: relative_velocity = float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']) / 3.6 # Converted to meter/second.
            except: relative_velocity = None

            try: miss_distance = float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']) * 1000 # Converted to metres.
            except: miss_distance = None

            final_data.append([id, name, min_diameter, 
                               max_diameter, potentially_hazardous, close_approach_date, 
                               relative_velocity, miss_distance])

    return final_data

def solar_data_fetcher(start_date, end_date):
    parms = {'startDate':start_date, 'endDate':end_date, 'api_key':config.NASA_API_KEY}
    base_url = config.DONKI_BASE_URL
    full_url = base_url + '?' +  urllib.parse.urlencode(parms)

    try:
        f = urllib.request.urlopen(full_url)
        full_data = f.read().decode()
        dict_data = json.loads(full_data)
    except:
        return []

    ## flrID (primary key), beginTime, peakTime, endTime, classType, sourceLocation, activeRegionNum
    final_data = []
    for flare in dict_data:
        id = flare['flrID'] ## string, guaranteed to be present in the JSON

        # The following variables are sometimes missing in NASA data, hence the try-except.
        try: 
            begin_time = flare['beginTime']
            begin_event_date = begin_time[:10]
        except: 
            begin_time = None
            begin_event_date = None

        try: 
            peak_time = flare['peakTime']
            peak_event_date = peak_time[:10]
        except: 
            peak_time = None
            peak_event_date = None

        try: 
            end_time = flare['endTime']
            end_event_date = end_time[:10]
        except: 
            end_time = None
            end_event_date = None

        try: class_type = flare['classType']
        except: class_type = None

        try: source_location = flare['sourceLocation'] ## string representing location of flare using latitudes and longitudes
        except: source_location = None

        try: active_region_num = flare['activeRegionNum'] ## integer representing sunspot group
        except: active_region_num = None

        final_data.append([id, begin_time, begin_event_date, 
                           peak_time, peak_event_date, end_time, 
                           end_event_date, class_type, source_location, 
                           active_region_num])

    return final_data
