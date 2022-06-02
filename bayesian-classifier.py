import pandas as pd

# 1 = True, 0 = False
# Д = делового характера, М = медицинского характера, Р = развлекательного характера
df = pd.read_excel('bl.xlsx')
print(df)

# Параметры человека, у которого хотим предсказать статус визы
FIELDS = ['Работа', 'Заработок', 'Цель_поездки', 'Английский_язык']
X = [1, 'Средний', 'Д', 1]

approved_count = list(df['Статус']).count('Одобрено')
refused_count = list(df['Статус']).count('Отказано')
approved_p = approved_count / len(df)
refused_p = refused_count / len(df)
print(f'P(Статус=Отказано) = {refused_p}, P(Статус=Одобрено) = {approved_p}')

X_approve_p = 1
X_refuse_p = 1
for param in enumerate(X):
    print(
        f"P({FIELDS[param[0]]}={param[1]} | Статус=Одобрено) = {len(df[(df['Статус'] == 'Одобрено') & (df[FIELDS[param[0]]] == param[1])]) / approved_count}")
    X_approve_p *= len(df[(df['Статус'] == 'Одобрено') & (df[FIELDS[param[0]]] == param[1])]) / approved_count

    print(
        f"P({FIELDS[param[0]]}={param[1]} | Статус=Отказано) = {len(df[(df['Статус'] == 'Отказано') & (df[FIELDS[param[0]]] == param[1])]) / refused_count}")
    X_refuse_p *= len(df[(df['Статус'] == 'Отказано') & (df[FIELDS[param[0]]] == param[1])]) / refused_count

print()
print(f'P(X | Статус=Одобрено) = {X_approve_p}')
print(f'P(X | Статус=Отказано) = {X_refuse_p}')
a = X_approve_p * approved_p
b = X_refuse_p * refused_p
print(f'P(X | Статус=Одобрено) * P(Статус=Одобрено) = {a}')
print(f'P(X | Статус=Отказано) * P(Статус=Отказано) = {b}')

print('Нормализованные значения:')
print(f'Вероятность одобрения {a / (a + b)}')
print(f'Вероятность отказа {b / (b + a)}')
