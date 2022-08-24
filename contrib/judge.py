import subprocess
import tempfile
import base64
from sqlalchemy.orm import Session
from crud import create
from difflib import SequenceMatcher
from typing import TypeVar
from converters.schemas import convert_schema_to_model
from routers.controllers.problem import get_problem


async def judge_submission(db: Session, schema: TypeVar('TSchema')) -> None:
    query = convert_schema_to_model(schema=schema)

    problem = await get_problem(id=schema.problem_id, db=db)

    if schema.language_type == 'python':
        response = await run_python(schema.content, problem.data_entry)
    elif schema.language_type == 'c':
        response = await run_c(schema.content, problem.data_entry)
    elif schema.language_type == 'cpp':
        response = await run_cpp(schema.content, problem.data_entry)
    else:
        print('Invalid language type')
        pass

    schema.status = judge(response=response, expected_output=problem.data_output)
    query = convert_schema_to_model(schema=schema)

    db.add(query)
    db.commit()


async def run_python(content, data_input):
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
        return pipe.communicate(data_input.encode(), timeout=5000)


async def run_c(code, data_input):
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
        return pipe.communicate(data_input.encode(), timeout=5000)


async def run_cpp(code, data_input):
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
        return pipe.communicate(data_input.encode(), timeout=5000)


def get_ratio(expected_response, response):
    return 100 - SequenceMatcher(None, expected_response, response).ratio() * 100


def judge(response: dict, expected_output: str):
    if response[1]:
       return 'COMPILATION ERROR'
    elif response[0] and (response[0].decode().count('\n') != expected_output.count('\n') or response[0].decode()[-1] != '\n'):
       return 'PRESENTATION ERROR'
    else:
        response = response[0].decode()
        ratio = get_ratio(expected_output.replace('\n', ''), response.replace('\n', ''))
        if ratio == 0:
            return 'ACCEPTED'
        else:
            count = (ratio - (ratio % 5)) or 5
            return f'WRONG ANSWER: {count:.0f}%'

