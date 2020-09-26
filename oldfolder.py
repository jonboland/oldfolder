import argparse
import os
import pathlib
import shutil
import sys
import time


SECONDS = 365 * 24 * 60 * 60
TIME_TYPES = {"modified": "st_mtime", "accessed": "st_atime", "created": "st_ctime"}


def prepare_move(number, path, storage_folder, time_type):
    length = SECONDS * number
    now = time.time()
    my_directory = pathlib.Path(path)
    my_subdirectories = (item for item in my_directory.iterdir() if item.is_dir())
    file_operations = []
    for subdirectory in my_subdirectories:
        time_stats = _get_stats(subdirectory, time_type)
        if all(time_stat < (now - length) for time_stat in time_stats):
            *_, subdirectory_name = subdirectory.parts
            _check_storage_folder_name(storage_folder, subdirectory_name)
            source = subdirectory
            destination = my_directory / storage_folder / subdirectory_name
            file_operations.append((source, destination, subdirectory_name))
    return file_operations


def _get_stats(subdirectory, time_type):
    time_stats = []
    for folder, _, files in os.walk(subdirectory):
        for file in files:
            file_path = pathlib.Path(folder) / file
            time_stat = getattr(file_path.stat(), TIME_TYPES[time_type])
            time_stats.append(time_stat)
    return time_stats


def _check_storage_folder_name(storage_folder, subdirectory_name):
    if storage_folder == subdirectory_name:
        print(
            "The operation has been aborted because a folder\n"
            f"named {storage_folder} already exists in that location.\n"
            "Please try again using a different storage_folder name."
        )
        sys.exit()


def move_files(file_operations):
    for operation in file_operations:
        source, destination, _ = operation
        shutil.move(source, destination)
    print("Operation complete")


def main(number, path, storage_folder, time_type):
    file_operations = prepare_move(number, path, storage_folder, time_type)
    if not file_operations:
        print(
            f"All subdirectories contain files with {time_type} times\n"
            "in the specified period so the operation was aborted"
        )
    else:
        print(
            f"Based on the {time_type} times of the files contained within them,\n"
            f"the subdirectories that will be moved to the {storage_folder} folder are:"


        )
        for operation in file_operations:
            *_, subdirectory_name = operation
            print("\t", subdirectory_name)
        proceed = input("Would you like to proceed?: Y/N ")
        if proceed.upper() in ("Y", "YES"):
            move_files(file_operations)
        else:
            print("Operation aborted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move old subfolders that contain files "
        "which haven't been modified for a given period. "
        "Moves can also be specified based on created or accessed time."
    )
    parser.add_argument(
        "number",
        type=float,
        help="Number of years since files in subfolders were last modified, accessed, or created."
    )
    parser.add_argument(
        "path", type=str, help="Path of directory where subfolders can be found."
    )
    parser.add_argument(
        "storage",
        type=str,
        help="Name of storage folder to place the old subfolders inside. "
        "The storage folder location will be the specifed path.",
    )
    parser.add_argument(
        "-t",
        "--time_type",
        type=str,
        choices=["modified", "accessed", "created"],
        default="modified",
        help="Time stat type to base the move on.",
    )

    args = parser.parse_args()

    main(args.number, args.path, args.storage, args.time_type)
