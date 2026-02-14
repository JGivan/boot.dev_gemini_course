import os
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):

    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_path_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:

        file = open(file_path_abs)
        content = file.read(10000)

        if file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    
    except:
        return "Error: failed to parse file contents"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(  
                type=types.Type.STRING,
                description="Path to the file whose contents should be read, relative to the working directory",
            ),
        },
    required=["file_path",]
    ),
)