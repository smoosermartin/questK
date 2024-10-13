import csv
import random
from datetime import date, timedelta, datetime
import argparse
import urllib.request
import os

today = date.today()
INFO_IDX = [1, 2, 7]
DATA_IDX = [2, 4, 5]


def check_files():
    urls = ["https://raw.github.com/cldf-datasets/wals/master/cldf/examples.csv",
            "https://raw.githubusercontent.com/cldf-datasets/wals/refs/heads/master/cldf/languages.csv"]

    path = "~/.cache/quest_k/"
    if not os.path.exists(path):
        os.makedirs(path)

    for url in urls:
        filename = url.split("/")[-1]
        file_path = path + filename
        if not os.path.exists(file_path):
            urllib.request.urlretrieve(url, file_path)


def get_list_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)


def set_date(date_arg):
    if date_arg:
        if date_arg == 'tomorrow':
            date_object = today + timedelta(days=1)
        elif date_arg == 'yesterday':
            date_object = today - timedelta(days=1)
        else:
            date_object = datetime.strptime(date_arg, '%d/%m/%Y')
    else:
        date_object = today
    return date_object


def zip_with_columns(column_idx, l1, l2):
    headers = [l1[0][idx] for idx in column_idx]
    data = [l2[idx] for idx in column_idx]
    zip_dict = dict(zip(headers, data))
    return zip_dict


def gen_dict(examples_l, languages_l, choice):
    lang_id = choice[1]
    for row in languages_l:
        if lang_id in row:
            lang_info = row
            break
    ex_dict = zip_with_columns(INFO_IDX, languages_l, lang_info)
    ex_dict.update(zip_with_columns(DATA_IDX, examples_l, choice))
    return ex_dict


def choose_example(date_obj, examples_l):
    seed = date_obj.strftime("%d/%m/%Y")
    random.seed(seed)
    choice = random.choice(examples_l)
    return choice


def cli(date_arg):
    check_files()
    examples_l = get_list_csv('~/.cache/quest_k/examples.csv')
    languages_l = get_list_csv('~/.cache/quest_k/languages.csv')
    date_object = set_date(date_arg)
    choice = choose_example(date_object, examples_l)
    ex_dict = gen_dict(examples_l, languages_l, choice)
    for key, value in ex_dict.items():
        print(f'{key: <20} {value: <40}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, help="Date in DD/MM/YYYY format, or 'yesterday' or 'tomorrow'")
    args = parser.parse_args()
    cli(args.date)
