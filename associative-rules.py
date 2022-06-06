from copy import copy
from itertools import combinations

import pandas as pd

F1 = ["Toyota", "Mercedes", "BMW", "Honda", "Volkswagen", "Ford", "Hyundai"]
trSubjectSets = {
    1: ["BMW", "Volkswagen", "Honda"],
    2: ["Toyota", "Ford", "Honda"],
    3: ["Honda", "Hyundai", "Mercedes", "Ford"],
    4: ["Volkswagen", "Honda", "Hyundai", "Mercedes"],
    5: ["Mercedes", "Toyota", "BMW"],
    6: ["Ford", "Toyota", "Mercedes", "Hyundai"],
    7: ["Hyundai", "Honda"],
    8: ["BMW", "Hyundai", "Volkswagen"],
    9: ["Ford", "Toyota", "Mercedes"],
    10: ["Mercedes", "Honda"],
    11: ["Volkswagen", "BMW", "Mercedes", "Ford"],
    12: ["Toyota", "Mercedes", "Ford"],
    13: ["Ford", "Honda", "Toyota", "Mercedes"],
    14: ["Honda", "Volkswagen", "Hyundai", "Mercedes", "BMW"],
    15: ['Volkswagen', 'Honda', 'Volkswagen', 'BMW'],
    16: ['Ford', 'Honda', 'Ford', 'Ford'],
    17: ['Mercedes', 'Hyundai'],
    18: ['Volkswagen', 'Volkswagen'],
    19: ['Toyota', 'Toyota', 'Mercedes', 'Mercedes'],
    20: ['Ford', 'Ford', 'Mercedes', 'Hyundai'],
}


def clear_lst(item, subset):
    temp_list = copy(item)
    for s in subset:
        temp_list.remove(s)
    return temp_list


def subsets(item):
    temp_list = []
    for j in range(1, len(list(item))):
        temp_list += list(combinations(list(item), j))
    return temp_list


def normalization(dfNormalizedView):
    for idx in range(len(trSubjectSets)):
        for name in F1:
            if name in trSubjectSets[idx + 1]:
                dfNormalizedView.loc[idx][name] = 1
    return dfNormalizedView


def data_subject_set():
    dataSubjectSetsTemp = []
    for i in range(len(F1) + 1):
        dataSubjectSetsTemp.extend(
            [list(item), find_all_quantity(item)]
            for item in list(combinations(F1, i))
            if find_all_quantity(item) >= 1 and item != ()
        )
    return dataSubjectSetsTemp


def data_normalized_view():
    return [[0] * (len(F1))] * len(trSubjectSets)


def find_all_quantity(item):
    quantity = 0
    for i in trSubjectSets:
        bool_temp = True
        for j in item:
            bool_temp = bool_temp and j in trSubjectSets[i]
        if bool_temp:
            quantity += 1
    return quantity


def support(item):
    print(
        f'support = {round(find_all_quantity(item), 3)} / {round(len(trSubjectSets), 3)} = {round(find_all_quantity(item) / len(trSubjectSets) * 100, 1)}')
    return round(find_all_quantity(item) / len(trSubjectSets) * 100, 1)


def reliability(item, condition):
    q1 = find_all_quantity(item)
    q2 = find_all_quantity(condition)
    print(f'reliability = {q1} / {q2} = {round(q1 / q2 * 100, 1)}')
    return round(q1 / q2 * 100, 1)


def lift(reliability, res):
    q = find_all_quantity(res)
    print(f'lift = {reliability} / ({q} / {len(trSubjectSets)} * 100) = {round(reliability / (q / len(trSubjectSets) * 100), 2)}')
    return round(reliability / (q / len(trSubjectSets) * 100), 2)


def data_associative_rules():
    data_full = []
    for i in range(2, len(F1) + 1):
        for item in list(combinations(F1, i)):
            if find_all_quantity(item) >= 1 and item != ():
                data_full += data_set(list(item), subsets(item))

    return data_full


def data_set(item, subsets):
    return [
        [
            con := clear_lst(item, subset),
            res := list(subset),
            support(item),
            rel := reliability(item, con),
            lift(rel, res)
        ]
        for subset in subsets
    ]


def popular_sets(dfSubjectSets):
    dfSubjectSets["Поддержка"] = 0
    for idx in range(len(dfSubjectSets)):
        value = support(dfSubjectSets.loc[idx]["Набор"])
        dfSubjectSets.loc[idx, "Поддержка"] = value

    print(dfSubjectSets.sort_values(by="Поддержка", ascending=False), end='\n\n')


def main():
    dfNormalizedView = pd.DataFrame(data_normalized_view(), columns=F1)
    dfNormalizedView = normalization(dfNormalizedView)
    dfSubjectSets = pd.DataFrame(data_subject_set(), columns=["Набор", "Кол-во"])

    print('Нормализованный вид данных:')
    print(dfNormalizedView, end='\n\n')
    print('Все наборы:')
    print(dfSubjectSets, end='\n\n')

    df_F2 = dfSubjectSets.loc[dfSubjectSets["Кол-во"] >= 4, ["Набор", "Кол-во"]].reset_index(drop=True)
    print('Наборы после фильтров:')
    print(df_F2, end='\n\n')

    data_all = data_associative_rules()
    dfAssociativeRules = pd.DataFrame(data_all,
                                      columns=["Условие", "Следствие", "Поддержка", "Достоверность", "Лифт"])
    print('Все ассоциативные правила:')
    print(dfAssociativeRules.to_string(), end='\n\n')

    print('Правила после фильтров:')
    print(dfAssociativeRules.loc[
              (dfAssociativeRules["Поддержка"] >= 20) &
              (dfAssociativeRules["Достоверность"] >= 70)
              ]
          .sort_values(by=["Достоверность"], ascending=False)
          .reset_index(drop=True)
          .to_string(), end='\n\n')

    print('Популярные наборы')
    popular_sets(dfSubjectSets)

    # print('Что-если')
    # print('Введите значения через пробел')
    # lst = input().split(' ')
    # df = pd.DataFrame(columns=["Условие", "Следствие", "Поддержка", "Достоверность", "Лифт"])
    # for idx in range(len(dfAssociativeRules)):
    #     if dfAssociativeRules.loc[idx]["Условие"] in [lst, reversed(lst)]:
    #         df = pd.concat([df, dfAssociativeRules.loc[idx].to_frame().T])
    #
    # print(df.reset_index(drop=True).to_string())


main()
