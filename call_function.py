from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
import json
from collections.abc import Callable

available_functions = [schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file]


def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name 
    function_args = json.loads(tool_call.function.arguments or "{}")
    
    # Print arguments for the function if verbose output desired
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    if function_name not in function_map.keys(): # Return early if the function is not available 
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    function_args["working_directory"] = "./calculator"

    result = function_map[function_name](**function_args)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    }
