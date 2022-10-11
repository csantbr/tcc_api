import subprocess
import tempfile
from difflib import SequenceMatcher
from typing import TypeVar
from uuid import UUID
from config import settings

from sqlalchemy.orm import Session

from apps.submissions.models import Submission


def judge_submission(id: UUID, collection: dict, code: bytes, schema: TypeVar('TSchema'), db: Session):
    if schema.language_type == 'py':
        response = run_python(code, collection.data_entry)
    elif schema.language_type == 'c':
        response = run_c(code, collection.data_entry)
    elif schema.language_type == 'cpp':
        response = run_cpp(code, collection.data_entry)

    status = judge(response=response, expected_output=collection.data_output)

    db.query(Submission).filter(Submission.id == id).update({'status': status})
    db.commit()


def run_python(code, data_input):
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
            return pipe.communicate(data_input.encode(), timeout=settings.TLE_TIMEOUT)
        except subprocess.TimeoutExpired:
            pipe.kill()
            return 'TLE'


def run_c(code, data_input):
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
            return pipe.communicate(data_input.encode(), timeout=settings.TLE_TIMEOUT)
        except subprocess.TimeoutExpired:
            pipe.kill()
            return 'TLE'


def run_cpp(code, data_input):
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
            return pipe.communicate(data_input.encode(), timeout=settings.TLE_TIMEOUT)
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
    elif (
        response[0]
        and (response[0].decode().count('\n') != expected_output.count('\n') or response[0].decode()[-1] != '\n')
        and response[0].decode().replace('\n', '') == expected_output.replace('\n', '')
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
