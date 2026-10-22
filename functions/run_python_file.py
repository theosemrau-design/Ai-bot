import os
import subprocess
schema_run_python_file: dict[str, str | dict[str, str | dict[str, str | list[str] | dict[str, dict[str, str]]]]] = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute and with that run a python file(the ending is .py) path is raltive to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath to python file to execute relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "List of arguments to run python file with",
                },
            },
            "required": [
                "file_path",
            ],
        },
    },
}
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command: list[str] = ["python", target_file]
        if args:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        return_message: str = ""
        if completed_process.returncode != 0:
            return_message += f"\nProcess exited with code {completed_process.returncode}"
        if completed_process.stdout:
            return_message += f"\nSTDOUT: {completed_process.stdout}"
        if completed_process.stderr:
            return_message += f"\nSTDERR: {completed_process.stderr}"
        if not completed_process.stdout and not completed_process.stderr:
            return_message += "\nNo output produced"
        return return_message

    except Exception as err:
        return f"Error: executing Python file: {err}"