import subprocess
import tempfile
from typing import TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from apps.submissions.models import Submission
from config import settings
from contrib.helpers import base64_decode

from loguru import logger


def judge_submission(id: UUID, collection: dict, code: bytes, schema: TypeVar('TSchema'), db: Session):
    if schema.language_type == 'py':
        response = run_python(code, collection.data_entry)
    elif schema.language_type == 'c':
        response = run_c(code, collection.data_entry)
    elif schema.language_type == 'cpp':
        response = run_cpp(code, collection.data_entry)

    expected_output = base64_decode(collection.data_output).decode('unicode_escape')
    status = judge(response=response, expected_output=expected_output)
    logger.info(status)

    db.query(Submission).filter(Submission.id == id).update({'status': status})
    db.commit()


def run_python(code, data_input):
    data_entry = base64_decode(data_input)
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
            return pipe.communicate(data_entry, timeout=settings.TLE_TIMEOUT)
        except subprocess.TimeoutExpired:
            pipe.kill()
            return 'TLE'


def run_c(code, data_input):
    data_entry = base64_decode(data_input)
    with tempfile.NamedTemporaryFile(suffix='.c') as tmp:
        tmp.write(code)
        tmp.file.seek(0)
        pipe = subprocess.Popen(
            f'gcc -o {tmp.name}_ {tmp.name} -lm && {tmp.name}_ && rm {tmp.name}_',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        try:
            return pipe.communicate(data_entry, timeout=settings.TLE_TIMEOUT)
        except subprocess.TimeoutExpired:
            pipe.kill()
            return 'TLE'


def run_cpp(code, data_input):
    data_entry = base64_decode(data_input)
    with tempfile.NamedTemporaryFile(suffix='.cpp') as tmp:
        tmp.write(code)
        tmp.file.seek(0)
        pipe = subprocess.Popen(
            f'g++ -o {tmp.name}_ {tmp.name} -lm && {tmp.name}_ && rm {tmp.name}_',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        try:
            return pipe.communicate(data_entry, timeout=settings.TLE_TIMEOUT)
        except subprocess.TimeoutExpired:
            pipe.kill()
            return 'TLE'


def judge(response, expected_output: str):
    if response == 'TLE':
        return 'TIME LIMIT EXCEEDED'
    elif not response[0].decode():
        return 'COMPILATION ERROR'
    elif expected_output == response[0].decode():
        return 'ACCEPTED'
    elif (
        response[0]
        and (response[0].decode().count('\n') != expected_output.count('\n') or response[0].decode()[-1] != '\n')
        and response[0].decode().replace('\n', '') == expected_output.replace('\n', '')
    ):
        return 'PRESENTATION ERROR'
    else:
        return 'WRONG ANSWER'
