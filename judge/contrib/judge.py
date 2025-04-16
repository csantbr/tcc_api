import subprocess
import tempfile
import sys
import os
from uuid import UUID

from judge.submissions.repositories import SubmissionRepository
from judge.submissions.schemas import SubmissionOut
from judge.config import settings
from judge.contrib.base64 import Base64Utils
from judge.contrib.constants import (
    STATUS_TIME_LIMIT_EXCEEDED,
    STATUS_COMPILATION_ERROR,
    STATUS_ACCEPTED,
    STATUS_PRESENTATION_ERROR,
    STATUS_WRONG_ANSWER,
)


class Judge:
    def __init__(self, repository: SubmissionRepository) -> None:
        self.repository = repository

    async def process_submission(self, submission: SubmissionOut, data: dict):
        runner = self._get_runner(submission.language_type)
        if not runner:
            raise ValueError(f"Unsupported language type: {submission.language_type}")

        code = Base64Utils.decode(submission.content)
        response = runner.run(code, data['data_entry'])
        expected_output = self._decode_output(data['data_output'])

        status = self._evaluate(response, expected_output)
        await self._update_submission_status(submission.id, status)

    def _get_runner(self, language_type: str):
        runners = {
            'py': PythonRunner(),
            'c': CRunner(),
            'cpp': CppRunner(),
        }
        return runners.get(language_type)

    def _decode_output(self, encoded_output: str) -> str:
        decoded = Base64Utils.decode(encoded_output).decode()
        return decoded.replace('\\n', '\n').replace('\r', '').rstrip('\n') + '\n'

    def _evaluate(self, response, expected_output: str) -> str:
        output, error = response if response != "TLE" else (None, None)

        if response == "TLE":
            return STATUS_TIME_LIMIT_EXCEEDED
        if not output:
            if error:
                print(f"Compilation error: {error.decode()}")
            return STATUS_COMPILATION_ERROR

        output_decoded = output.decode().replace('\r', '').rstrip('\n') + '\n'

        if expected_output == output_decoded:
            return STATUS_ACCEPTED

        if (
            output_decoded.replace('\n', '') == expected_output.replace('\n', '')
            and output_decoded.count('\n') != expected_output.count('\n')
        ):
            return STATUS_PRESENTATION_ERROR

        return STATUS_WRONG_ANSWER

    async def _update_submission_status(self, submission_id: UUID, status: str):
        await self.repository.update(data={'status': status}, filter={'id': submission_id})


class CodeRunner:
    def run(self, code: bytes, data_input: str):
        raise NotImplementedError("Subclasses must implement 'run' method")

    def _execute(self, command_template: str, code: bytes, data_input: str, timeout: int):
        data_entry = Base64Utils.decode(data_input)
        tmp_file = None
        try:
            tmp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.py', delete=False)
            tmp_file.write(code if isinstance(code, bytes) else code.encode('utf-8'))
            tmp_file.flush()
            tmp_file.close()

            command = command_template.format(tmp_file.name)
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            try:
                result = process.communicate(data_entry, timeout=timeout)
                return result
            except subprocess.TimeoutExpired:
                process.kill()
                return "TLE", None
        finally:
            if tmp_file and os.path.exists(tmp_file.name):
                try:
                    os.unlink(tmp_file.name)
                except Exception as e:
                    print(f"Error deleting temporary file: {e}")


class PythonRunner(CodeRunner):
    def run(self, code: bytes, data_input: str):
        python_executable = sys.executable
        return self._execute(f'"{python_executable}" "{{0}}"', code, data_input, settings.TLE_TIMEOUT)


class CRunner(CodeRunner):
    def run(self, code: bytes, data_input: str):
        return self._execute("gcc -o {0}_exec {0} -lm && {0}_exec && rm {0}_exec", code, data_input, settings.TLE_TIMEOUT)


class CppRunner(CodeRunner):
    def run(self, code: bytes, data_input: str):
        return self._execute("g++ -o {0}_exec {0} -lm && {0}_exec && rm {0}_exec", code, data_input, settings.TLE_TIMEOUT)
