import sqlite3
import subprocess
import tempfile
from difflib import SequenceMatcher


def get_ratio(expected_response, response):
    return 100 - SequenceMatcher(None, expected_response, response).ratio() * 100


def init_db(index, language, code, expected_input, expected_output, delete=False):
    conn = sqlite3.connect('teste.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS teste (id int, language text, code text, input text, output text)')
    if delete:
        cursor.execute('DELETE FROM teste')
    cursor.execute(
        'INSERT INTO teste VALUES (?, ?, ?, ?, ?)',
        (index, language, code, expected_input, expected_output),
    )
    conn.commit()


def get_from_db(id):
    conn = sqlite3.connect('teste.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT code, input, output FROM teste WHERE id = {id}')
    data = cursor.fetchall()[0]
    return data[0], data[1], data[2]


def run_python(code, data_input):
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(code.encode())
        tmp.file.seek(0)
        pipe = subprocess.Popen(
            f'python {tmp.name}',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        return pipe.communicate(data_input.encode(), timeout=5000)


def run_c(code, data_input):
    with tempfile.NamedTemporaryFile(suffix='.c') as tmp:
        tmp.write(code.encode())
        tmp.file.seek(0)
        pipe = subprocess.Popen(
            f'gcc -lm -o {tmp.name}_ {tmp.name} && {tmp.name}_ && rm {tmp.name}_',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        return pipe.communicate(data_input.encode(), timeout=5000)


def run_cpp(code, data_input):
    with tempfile.NamedTemporaryFile(suffix='.cpp') as tmp:
        tmp.write(code.encode())
        tmp.file.seek(0)
        pipe = subprocess.Popen(
            f'g++ -lm -o {tmp.name}_ {tmp.name} && {tmp.name}_ && rm {tmp.name}_',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        return pipe.communicate(data_input.encode(), timeout=5000)


def judge(obj: dict):
    if obj[1]:
        print('COMPILATION ERROR')
    elif obj[0] and (obj[0].decode().count('\n') != expected_response.count('\n') or response[0].decode()[-1] != '\n'):
        print('PRESENTATION ERROR')
    else:
        obj = obj[0].decode()
        ratio = get_ratio(expected_response.replace('\n', ''), obj.replace('\n', ''))
        if ratio == 0:
            print('ACCEPTED')
        else:
            count = (ratio - (ratio % 5)) or 5
            print(f'WRONG ANSWER: {count:.0f}%')


def initial():
    code_in_python = """
def add(x, y):
    return x + y
x, y = map(int, input().split(' '))
print(add(x, y))
    """

    code_in_c = """
    #include <stdio.h>
    int main() {
        int a, b;
        scanf("%d %d", &a, &b);
        printf("%d\\n", a + b);
        return 0;
    }
    """

    code_in_cpp = """
    #include <iostream>

    int main() {
        int a, b;
        std::cin >> a >> b;
        std::cout << std::to_string(a+b) + "\\n";
        return 0;
    }
    """

    request_input_to_db = '20 5'
    expected_response_to_db = '25\n'

    init_db(
        1,
        'python',
        code_in_python,
        request_input_to_db,
        expected_response_to_db,
        delete=False,
    )
    init_db(
        2,
        'c',
        code_in_c,
        request_input_to_db,
        expected_response_to_db,
        delete=False,
    )
    init_db(
        3,
        'cpp',
        code_in_cpp,
        request_input_to_db,
        expected_response_to_db,
        delete=False,
    )


initial()
code_py, request_input, expected_response = get_from_db(1)
code_c, request_input, expected_response = get_from_db(2)
code_cpp, request_input, expected_response = get_from_db(3)

response = run_python(code_py, request_input)
judge(response)

response = run_c(code_c, request_input)
judge(response)

response = run_cpp(code_cpp, request_input)
judge(response)
