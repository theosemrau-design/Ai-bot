from config import *
import os
schema_get_file_content: dict[str, str | dict[str, str | dict[str, str | list[str] | dict[str, dict[str, str]]]]] = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists the contents of a file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath to file to get the content of relative to the working directory",
                },
            },
            "required": [
                "file_path",
            ],
        },
    },
}
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_string: str = f.read(MAX_FILE_READ_CHARS)
            if f.read(MAX_FILE_READ_CHARS + 1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'
        return file_content_string
        
    except Exception as err:
        return f"Error: getting file content: {err}"