import pandas as pd
import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class LogisticRegression:
    def __init__(self):
        self.w = np.random.randn(n, 1) * 0.001
        self.b = np.random.randn() * 0.001

    def train(self, X, y, learning_rate=0.005, epochs=50):
        for _ in range(epochs):
            dw = np.zeros((n, 1))
            db = 0

            for i in range(len(X)):
                z = X[i].reshape(1, n).dot(self.w) + self.b
                a = sigmoid(z)[0][0]

                dw += (a - y[i]) * X[i].reshape(n, 1)
                db += (a - y[i])

            dw /= len(X)
            db /= len(X)

            self.w = self.w - learning_rate * dw
            self.b = self.b - learning_rate * db

    def predict(self, X):
        return np.array([sigmoid(x.reshape(1, n).dot(self.w) + self.b)[0][0] for x in X])


df = pd.read_excel('dataset_small.xlsx')
print(df)
table = df.to_numpy()
X = table[:, 0]
Y = table[:, 1]
n = 1

logic = LogisticRegression()
logic.train(X, Y)

event = np.array([50])
predict_event = logic.predict(event)
print(f'\np = {predict_event}')
print(f'Шанс -> O = {predict_event} / 1 - {predict_event} = {predict_event / (1 - predict_event)}')
a = predict_event / (1 - predict_event)
b = (1 - predict_event) / predict_event
OR = a / b
print(
    f'Отношение шансов, или отношение несогласия -> OR ({predict_event} / 1 - {predict_event}) / ((1 - {predict_event}) / {predict_event}) = {OR}')
train_prediction = np.array(logic.predict(X))
train_accuracy = np.sum((train_prediction > 0.5) == Y) / len(train_prediction)
print(
    f'Стандартную ошибку отношения шансов -> Eст(OR) = ({np.sum((train_prediction > 0.5) == Y)} / {len(train_prediction)}) * {OR} = {train_accuracy * OR}')
print(f'Точность на тестовой выборке: {round(train_accuracy * 100, 2)}%')
print(f'Относительный риск = {predict_event} / (1 - {predict_event}) {predict_event / (1 - predict_event)}')
