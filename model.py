from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


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
    google_time = df.google_time.values.reshape(-1, 1)

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
    do_model()
