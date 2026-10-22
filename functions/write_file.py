import os
schema_write_file: dict[str, str | dict[str, str | dict[str, str | list[str] | dict[str, dict[str, str]]]]] = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text to specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath to file to write text to relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to file"
                }
            },
            "required": [
                "file_path",
                "content",
            ],
        },
    },
}
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as err:
        return f"Error: writing to file: {err}"