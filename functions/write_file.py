import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
  
    abs_path = os.path.abspath(working_directory)

