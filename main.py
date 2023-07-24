import csv
import re

csv_file = 'phonebook_raw.csv'
PHONE_EX = r"(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]*(доб\.)?[\s]?(\d{4})*\)?"
PHONE_SUB = r"+7(\2)-\3-\4-\5 \6\7"

def open_csv(name_file, delimiter):
    with open(name_file, 'r', encoding='utf-8') as file:
        return list(csv.reader(file, delimiter=delimiter))

def get_full_name(line: list):
    return " ".join(line[:3]).split(' ')

def get_full_list(contact: list,PHONE_EX,PHONE_SUB):
    full_list = []
    for line in contact:
        full_name = get_full_name(line)
        result = [full_name[0], full_name[1], full_name[2], line[3], line[4],
                  re.sub(PHONE_EX, PHONE_SUB, line[5]), line[6]]
        full_list.append(result)
    return full_list

def removing_duplicates(full_list):
    res_dict = {}
    for name in full_list:
        if name[0] in res_dict:
            for i, elm in enumerate(res_dict[name[0]]):
                if elm == '':
                    res_dict[name[0]][i] = name[i + 1]
        else:
            res_dict[name[0]] = name[1:]
    return res_dict

def dict_to_list(data: dict):
    list_for_csv = []
    for key, values in data.items():
        onemore_list = []
        onemore_list.append(key)
        for val in values:
            onemore_list.append(val)
        list_for_csv.append(onemore_list)
    return list_for_csv

def save_csv(data, delimiter):
        with open("contact_book.csv", 'w', encoding='utf-8', newline='') as file:
            write = csv.writer(file, delimiter=delimiter)
            for row in data:
                write.writerow(row)

if __name__ == '__main__':
    open_file = open_csv(csv_file, ',')
    full_list = get_full_list(open_file, PHONE_EX, PHONE_SUB)
    r_dup_dict = removing_duplicates(full_list)
    final_list = dict_to_list(r_dup_dict)
    save_csv(final_list, ',')

