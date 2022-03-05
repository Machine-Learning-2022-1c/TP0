import pandas as pd
import matplotlib.pyplot as plt

ALCOHOL_COLUMN = 'Alcohol'
FAT_COLUMN = 'Grasas_sat'
CALORIES_COLUMN = 'Calorías'
SEX_COLUMN = 'Sexo'


def replace_by_mean(data, column, empty_value=999.99):
    filtered_data = data[data[column] != empty_value]
    mean = filtered_data[column].mean()
    data.loc[data[column] == empty_value, column] = mean
    return data


def boxplot_figure(data, title):
    plt.figure()
    plt.title(title)
    plt.boxplot(data)


def plot_by_sex(data, column):
    male_data = data[data[SEX_COLUMN] == 'M']
    female_data = data[data[SEX_COLUMN] == 'F']

    boxplot_figure(male_data[column], f'{column} Hombres')
    boxplot_figure(female_data[column], f'{column} Mujeres')


def plot_by_calories(data, column):
    cate1 = data[data[CALORIES_COLUMN] <= 1100]
    cate2 = data[(data[CALORIES_COLUMN] > 1100) & (data[CALORIES_COLUMN] <= 1700)]
    cate3 = data[data[CALORIES_COLUMN] > 1700]

    boxplot_figure(cate1[column], f'{column} CATE 1')
    boxplot_figure(cate2[column], f'{column} CATE 2')
    boxplot_figure(cate3[column], f'{column} CATE 3')


if __name__ == '__main__':
    data = pd.read_excel('Datos trabajo 1.xls')
    replace_by_mean(data, ALCOHOL_COLUMN)
    replace_by_mean(data, FAT_COLUMN)

    plot_by_sex(data, ALCOHOL_COLUMN)
    plot_by_calories(data, ALCOHOL_COLUMN)

    plt.show()


