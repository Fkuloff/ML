import numpy as np
import matplotlib.pyplot as plt
import random
import math


class LinearRegression:
    a = 0
    b = 0

    def fit(self, X, Y):
        n = len(X)
        self.a = (sum(Y) * sum(X ** 2) - sum(X) * sum(X * Y)) / (n * sum(X ** 2) - sum(X) ** 2)
        self.b = (n * sum(X * Y) - sum(X) * sum(Y)) / (n * sum(X ** 2) - sum(X) ** 2)

    def predict(self, X):
        return self.a + self.b * X

    def getCharacteristics(self, X, Y):
        characteristics = {}
        Y_mean = np.mean(Y)
        X_mean = np.mean(X)
        Y_pred = self.predict(X)
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
        return characteristics


def generateData(amount=30):
    def f(x, a, b):
        return a + b * x

    a = random.uniform(-10, +10)
    b = random.uniform(-10, +10)
    X = np.random.permutation(
        [(i + random.uniform(-5, +5)) for i in np.random.uniform(low=-10, high=+10, size=(amount,))])
    Y = []
    for x in X:
        Y.append(f(x, a, b) + random.uniform(-10, +10))
    Y = np.array(Y)
    return (X, Y)


def plotGraph(lr, X_train, Y_train, X_test, Y_test):
    x_pred = np.arange(-20, +20)
    y_pred = lr.predict(x_pred)
    plt.plot(x_pred, y_pred, color='red', label='regression')
    plt.scatter(X_train, Y_train, label='train', s=3)
    plt.scatter(X_test, Y_test, label='test', s=3)
    plt.legend()
    plt.show()


test_percent = 0.8
X, Y = generateData(500)

train_quantity = int(len(X) * test_percent)
X_train, Y_train = X[:train_quantity], Y[:train_quantity]
X_test, Y_test = X[train_quantity:], Y[train_quantity:]
# print(X_train, Y_train)

lr = LinearRegression()
lr.fit(X_train, Y_train)
characteristics = lr.getCharacteristics(X, Y)

print(f"Еско = {characteristics['E_sko']}")
print(f"Ест = {characteristics['E_st']}")
print(f"Q = {characteristics['Q']}")
print(f"Qr = {characteristics['Qr']}")
print(f"Qe = {characteristics['Qe']}")
print(f"Коэффициент детерминации = {characteristics['det_koef']}")
print(f"Коэффициент корреляции = {characteristics['kor_koef']}")

plotGraph(lr, X_train, Y_train, X_test, Y_test)
