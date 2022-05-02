import pandas as pd
import geojson
from pprint import pprint
import json
import pickle


def read_from_csv(filename="london-lsoa-2020-1-All-HourlyAggregate.csv",
                  geojson_filename="london_lsoa.json"):
    """
    Function takes the file, reads its data and processes it into a format that we need.
    :param filename: Name of the file to read data from
    :param geojson_filename: Name of the file to read geo data from
    :return:
    """
    df = pd.read_csv(filename)

    # Remove data we don't need
    df.drop('standard_deviation_travel_time', inplace=True, axis=1)
    df.drop('geometric_standard_deviation_travel_time', inplace=True, axis=1)
    df.drop('geometric_mean_travel_time', inplace=True, axis=1)

    # Separate the data into different time chunks (as defined below)
    """
        6-10 morning rush
        10-14 mid-day
        14-18 evening rush
        18-6 (next day) non-rush -> this is in one dataframe
    """
    df_midnight_five = df[df["hod"] < 6]
    df_copy = df.drop(df_midnight_five.index.values)
    df_morning_rush = df_copy[df_copy["hod"] < 10]
    df_copy = df_copy.drop(df_morning_rush.index.values)
    df_mid_day = df_copy[df_copy["hod"] < 14]
    df_copy = df_copy.drop(df_mid_day.index.values)
    df_afternoon_rush = df_copy[df_copy["hod"] < 18]
    df_copy = df_copy.drop(df_afternoon_rush.index.values)
    df_six_midnight = df_copy.copy()
    df_copy = df_copy.drop(df_six_midnight.index.values)
    df_night = pd.concat([df_midnight_five, df_six_midnight])

    # Read geo data from the json file
    with open(geojson_filename) as f:
        geo_data = geojson.load(f)
    # pprint(geo_data["features"][1])

    # Save geo data from the json file
    nodes_data = []
    for district in geo_data["features"]:
        properties = district["properties"]
        coordinates = district["geometry"]["coordinates"][0][0]
        # Take average geo location of district
        sum_x = 0
        sum_y = 0
        for [x, y] in coordinates:
            sum_x += x
            sum_y += y
        # There is some more data we can save, but I am not really sure what it means
        nodes_data.append({
            "display_name": properties["DISPLAY_NAME"],
            "node_id": properties["MOVEMENT_ID"],
            "geo_loc": [sum_x / len(coordinates), sum_y / len(coordinates)]
        })

    # Convert data frames into lists, so they take less space and only convey information that we need
    edges = []
    for cnt, df_e in enumerate([df_morning_rush, df_mid_day, df_afternoon_rush, df_night]):
        df_e.drop('hod', inplace=True, axis=1)

        print(f"Iterating data in interval: {cnt}")
        to_print = []
        visited = {}
        for [i, j, mtt] in df_e.values.tolist():
            if f"{i},{j}" not in visited:
                visited[f"{i},{j}"] = [mtt]
            else:
                visited[f"{i},{j}"].append(mtt)

        for key in visited:
            i, j = [float(x) for x in key.split(",")]
            vals = visited[key]
            to_print.append([int(i), int(j), sum(vals)/len(vals)])

        # The last interval is very large, so we split it into three parts, so the files can be stored on github
        """if cnt == 3:
            mod = int(len(to_print) / 3)
            t = []
            for i, el in enumerate(to_print):
                t.append(el)
                # If condition is (i + 1) % mod == 0, then we will get one small file with 1-3 edges in it and we don't
                # want that
                if (i + 1) % (mod + 3) == 0:
                    edges.append(t)
                    t = []
            edges.append(t)
        else:"""
        edges.append(to_print)

    dict_to_save = {
        "nodes": nodes_data,
        "edges": edges
    }
    # Write data to json files, with formating for easier reading
    with open('nodes_data.json', 'w') as handle:
        json.dump(dict_to_save["nodes"], handle, indent=2)

    for i, e in enumerate(dict_to_save["edges"]):
        with open(f'edges_data_{i}.json', 'w') as handle:
            # parsed = json.loads(str(e))
            json.dump(e, handle)  # , indent=2)


if __name__ == "__main__":
    read_from_csv()
