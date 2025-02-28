import io
import pandas as pd
import requests
import json
import os
from datetime import datetime
import time
import re
from datetime import datetime, timedelta
from datetime import date
import numpy as np
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Data from NASA API
    """
    asteroid_list = []

    url = "https://api.nasa.gov/neo/rest/v1/feed?"

    current_date = date.today()
    start_date = current_date
    end_date = start_date
    # start_date= '2025-02-21'
    # start_date = datetime.strptime(start_date, '%Y-%m-%d')
    # end_date = start_date + timedelta(days = 5)

    parameters = {
        "start_date" : start_date,
        "end_date" : end_date,
        "api_key": get_secret_value('nasa_key')
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"}

    response = requests.get(url, params=parameters, headers = headers)
    if response.status_code == 200:
        data = response.json()
        filtered_data  = data['near_earth_objects']
        asteroid_list.append(filtered_data)
    else:
        # Si la requête échoue, on retourne un message d'erreur avec le code de statut
        print(f"Error {response.status_code}: {response.json().get('message', 'Unknown error')}")
    
    time.sleep(7)

    asteroid_dict = {}
    empty_dict = {}
    final_dict = {} # il ne peut pas avoir le même nom de clé, on ne peut pas mettre la date

    count = 0

    # Première boucle : range de i = le nombre de boucles 
    for i in range(0, len(asteroid_list)):
        asteroid_dict[i] = asteroid_list[i]
        # Deuxième boucle : k = la date
        for k, v in asteroid_dict[i].items(): 
            empty_dict[k] = asteroid_dict[i][k]

    # Troisième boucle : pour récupérer les infos asteroides à l'intérieure de chaque date
    # pour une date il y a en moyenne entre 10-15 asteroides
    for k, v in empty_dict.items(): 
        for m in range(0, len(empty_dict[k])):
            count += 1 
            try: 
                final_dict[count] = {
                    'date': k, 
                    'id' : empty_dict[k][m]['id'],
                    'name': empty_dict[k][m]['name'],
                    'absolute_magnitude_h': empty_dict[k][m]['absolute_magnitude_h'], 
                    'estimated_diameter_min_meters' : empty_dict[k][m]['estimated_diameter']['meters']['estimated_diameter_min'],
                    'estimated_diameter_max_meters' : empty_dict[k][m]['estimated_diameter']['meters']['estimated_diameter_max'], 
                    'is_potentially_hazardous_asteroid' : empty_dict[k][m]['is_potentially_hazardous_asteroid'], 
                    'is_sentry_object' : empty_dict[k][m]['is_sentry_object'],
                    'close_approach_date': empty_dict[k][m]['close_approach_data'][0]['close_approach_date'], 
                    'close_approach_date_full': empty_dict[k][m]['close_approach_data'][0]['close_approach_date_full'],
                    'relative_velocity_km_per_second': empty_dict[k][m]['close_approach_data'][0]['relative_velocity']['kilometers_per_second'],
                    'relative_velocity_km_per_hour' : empty_dict[k][m]['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'], 
                    'miss_distance_kilometers' : empty_dict[k][m]['close_approach_data'][0]['miss_distance']['kilometers'], 
                    'orbiting_body' : empty_dict[k][m]['close_approach_data'][0]['orbiting_body']
                            }

            except: 
                continue

    df1 = pd.DataFrame.from_dict(final_dict, orient='index').reset_index(drop=True)
    
    print(df1.shape)

    return df1


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
