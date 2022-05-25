import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLNE = '\033[4m'
    END = '\033[0m'


def plot_data(X):
    plt.figure(figsize=(7.5, 6))
    for i in range(len(X)):
        plt.scatter(X[i][0], X[i][1], color='k')
    plt.show()
    # Первоначально назначает случайные точки данных в качестве центроидов для кластеров


def random_centroid(X, k):
    # Создание k случайных индексов и использование точки данных в этих индексах в качестве центроида
    random_idx = [np.random.randint(len(X)) for _ in range(k)]
    return [X[i] for i in random_idx]


# # Определяет, какая точка данных относится к какому кластеру
def assign_cluster(X, ini_centroids, k):
    cluster = []  # to store the data point's corresponding cluster number
    # for every point in X
    for i in range(len(X)):
        euc_dist = [np.linalg.norm(np.subtract(X[i], ini_centroids[j])) for j in range(k)]

        idx = np.argmin(euc_dist)  # returns the index where the value is minimum
        cluster.append(idx)  # appends the index to the cluster array
    return np.asarray(cluster)


# Возвращает обновленный центроид
def compute_centroid(X, clusters, k):
    centroid = []  # stores the centroid values
    for i in range(k):
        temp_arr = [X[j] for j in range(len(X)) if clusters[j] == i]
        # taking mean among those points and storing it in the centroid array
        centroid.append(np.mean(temp_arr, axis=0))
    return np.asarray(centroid)


# Возвращает разницу между предыдущим центроидом и вновь вычисленным центроидом
def difference(prev, nxt):
    return sum(np.linalg.norm(prev[i] - nxt[i]) for i in range(len(prev)))


# Используется для построения графика на каждой итерации
def show_clusters(X, clusters, centroids, ini_centroids, mark_centroid=True, show_ini_centroid=True, show_plots=True):
    # присвоение определенного цвета каждому кластеру. Предполагая, что на данный момент 3
    cols = {0: 'r', 1: 'b', 2: 'g', 3: 'coral', 4: 'c', 5: 'lime'}
    fig, ax = plt.subplots(figsize=(7.5, 6))
    # отображает все точки кластера
    for i in range(len(clusters)):
        ax.scatter(X[i][0], X[i][1], color=cols[clusters[i]])
    # строит все центроиды
    for j in range(len(centroids)):
        ax.scatter(centroids[j][0], centroids[j][1], marker='*', color=cols[j])
        if show_ini_centroid:
            ax.scatter(ini_centroids[j][0], ini_centroids[j][1], marker="+", s=150, color=cols[j])
    # используется для обозначения центра тяжести, рисуя вокруг него круг
    if mark_centroid:
        for i in range(len(centroids)):
            ax.add_artist(plt.Circle((centroids[i][0], centroids[i][1]), 0.4, linewidth=2, fill=False))
            if show_ini_centroid:
                ax.add_artist(
                    plt.Circle((ini_centroids[i][0], ini_centroids[i][1]), 0.4, linewidth=2, color='y', fill=False))
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_title("K-means Кластеризация")
    if show_plots:
        plt.show()


"""
Начальный центр тяжести отмечен плюсовым маркером и желтым кружком
Конечный центр тяжести отмечен маркером * и черным кружком
"""


# Используется для выполнения кластеризации k средств
# если не задан ввод типа show, то он покажет график для каждого цикла
def k_means(X, k, show_type='all', show_plots=True):
    c_prev = random_centroid(X, k)  # первоначально назначьте случайный центроид
    cluster = assign_cluster(X, c_prev, k)  # для сохранения номера кластера точки данных
    diff = 100  # предполагая, что начальная разница между центроидами равна 100
    ini_centroid = c_prev  # сохранение начальных значений центроида

    print(
        color.BOLD + "NOTE:\n + и Желтый Круг -> Начальный центроид\n * и Черный Круг -> Конечный центроид" + color.END)

    # останавливается, если разница меньше 0,001
    if show_plots:
        print(color.BOLD + "\n\nInitial Plot:\n" + color.END)
        show_clusters(X, cluster, c_prev, ini_centroid, show_plots=show_plots)
    while diff > 0.0001:
        cluster = assign_cluster(X, c_prev, k)  # присваивает точку данных соответствующим кластерам
        # построение начального графика
        if show_type == 'all' and show_plots:
            show_clusters(X, cluster, c_prev, ini_centroid, False, False, show_plots=show_plots)
        c_new = compute_centroid(X, cluster, k)  # для вычисления новой точки центроида
        diff = difference(c_prev, c_new)  # чтобы вычислить разницу между центроидами
        c_prev = c_new  # теперь новый центроид становится текущей точкой центроида

    # Конечные кластерные центры
    if show_plots:
        print(color.BOLD + "\nInitial Cluster Centers:\n" + color.END)
        print(ini_centroid)
        print(color.BOLD + "\nFinal Cluster Centers:\n" + color.END)
        print(c_prev)
        # Построение окончательного графика
        print(color.BOLD + "\n\nFinal Plot:\n" + color.END)
        show_clusters(X, cluster, c_prev, ini_centroid, mark_centroid=True, show_ini_centroid=True)
    return cluster, c_prev


k = 2
X, original_clus = make_blobs(n_samples=500, centers=2, n_features=2, random_state=30)
plot_data(X)
# Окончательный график и окончательные центры кластеров находятся в конце по умолчанию show_type имеет значение
# 'all', чтобы получить только начальный и конечный график, установите show_type в 'ini_fin'
cluster, centroid = k_means(X, k, show_type='ini_fin')
