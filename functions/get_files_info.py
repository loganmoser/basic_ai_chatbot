import os 

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_abspath, directory))

        valid_target_dir = os.path.commonpath([working_abspath, target_dir]) == working_abspath

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if  not os.path.isdir(target_dir):
            return f'Error: {directory} is not a directory'
        
        file_info: list[str] = []

        for file in os.listdir(target_dir):
            file_path = '/'.join([target_dir, file])
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            file_info.append(
                f"- {file_path}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(file_info)
        
    except Exception as e:
        return f'Error: {e}'
