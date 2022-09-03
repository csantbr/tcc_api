import subprocess
import tempfile
import base64
from uuid import UUID
from difflib import SequenceMatcher
from typing import TypeVar
from converters.schemas import convert_schema_to_model
from routers.controllers.submission import update_submission
from contrib.exceptions import LanguageNotImplemented, UnprocessableEntity


def judge_submission(id: UUID, problem_id: UUID, schema: TypeVar('TSchema')):
    if schema.language_type == 'python':
        response = run_python(schema.content, problem.data_entry)
    elif schema.language_type == 'c':
        response = run_c(schema.content, problem.data_entry)
    elif schema.language_type == 'cpp':
        response = run_cpp(schema.content, problem.data_entry)
    else:
        raise LanguageNotImplemented

    if not schema.content:
        raise UnprocessableEntity

    field = judge(response=response, expected_output=problem.data_output)
    query = convert_schema_to_model(schema=schema, field=field)




def run_python(content, data_input):
    code = base64.b64decode(content)
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(code)
        tmp.file.seek(0)
        pipe = subprocess.Popen(
            f'python {tmp.name}',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        try:
            return pipe.communicate(data_input.encode(), timeout=35)
        except subprocess.TimeoutExpired:
            pipe.kill()
            return 'TLE'


def run_c(content, data_input):
    code = base64.b64decode(content)
    with tempfile.NamedTemporaryFile(suffix='.c') as tmp:
        tmp.write(code)
        tmp.file.seek(0)
        pipe = subprocess.Popen(
            f'gcc -lm -o {tmp.name}_ {tmp.name} && {tmp.name}_ && rm {tmp.name}_',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        try:
            return pipe.communicate(data_input.encode(), timeout=35)
        except subprocess.TimeoutExpired:
            pipe.kill()
            return 'TLE'


def run_cpp(content, data_input):
    code = base64.b64decode(content)
    with tempfile.NamedTemporaryFile(suffix='.cpp') as tmp:
        tmp.write(code)
        tmp.file.seek(0)
        pipe = subprocess.Popen(
            f'g++ -lm -o {tmp.name}_ {tmp.name} && {tmp.name}_ && rm {tmp.name}_',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        try:
            return pipe.communicate(data_input.encode(), timeout=35)
        except subprocess.TimeoutExpired:
            pipe.kill()
            return 'TLE'


def get_ratio(expected_response, response):
    return 100 - SequenceMatcher(None, expected_response, response).ratio() * 100


def judge(response, expected_output: str):
    if response == 'TLE':
        return 'TIME LIMIT EXCEEDED'
    elif not response[0].decode():
        return 'COMPILATION ERROR'
    elif response[0] and (
        response[0].decode().count('\n') != expected_output.count('\n') or response[0].decode()[-1] != '\n'
    ):
        return 'PRESENTATION ERROR'
    else:
        response = response[0].decode()
        ratio = get_ratio(expected_output.replace('\n', ''), response.replace('\n', ''))
        if ratio == 0:
            return 'ACCEPTED'
        else:
            count = (ratio - (ratio % 5)) or 5
            return f'WRONG ANSWER: {count:.0f}%'
