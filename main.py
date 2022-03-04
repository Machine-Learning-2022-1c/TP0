import pandas as pd

ALCOHOL_COLUMN = 'Alcohol'
FAT_COLUMN = 'Grasas_sat'
CALORIES_COLUMN = 'Calorías'


def replace_by_mean(data, column, empty_value = 999.99):
    filtered_data = data[data[column] != empty_value]
    mean = filtered_data[column].mean()
    data.loc[data[column] == empty_value, column] = mean
    return data


if __name__ == '__main__':
    data = pd.read_excel('Datos trabajo 1.xls')
    replace_by_mean(data, ALCOHOL_COLUMN)
    replace_by_mean(data, FAT_COLUMN)

    print(data)


