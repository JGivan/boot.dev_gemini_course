import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", file_path_abs]
        if args:
            for arg in args:
                command.extend(arg)

        process_result = subprocess.run(command,capture_output=True,text=True, timeout=30)

        output_str = ""

        if process_result.returncode != 0:
            output_str += f'Processed exited with code {process_result.returncode}\n'
        
        if process_result.stdout == None and process_result.stderr == None:
            output_str += "No output produced"
        
        else:
            output_str += f"STDOUT: {process_result.stdout}STDERR: {process_result.stderr}"
        
        return output_str
    except:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the python file at the specified file path relative to the working directory, optionally providing arguments for the function",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file whose contents should be read, relative to the working directory",
            ),
            "args" : types.Schema(
                type = types.Type.ARRAY,
                items = types.Schema(
                    type=types.Type.STRING,
                ),
                description = "Additional arguments (as strings) to pass to the function being called"
            )
        },
    required=["file_path"]
    ),
)
