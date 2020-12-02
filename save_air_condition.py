import csv
import pickle
from itertools import product
from get_air_condition import get_city_coding
from get_air_condition import get_from_http


def save_air_condition(cities=None, test=False, colunm_name_write = True):
    '''
    save all cities air condition information
    :param cities:
    :param test:
    :return:
    '''
    # cities = cities or list(get_city_coding().keys())
    if test:
        cities = cities[:2]

    column_name_wirte = colunm_name_write

    for index, city in enumerate(cities):
        print('runing ratio:{}%'.format(index * 100 / len(cities)))

        print('runing city:{}'.format(city))

        need_wirte_column_name = not column_name_wirte

        sucess, write_column = save_one_city_info(city, need_column=need_wirte_column_name)

        if need_wirte_column_name and write_column:
            column_name_wirte = True


def save_one_city_info(city, need_column=False):
    city_codes = get_city_coding()

    code = city_codes[city]

    monthes = range(1, 12 + 1)
    years = range(2016, 2019 + 1)

    column_name_write = False

    success = False
    # produce 多个可迭代对象的笛卡尔乘积
    for index, y_m in enumerate(product(years, monthes)):
        y, m = y_m

        if index % 10 == 0:
            print("{}-{}".format(y, m))

        data = get_from_http(code, y, m)

        if data:
            if need_column:
                # data = data[0]
                column_name_write = True
                need_column=False
            else:
                data = data[1:]  # delete the column name

            write_into_csv(data)
            success = True
    return success, column_name_write


def write_into_csv(rows):
    air_condition_file = 'air_condition.csv'

    with open(air_condition_file, 'a',newline='') as f:
        # 写csv的一个操作
        writer = csv.writer(f)
        writer.writerows(rows)

    return air_condition_file




if __name__ == '__main__':
    all_cities = sorted(list(get_city_coding().keys()))

    step = 5
    begin = 0
    last_city = '黔西南'
    last_index = all_cities.index(last_city)

    # all_cities=all_cities[last_index+1:]
    column_name_write = False
    for i in range(step, len(all_cities), step):
        print('ratio {}/{}'.format(i, len(all_cities)))

        cities = all_cities[begin:i]

        print('begin:{},end:{}'.format(begin, i))

        begin += step
        print('calculate:{}'.format(cities))
        save_air_condition(cities=cities, test=False, colunm_name_write=column_name_write)
        column_name_write = True
