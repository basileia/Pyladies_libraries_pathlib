from pathlib import Path
from collections import defaultdict


def get_files_info(folderPath):
    """
    Returns list of tuples - file suffix or empty string and its size
    """
    files_info = []
    for file in folderPath.iterdir():

        if file.is_file():
            suffix = file.suffix
            files_info.append((suffix, Path(file).stat().st_size))
        else:
            files_info.extend(get_files_info(file))
    return files_info


def group_by_suffixes(files_info):
    """
    Returns tuples grouped by suffixes (suffix, sum of file sizes)
    """
    dictionary = defaultdict(int)
    for suffix, size in files_info:
        dictionary[suffix] = dictionary[suffix] + size
    tuples = (list(dictionary.items()))
    return tuples


def convert_size(size_bytes_in_dict):
    """
    Converts size from bytes to more human readable. Input and output is
    dictionary.
    """
    unit_list = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    i = 0
    for suffix in size_bytes_in_dict:
        while size_bytes_in_dict[suffix] >= 1024 and i < len(unit_list) - 1:
            size_bytes_in_dict[suffix] /= 1024.
            i += 1
        f = ('%.2f' % size_bytes_in_dict[suffix]).rstrip('0').rstrip('.')
        size_bytes_in_dict[suffix] = '%s %s' % (f, unit_list[i])
        i = 0
    return size_bytes_in_dict


if __name__ == "__main__":
    path = Path().absolute()
    files_info = get_files_info(path)
    result_bytes = group_by_suffixes(files_info)
    result = convert_size(dict(result_bytes))
    print(result)
    
