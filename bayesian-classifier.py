import pandas as pd

df = pd.read_excel('bl.xlsx')
print(df.to_string())

FIELDS = ['Опыт_разработки', 'Уровень_знаний', 'Претендуемая_позиция', 'Английский_язык']
X = [1, 'Средний', 'Д', 1]

approved_count = list(df['Статус']).count('Одобрено')
refused_count = list(df['Статус']).count('Отказано')
approved_p = approved_count / len(df)
refused_p = refused_count / len(df)
print(f'\nP(Статус=Отказано) = {round(refused_p, 3)}, P(Статус=Одобрено) = {round(approved_p, 3)}')

X_approve_p = 1
X_refuse_p = 1
for param in enumerate(X):
    print(
        f"P({FIELDS[param[0]]}={param[1]} | Статус=Одобрено) ="
        f" {round(len(df[(df['Статус'] == 'Одобрено') & (df[FIELDS[param[0]]] == param[1])]) / approved_count, 3)}"
    )
    X_approve_p *= len(df[(df['Статус'] == 'Одобрено') & (df[FIELDS[param[0]]] == param[1])]) / approved_count

    print(
        f"P({FIELDS[param[0]]}={param[1]} | Статус=Отказано) ="
        f" {round(len(df[(df['Статус'] == 'Отказано') & (df[FIELDS[param[0]]] == param[1])]) / refused_count, 3)}"
    )
    X_refuse_p *= len(df[(df['Статус'] == 'Отказано') & (df[FIELDS[param[0]]] == param[1])]) / refused_count

print(f'\nP(X | Статус=Одобрено) = {round(X_approve_p, 3)}')
print(f'P(X | Статус=Отказано) = {round(X_refuse_p, 3)}')
a = X_approve_p * approved_p
b = X_refuse_p * refused_p
print(f'P(X | Статус=Одобрено) * P(Статус=Одобрено) = {round(a, 3)}')
print(f'P(X | Статус=Отказано) * P(Статус=Отказано) = {round(b, 3)}')

print('Нормализованные значения:')
print(f'Вероятность одобрения {round(a / (a + b), 3)}')
print(f'Вероятность отказа {round(b / (b + a), 3)}')
