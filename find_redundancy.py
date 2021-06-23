# Find duplicated and similar keywords in Robot files
import difflib
import os
import collections

FORBIDDEN_CHARACTERS = [
    '    ',
    '...',
    '#',
    '$',
    'Test Cases',
    'Resource',
    'Library',
    'Variables',
    'Documentation',
    'Settings',
    'Keywords',
    'Variable',
    'Suite',
    'Metadata'
]

PROJECT_PATH = ''


def get_files(root_path: str = PROJECT_PATH):
    list_of_files = []
    for (dir_path, dir_names, filenames) in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.robot'):
                if not str(dir_path).endswith('\\'):
                    dir_path += '\\'
                list_of_files.append(dir_path + filename)

    return list_of_files


def get_keywords(file_path: str) -> list:
    file = open(file_path, encoding='UTF-8')
    lines = file.readlines()
    keywords_list = []
    flag = False
    for line in lines:
        for fc in FORBIDDEN_CHARACTERS:
            if fc in line:
                flag = True
                break
        new_line = line.replace('\n', '').replace('\r', '').strip()
        if not flag and new_line != '':
            keywords_list.append(new_line)
        flag = False
    file.close()

    return keywords_list


def create_keywords_list():
    single_list = []
    files = get_files()
    for file in files:
        keywords_list = get_keywords(file)
        for keywords in keywords_list:
            single_list.append(keywords)

    return single_list


def find_similar_keywords(keywords_list: list):
    keywords_list.sort()
    print('\nSimilar Keywords:\n')
    for keyword in keywords_list:
        result = difflib.get_close_matches(keyword, keywords_list)
        # Remove found similar words
        for res in result:
            keywords_list.remove(res)
        # Ignore one single occurrence
        if len(result) > 1:
            print(result)


def find_duplicate_keywords(keywords_list: list):
    keywords = collections.Counter(keywords_list)
    print('\nDuplicated Keywords:\n')
    for word, count in sorted(keywords.items()):
        if count > 1:
            print(f'Occurrences {count}: {word}')


if __name__ == '__main__':
    single_list = create_keywords_list()
    find_duplicate_keywords(single_list)
    find_similar_keywords(single_list)
