#!/usr/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser

ALCOHOL_COLUMN = 'Alcohol'
FAT_COLUMN = 'Grasas_sat'
CALORIES_COLUMN = 'Calorías'
SEX_COLUMN = 'Sexo'

def get_statistic(statistic, data, column, empty_value):
    if statistic == 'mean':
        return data[data[column] != empty_value][column].mean()
    elif statistic == 'mode':
        return data[data[column] != empty_value][column].mode()[0]
    elif statistic == 'median':
        return data[data[column] != empty_value][column].median()

def replace_by_statistic(statistic, data, column, column2, empty_value=999.99):
    if statistic == 'remove':
        return data[(data[column] != empty_value) & (data[column2] != empty_value)]

    data.loc[data[column] == empty_value, column] = get_statistic(statistic, data, column, empty_value)
    data.loc[data[column2] == empty_value, column2] = get_statistic(statistic, data, column2, empty_value)
    return data

def boxplot_figure(data, title):
    plt.figure()
    plt.title(title)
    plt.boxplot(data)

def scatter(data,x,y):
    plt.figure()
    plt.plot(data[x],data[y],'o')
    plt.title(f'{y} vs {x}')
    plt.xlabel(x)
    plt.ylabel(y)


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

def parseColumn(arg):
    column = ''
    if arg == 'alcohol':
        column = ALCOHOL_COLUMN
    elif arg == 'fat':
        column = FAT_COLUMN
    elif arg == 'calories':
        column = CALORIES_COLUMN
    else:
        print('Invalid column, option must be either [alcohol | fat | calories]')
        exit()
    return column

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename", default='Datos trabajo 1.xls',
                        help="Path to excel file", metavar="FILE")
    parser.add_argument("-c", "--column", dest="column", default='alcohol',
                        help="Name of column to analyze [alcohol | fat | calories]")
    parser.add_argument("-c2", "--column2", dest="column2", default='calories',
                        help="Name of column to compare against [alcohol | fat | calories]")
    parser.add_argument("-s", "--statistic", dest="statistic", default='mean',
                        help="Statistic to use to replace missing values [mean | median | mode]")
    parser.add_argument("-p", "--plot", dest="plot", default='population',
                        help="Name of the plot [population | sex | calories | scatter]")

    args = parser.parse_args()

    data = pd.read_excel(args.filename)

    column = parseColumn(args.column)
    column2 = parseColumn(args.column2)

    data = replace_by_statistic(args.statistic, data, column, column2)

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
    elif args.plot == 'scatter':
        scatter(data, column, column2)

    plt.show()


