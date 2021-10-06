import difflib
import os
import glob
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

PROJECT_PATH = 'REPLACE_ROOT_PROJECT_PATH_HERE'

FORBIDDEN_DIRS = ['.vscode', '__pycache__', 'Results', '.pytest_cache', '.idea', '.git']
FILES = []
OUTPUT_LIST = []

def get_path_file():
    for dirpath, dirs, files in os.walk(PROJECT_PATH):
        # Check if it is the last directory
        if not dirs:
            flag = False
            for FD in FORBIDDEN_DIRS:
                if FD in dirpath:
                    flag = True
                    break
            if not flag:
                result = glob.glob(dirpath + "/*.robot")
                if result:
                    FILES.append(dirpath)
                    FILES.append(result)


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


def find_duplicate_keywords(keywords_list: list):
    keywords = collections.Counter(keywords_list)
    print_output('<br><br><h2>Duplicated Keywords:</h2><br><br>')
    for word, count in sorted(keywords.items()):
        if count > 1:
            print_output(f'<b>Occurrences</b> {count}: {word}')


def find_similar_keywords(keywords_list: list):
    keywords_list.sort()
    print_output('<br><br><h2>Similar Keywords</h2><br><br>')
    for keyword in keywords_list:
        result = difflib.get_close_matches(keyword, keywords_list)
        # Remove found similar words
        for res in result:
            keywords_list.remove(res)
        # Ignore one single occurrence
        if len(result) > 1:
            for r in result:
                print_output(r)


def output_file():

    header = '''
    <!DOCTYPE html>
    <html lang="pt">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <title>Diagnostics</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet"/>
    </head>
    <style>
    #hierarchy { font-family: FontAwesome; }
    .foldercontainer, .file, .noitems { display: block; padding: 5px 5px 5px 50px; }
    .noitems { display: none; pointer-events: none; }
    ul { list-style-type: none; margin: 0; padding: 0; }
    li:hover  { background-color: #7fd2e4; }
    li:before { padding-right: 10px; }
    </style>
    <body>
    <div id="hierarchy">
    <h1>Robot Framework Project Diagnostics</h1>
    <ul>
    '''

    footer = '''
    </ul>
    </div>
    </body>
    </html>
    '''

    content = ""
    for c in OUTPUT_LIST:
        content+= "<li>" + c + "</li>"

    html = header + content + footer
    report = open("diagnostics.html","w")
    report.write(html)
    report.close()


def print_output(output: str):
    OUTPUT_LIST.append(output)


if __name__ == '__main__':
    all_project_keywords = []
    get_path_file()
    for F in FILES:
        if type(F) == str:
            print_output('<span class="folder fa-folder-o" data-isexpanded="true">&emsp;' + F + '</span>')
        if type(F) == list:
            for files in F:
                print_output('<span class="file fa-file-code-o">&emsp;&emsp;' + files + '</span>')
                keywords_list = get_keywords(files)
                for k in keywords_list:
                    print_output('&emsp;&emsp;&emsp;&emsp;' + k)
                    all_project_keywords.append(k)


    find_duplicate_keywords(all_project_keywords)
    find_similar_keywords(all_project_keywords)
    output_file()
