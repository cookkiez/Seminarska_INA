import random
import haversine as hs
import googlemaps
from time import sleep
from pprint import pprint
import pandas as pd
import math
import numpy as np
import json


def get_input_data(filename):
    with open(filename, "r") as f:
        return json.load(f)


def download():
    # insert your google developer api key here. Do this on the google developer platform,
    # find the instructions how to do this on the internet. You will also have to enable billing
    # and the api for your account
    api_key = "key"
    gmaps = googlemaps.Client(key=api_key)

    origin_ids = list(range(983))
    destination_ids = list(range(983))
    data = get_input_data("nodes_data.json")
    to_print = []
    for _ in range(50):
        # getting the coordinates and putting them in lists
        origins = []
        destinations = []
        try:
            dest_ind = random.sample(destination_ids, 25)
            origin_ind = random.sample(origin_ids, 25)
            print(len(set(dest_ind)), len(set(origin_ind)))
        
            for i in dest_ind:
                lng, lat = data[i]["geo_loc"]
                destinations.append((lat, lng))
                destination_ids.remove(i)

            for i in origin_ind:
                lng, lat = data[i]["geo_loc"]
                origins.append((lat, lng))
                origin_ids.remove(i)

            """
            print("**** Origins")
            pprint(origins)
            print("**** Destinations")
            pprint(destinations)
            """

            """ TEST
            res = gmaps.distance_matrix(origins[0], destinations, mode="driving")
            pprint(res)"""

            for loc in origins:
                res = gmaps.distance_matrix(loc, destinations, mode="driving")
                pprint(res)
                results = res["rows"][0]["elements"]
                x1, y1 = loc
                for i, (x2, y2) in enumerate(destinations):
                    curr_dist_google = int(math.floor(int(results[i]["distance"]["value"]) / 1000))
                    curr_dur_google = results[i]["duration"]["value"] / 3600
                    to_print.append([x1, y1, x2, y2, hs.haversine((x1, y1), (x2, y2)), curr_dist_google, curr_dur_google]) 
            
            sleep(0.5)
        
        except:
            print("Zmanjkal podatkov!!")
            pass
        

    # Write to file
    df = pd.DataFrame(data=to_print, columns=["x1", "y1", "x2", "y2", "aerial",
                                              "google_distance", "google_time"])
    df.to_csv("learning_data_all.csv", index=False)


if __name__ == "__main__":
    download()
