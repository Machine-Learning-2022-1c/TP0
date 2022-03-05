import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser

ALCOHOL_COLUMN = 'Alcohol'
FAT_COLUMN = 'Grasas_sat'
CALORIES_COLUMN = 'Calorías'
SEX_COLUMN = 'Sexo'


def replace_by_statistic(statistic, data, column, empty_value=999.99):
    filtered_data = data[data[column] != empty_value]

    statistic_value = 0
    if statistic == 'mean':
        statistic_value = filtered_data[column].mean()
    elif statistic == 'mode':
        statistic_value = filtered_data[column].mode()[0]
    elif statistic == 'median':
        statistic_value = filtered_data[column].median()

    data.loc[data[column] == empty_value, column] = statistic_value

    return statistic_value


def boxplot_figure(data, title):
    plt.figure()
    plt.title(title)
    plt.boxplot(data)


def plot_by_sex(data, column):
    male_data = data[data[SEX_COLUMN] == 'M']
    female_data = data[data[SEX_COLUMN] == 'F']

    boxplot_figure(male_data[column], f'{column} Hombres')
    boxplot_figure(female_data[column], f'{column} Mujeres')

    return {
        "male_data": male_data,
        "female_data": female_data
    }


def plot_by_calories(data, column):
    cate1 = data[data[CALORIES_COLUMN] <= 1100]
    cate2 = data[(data[CALORIES_COLUMN] > 1100) & (data[CALORIES_COLUMN] <= 1700)]
    cate3 = data[data[CALORIES_COLUMN] > 1700]

    boxplot_figure(cate1[column], f'{column} CATE 1')
    boxplot_figure(cate2[column], f'{column} CATE 2')
    boxplot_figure(cate3[column], f'{column} CATE 3')

    return {
        "cate1": cate1,
        "cate2": cate2,
        "cate3": cate3
    }


def print_statistics(title, data, column):
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    print('******************************************')
    print(title)
    print()
    print(f'Mean: {data[column].mean()}')
    print(f'Mode: {data[column].mode()[0]}')
    print(f'Median: {data[column].median()}')
    print(f'Std. deviation: {data[column].std()}')
    print(f'Q1: {q1} | IQR: {iqr} | Q3: {q3}')
    print(f'Correlation:\n {data.corr()}')
    print('******************************************')


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", default='Datos trabajo 1.xls',
                        help="Path to excel file", metavar="FILE")
    parser.add_argument("-c", "--column", dest="column", default='alcohol',
                        help="Name of column to analyze [alcohol | fat | calories]")
    parser.add_argument("-s", "--statistic", dest="statistic", default='mean',
                        help="Statistic to use to replace missing values [mean | median | mode]")
    parser.add_argument("-p", "--plot", dest="plot", default='population',
                        help="Name of the plot [population | sex | calories]")

    args = parser.parse_args()

    data = pd.read_excel(args.filename)

    column = ''
    if args.column == 'alcohol':
        column = ALCOHOL_COLUMN
    elif args.column == 'fat':
        column = FAT_COLUMN
    elif args.column == 'calories':
        column = CALORIES_COLUMN
    else:
        print('Invalid column, option must be either [alcohol | fat | calories]')
        exit()

    replace_by_statistic(args.statistic, data, column)

    if args.plot == 'population':
        boxplot_figure(data[column], f'Population {column}')
        print_statistics(f'{column} Statistics', data, column)
    elif args.plot == 'sex':
        result = plot_by_sex(data, column)
        print_statistics(f'Male {column} Statistics', result["male_data"], column)
        print_statistics(f'Female {column} Statistics', result["female_data"], column)
    elif args.plot == 'calories':
        result = plot_by_calories(data, column)
        print_statistics(f'CATE 1 {column} Statistics', result["cate1"], column)
        print_statistics(f'CATE 2 {column} Statistics', result["cate2"], column)
        print_statistics(f'CATE 3 {column} Statistics', result["cate3"], column)

    plt.show()


