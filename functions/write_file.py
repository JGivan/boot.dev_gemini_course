import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(file_path_abs):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:
        
        parent_dir = os.path.dirname(file_path_abs)
        os.makedirs(parent_dir, exist_ok=True)

        with open(file_path_abs, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except:

        return f'Error: failed to write to {file_path}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the provided content to the specified file path (relative to the working directory)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file whose contents should be read, relative to the working directory",
            ),
            "content" : types.Schema(
                type = types.Type.STRING,
                description = "The content that should be written to the specified file path"
            )
        },
    required=["file_path", "content"]
    ),
)


