import os
schema_get_files_info: dict[str, str | dict[str, str | dict[str, str | dict[str, dict[str, str]]]]] = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        return_string: str = f"Result for current directory:"
        for i in os.listdir(target_dir):
            name: str = i
            size: int = os.path.getsize(target_dir)
            is_dir: bool = os.path.isdir("/".join([target_dir, i]))
            return_string += f"\n  - {name}: file_size={size} bytes, is_dir={is_dir}"

        return return_string
    except Exception as err:
        return f"Error: getting files info: {err}"