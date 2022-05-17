from pprint import pprint

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import networkx as nx
import construct_graphs


def predict_with_shortest_path(n1, n2, G):
    """
    Predict time of travel between two nodes, that we do not have data for
    :param n1: node a
    :param n2: node b
    :param G: Graph with nodes a and b
    :return: time of travel between a and b
    """
    path = nx.shortest_path(G, source=n1, target=n2, weight="weight")
    travel_time = 0
    prev = path[0]
    print(path)
    for node in path[1:]:
        travel_time += G[prev][node]["weight"]
        prev = node
    return travel_time


def check_bfs(neigh, G, visited_curr, visited_opposite, queue):
    curr_path = visited_curr[neigh]["path"]
    if neigh in visited_opposite:
        """ 
        # Test prints
        pprint(visited_curr)
        pprint(visited_opposite)
        """
        visited_opposite[neigh]["path"].reverse()
        curr_path.extend(visited_opposite[neigh]["path"][1:])
        print(f'First joint on node: {neigh}, with path: {curr_path}')
        return visited_curr[neigh]["weight"] + visited_opposite[neigh]["weight"]

    for n, metadata in sorted(G[neigh].items(), key=lambda edge: edge[1]['weight']):
        if n not in visited_curr:
            queue.append(n)
            p = curr_path.copy()
            p.append(n)
            visited_curr[n] = {
                "weight": visited_curr[neigh]["weight"] + metadata["weight"],
                "path": p
            }

    return None


def bfs_first_joint(n1, n2, G):
    """
    Do BFS over graph from n1 to n2 and n2 to n1 at the same time.
    Take first common neighbor of n1 and n2, n3. Return travel time = n1-n3 + n2-n3
    :param n1: node a
    :param n2: node b
    :param G: Graph with nodes a and b
    :return: time of travel between a and b
    """
    visited1 = {n1: {"weight": 0, "path": [n1]}}
    visited2 = {n2: {"weight": 0, "path": [n2]}}
    queue1 = [n1]
    queue2 = [n2]
    while queue1 and queue2:
        travel_time = check_bfs(queue1.pop(0), G, visited_curr=visited1, visited_opposite=visited2, queue=queue1)
        if travel_time:
            return travel_time

        travel_time = check_bfs(queue2.pop(0), G, visited_curr=visited2, visited_opposite=visited1, queue=queue2)
        if travel_time:
            return travel_time

    return None


def test_bfs():
    G_temp_morning = construct_graphs.temporal_graph(0)
    # (45, 230) - BFS finds path of length 4: [230, 980, 136, 45]
    # (669, 439), (610, 699)  BFS finds that they are neighbors
    # -> for all, shortest path finds better path
    n1, n2 = 45, 230  # (669, 439)  # (610, 699)
    print((n1, n2))
    print(bfs_first_joint(n1, n2, G_temp_morning))
    print(predict_with_shortest_path(n1, n2, G_temp_morning))


def model_train_rmse(model, train_x, train_y, test_x, test_y):
    """
    Train the given model on the given train and test data. After training, use the test set to
    predict new values and compare them to the real test set. Calculate RMSE and return the
    predicted values with RMSE. We want to use X data to predict Y data.

    :param model: instance of model eg. LinearRegression()
    :param train_x: training set of X class
    :param train_y: training set of Y class
    :param test_x: test set of X class
    :param test_y: test set of Y class.
    :return a tuple of
        - predicts: the predicted values stored in a list
        - rmse: RMSE value calculated for this model
    """
    model.fit(train_x, train_y.ravel())
    predicts = model.predict(test_x)
    rmse = np.sqrt(mean_squared_error(test_y, predicts))
    print("For model:", str(model), "RMSE:", rmse, "Score:", model.score(test_x, test_y))
    return predicts, rmse


def do_model():
    df = pd.read_csv("learning_data_all.csv")
    # df = pd.read_csv("edges_data_0.json")
    google_time = df.google_time.values.reshape(-1, 1)
    print(google_time)

    features = ["aerial", "x1", "x2", "y1", "y2"]
    X = df.loc[:, features].values
    X_train, X_test, time_train, time_test = train_test_split(X, google_time,
                                                              test_size=0.30,
                                                              random_state=42)

    rfr = RandomForestRegressor()
    predicts_rfr, rmse_rfr = model_train_rmse(rfr, X_train, time_train, X_test, time_test)
    br = GradientBoostingRegressor()
    predicts_br, rmse_br = model_train_rmse(br, X_train, time_train, X_test, time_test)

    fig, ax = plt.subplots()
    ax.set_ylabel("Travel time (predicted)")
    ax.set_xlabel("Travel time (by google maps)")
    ax.scatter(x=time_test, y=predicts_br, c="b", alpha=0.5)
    ax.scatter(x=time_test, y=predicts_rfr, c="r", alpha=0.5)

    # For diagonal (optimal value)
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),
        np.max([ax.get_xlim(), ax.get_ylim()]),
    ]
    ax.plot(lims, lims, alpha=0.5, c="black")

    ax.set_title(f"Random forest regressor (red, RMSE={rmse_rfr:.3f}),\n "
                 f"Gradient boosting (blue, RMSE={rmse_br:.3f})")

    plt.savefig("learning_time.png")
    plt.show()


if __name__ == "__main__":
    # do_model()
    test_bfs()
