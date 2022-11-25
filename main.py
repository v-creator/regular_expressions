from pprint import pprint
import csv
from functions import change_number_format, change_name, identify_duplicates, create_final_list, convert_duplicate_str, add_intermediate_list
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def read_file():
    with open('phonebook_raw.csv') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
        logger.info(' File read')
    return contacts_list

def write_file(contacts_list):
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)
        logger.info(' Recording file')

if __name__ == '__main__':
    contacts_list = read_file()
    change_name_list = change_name(contacts_list)
    upgrade_number_list =  change_number_format(change_name_list)
    duplicates = identify_duplicates(upgrade_number_list)
    final_list = create_final_list(upgrade_number_list, duplicates)
    intermediate_list = convert_duplicate_str(upgrade_number_list, duplicates)
    result = add_intermediate_list(final_list, intermediate_list)
    write_file(result)