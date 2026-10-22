from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *
from collections.abc import Callable
from config import *
import json
available_functions: list[Callable[[str, str], str]] = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]
function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}
def call_function(tool_call, verbose: bool = False) -> dict[str, str|dict[str, str]]:
    function_name: str = tool_call.function.name
    function_args: dict[str, dict[str, str]] = json.loads(tool_call.function.arguments or "{}")
    function_args["working_directory"] = WORKING_DIRECTORY

    if function_name not in function_map:
        return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": f"Error: Unknown function: {function_name}",
}
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    result: str = function_map[function_name](**function_args)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }