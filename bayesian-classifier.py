import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB


def Normal(n, mu, var):
    # Функция для возврата pdf нормального (mu, var) значения, вычисленного при x
    sd = np.sqrt(var)
    return (np.e ** (-0.5 * ((n - mu) / sd) ** 2)) / (sd * np.sqrt(2 * np.pi))


def Predict(X):
    Predictions = []

    for i in X.index:  # Цикл по каждому экземпляру

        ClassLikelihood = []
        instance = X.loc[i]
        print(f'\n{instance}')

        for cls in classes:  # Цикл по каждому классу

            FeatureLikelihoods = [np.log(prior[cls])]  # Вероятности появления признаков
            print(cls)
            print(f'log P (C{i}) = {FeatureLikelihoods}')

            for col in x_train.columns:
                data = instance[col]
                print(col, data)

                mean = means[col].loc[cls]  # Найдите среднее значение столбца 'col', которые находятся в классе 'cls'
                variance = var[col].loc[cls]  # Найдите дисперсию столбцов 'col', которые находятся в классе 'cls'

                Likelihood = Normal(data, mean, variance)  # Вероятность
                print(f'log P({col}={data} ∣ C{i}) = {Likelihood}')
                Likelihood = np.log(Likelihood) if Likelihood != 0 else 1 / len(train)
                FeatureLikelihoods.append(Likelihood)

            TotalLikelihood = sum(FeatureLikelihoods)  # апостериорная вероятность
            print(f'log P(C{i} ∣ x) = {TotalLikelihood}')
            ClassLikelihood.append(TotalLikelihood)

        MaxIndex = ClassLikelihood.index(max(ClassLikelihood))  # Наибольшее апостериорное значение
        Prediction = classes[MaxIndex]
        Predictions.append(Prediction)

    return Predictions


def Accuracy(y, prediction):
    # Функция для вычисления точности
    y = list(y)
    prediction = list(prediction)
    score = sum(i == j for i, j in zip(y, prediction))

    return score / len(y)


df = pd.read_excel("iris.xlsx")
df = df.drop("Id", axis=1)
# print(df.to_string())

# Разделение на тестовые данных
train = df.sample(frac=0.2, random_state=1)
test = df.drop(train.index)

y_train = train["Вид"]
x_train = train.drop("Вид", axis=1)

y_test = test["Вид"]
x_test = test.drop("Вид", axis=1)

means = train.groupby(["Вид"]).mean()  # среднее значение каждого класса
var = train.groupby(["Вид"]).var()  # Дисперсия
prior = (train.groupby("Вид").count() / len(train)).iloc[:, 1]  # Априорная вероятность каждого класса
classes = np.unique(train["Вид"].tolist())  # Классы

PredictTrain = Predict(x_train)
PredictTest = Predict(x_test)


clf = GaussianNB()
clf.fit(x_train, y_train)


predicted = clf.predict([[4.8, 3.4, 1.6, 0.2]])  # 0:Overcast, 2:Mild, 1:Normal, 1.True
print("Прогнозируемое значение:", predicted)
