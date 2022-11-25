import re
import logging

logger = logging.getLogger(__name__)

def change_name(row_list):
    for row in row_list:
        if len(row[1].split(' ')) > 1:
            row[2], row[1] = row[1].split(' ')[1], row[1].split(' ')[0]
        if len(row[0].split(' ')) == 2:
            row[1], row[0] = row[0].split(' ')[1], row[0].split(' ')[0]
        if len(row[0].split(' ')) > 2:
            row[2], row[1], row[0] = row[0].split(' ')[2], row[0].split(' ')[1], row[0].split(' ')[0]
    logger.info(' Success change_name')
    return row_list


def change_number_format(row_list):
    re_contacts_list = []
    for row in row_list:
        new_str = []
        for string in row:
            pattern = '(8|\+7)?\s*\((\d+)\)\s*(\d+)-(\d+)-(\d+)\s?(\()?([а-я.]+)?\s?(\d+)?(\))?'
            pattern2 = '(8|\+7)\s*(\(?\d{3})-?(\d+)-?(\d{2})-?(\d{2})'
            if re.findall(pattern, string):
                re_string = re.sub(pattern, r"+7(\2)\3-\4-\5 \7\8", string)
                if re_string != '':
                    new_str.append(re_string)
            elif re.findall(pattern2, string):
                re_string = re.sub(pattern2, r"+7(\2)\3-\4-\5", string)
                if re_string != '':
                    new_str.append(re_string)
            else:
                re_string = string
                new_str.append(re_string)
        re_contacts_list.append(new_str)
    logger.info(' Success change_number_format')
    return re_contacts_list


def identify_duplicates(row_list):
    list_duplicates = []
    for i in range(1,len(row_list)):
        for j in range(1,len(row_list)):
            if i != j and row_list[i][0] == row_list[j][0] and row_list[i][1] == row_list[j][1]:
                list_duplicates.append(row_list[i][0])
    list_duplicates = sorted(set(list_duplicates), key=list_duplicates.index)
    logger.info(' Success identify_duplicates')
    return list_duplicates


def create_final_list(row_list, duplicate_list):
    final_list = []
    for row in row_list:
        if row[0] not in duplicate_list:
            final_list.append(row)
    logger.info(' Success create_final_list')
    return final_list


def convert_duplicate_str(row_list, duplicate_list):
    intermediate_list = {}
    for row in row_list:
        for i in range(len(duplicate_list)):
            if row[0] == duplicate_list[i]:
                if i not in intermediate_list.keys():
                    intermediate_list[i] = {
                        'lastname': {row[0]},
                        'firstname': {row[1]},
                        'surname': {row[2]},
                        'organization': {row[3]},
                        'position': {row[4]},
                        'phone': {row[5]},
                        'email': {row[6]}
                        }
                else:
                    intermediate_list[i]['lastname'].add(row[0])
                    intermediate_list[i]['firstname'].add(row[1])
                    intermediate_list[i]['surname'].add(row[2])
                    intermediate_list[i]['organization'].add(row[3])
                    intermediate_list[i]['position'].add(row[4])
                    intermediate_list[i]['phone'].add(row[5])
                    intermediate_list[i]['email'].add(row[6])
    logger.info(' Success convert_duplicate_str')
    return intermediate_list


def add_intermediate_list(final_list, intermediate_list):
    for item in intermediate_list.items():
        new_row = []
        for elemnt in item[1]:
            if len(item[1].get(elemnt)) > 1:
                new_row.append([x for x in item[1].get(elemnt) if x != ''][0])
            else:
                new_row.append(list(item[1].get(elemnt))[-1])
        final_list.append(new_row)
    logger.info(' Success add_intermediate_list')
    return final_list