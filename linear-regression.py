import numpy as np
import matplotlib.pyplot as plt
import random
import math

b0 = 0
b1 = 0


def fit(X, Y):
    n = len(X)
    b0 = (sum(Y) * sum(X ** 2) - sum(X) * sum(X * Y)) / (n * sum(X ** 2) - sum(X) ** 2)
    b1 = (n * sum(X * Y) - sum(X) * sum(Y)) / (n * sum(X ** 2) - sum(X) ** 2)
    return b0, b1


def predict(X):
    print(f'{b0} + {b1} * X')
    return b0 + b1 * X


def getCharacteristics(X, Y):
    characteristics = {}
    Y_mean = np.mean(Y)
    X_mean = np.mean(X)
    Y_pred = predict(X)
    n = len(X)
    characteristics['E_sko'] = sum((Y - Y_pred) ** 2) / (len(X) - 2)
    characteristics['E_st'] = math.sqrt(characteristics['E_sko'])
    characteristics['Q'] = sum((Y - Y_mean) ** 2)
    characteristics['Qr'] = sum((Y_pred - Y_mean) ** 2)
    characteristics['Qe'] = sum((Y - Y_pred) ** 2)
    characteristics['det_koef'] = characteristics['Qr'] / characteristics['Q']
    cov = sum((X - X_mean) * (Y - Y_mean)) / n
    sigma_x = math.sqrt(sum((X - X_mean) ** 2) / (n - 1))
    sigma_y = math.sqrt(sum((Y - Y_mean) ** 2) / (n - 1))
    characteristics['kor_koef'] = cov / (sigma_x * sigma_y)

    print(f"Еско = {characteristics['E_sko']}")
    print(f"Ест = {characteristics['E_st']}")
    print(f"Q = {characteristics['Q']}")
    print(f"Qr = {characteristics['Qr']}")
    print(f"Qe = {characteristics['Qe']}")
    print(f"Коэффициент детерминации = {characteristics['det_koef']}")
    print(f"Коэффициент корреляции = {characteristics['kor_koef']}")


def generateData(amount=30):
    def f(x, a, b):
        return a + b * x

    a = random.uniform(-10, +10)
    b = random.uniform(-10, +10)
    X = np.random.permutation(
        [(i + random.uniform(-5, +5)) for i in np.random.uniform(low=-5, high=+5, size=(amount,))])
    Y = []
    for x in X:
        Y.append(f(x, a, b) + random.uniform(-10, +10))
    Y = np.array(Y)
    return X, Y


def plotGraph(X_train, Y_train, X_test, Y_test):
    x_pred = np.arange(-10, +10)
    y_pred = predict(x_pred)
    plt.plot(x_pred, y_pred, color='red', label='regression')
    plt.scatter(X_train, Y_train, label='train', s=3)
    plt.scatter(X_test, Y_test, label='test', s=3)
    plt.legend()
    plt.show()


test_percent = 0.8
X, Y = generateData(100)

train_quantity = int(len(X) * test_percent)
X_train, Y_train = X[:train_quantity], Y[:train_quantity]
X_test, Y_test = X[train_quantity:], Y[train_quantity:]

b0, b1 = fit(X_train, Y_train)
getCharacteristics(X, Y)

plotGraph(X_train, Y_train, X_test, Y_test)
