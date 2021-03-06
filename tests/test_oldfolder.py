from argparse import Namespace
from pathlib import Path
import pytest

import context
import oldfolder


@pytest.fixture
def fake_directory(fs):
    fs.create_dir(Path(r"F:\main_directory\new_files"))
    fs.create_dir(Path(r"F:\main_directory\old_files"))


@pytest.fixture
def fake_time(monkeypatch):
    # Set point in time to Wednesday, October 7, 2020 9:07:33 AM GMT+01:00 DST
    def fake_now():
        return 1602058053.0

    monkeypatch.setattr(oldfolder.time, "time", fake_now)


@pytest.fixture
def fake_parse_args(monkeypatch):
    def fake_args():
        return Namespace(
            path=Path(r"F:\main_directory"),
            number=1,
            storage="old_stuff",
            time_type="modified",
        )

    monkeypatch.setattr(oldfolder, "parse_arguments", fake_args)


def test_prepare_move_storage_folder_name_already_exists(fs, fake_directory):
    """Fails if FolderAlreadyExistsError not raised with correct error message."""
    # Add folder with same name as storage folder to the fake directory
    fs.create_dir(Path(r"F:\main_directory\old_stuff"))

    with pytest.raises(oldfolder.FolderAlreadyExistsError) as excinfo:
        oldfolder.prepare_move(Path(r"F:\main_directory"), 1, "old_stuff", "modified")

    assert (
        str(excinfo.value)
        == "The operation was aborted because a folder named old_stuff "
        "already exists in that location.\n"
    )


def test_prepare_move_with_file_operations(fs, fake_time, monkeypatch):
    """Fails if correct file operation is not prepared."""
    # Create a fake directory containing a single folder
    fs.create_dir(Path(r"F:\main_directory\old_files_1"))

    # Return fake stats mimicking files all created before the given time period
    def fake_stats(subdirectory, time_type):
        return [1546348608.0, 1514785000.0, 1514812608.0]

    monkeypatch.setattr(oldfolder, "_get_stats", fake_stats)

    result = oldfolder.prepare_move(
        Path(r"F:\main_directory"), 1, "old_stuff", "created"
    )
    assert result == [
        (
            Path(r"F:\main_directory\old_files_1"),
            Path(r"F:\main_directory\old_stuff\old_files_1"),
        )
    ]


def test_prepare_move_no_file_operations(fs, fake_time, monkeypatch):
    """Fails if list of file operations is not blank."""
    # Create a fake directory containing a single folder
    fs.create_dir(Path(r"F:\main_directory\old_files_1"))

    # Return fake stats mimicking files all accessed within the given time period
    def fake_stats(subdirectory, time_type):
        return [1646348608.0, 1614785000.0, 1614812608.0]

    monkeypatch.setattr(oldfolder, "_get_stats", fake_stats)

    result = oldfolder.prepare_move(
        Path(r"F:\main_directory"), 1, "old_stuff", "accessed"
    )
    assert result == []


def test_move_files_one_folder_placed_in_storage(fake_directory):
    """Fails if correct subdirectories not present."""
    file_operations = [
        (
            Path(r"F:\main_directory\old_files"),
            Path(r"F:\main_directory\old_stuff\old_files"),
        )
    ]

    oldfolder.move_files(file_operations)

    assert Path(r"F:\main_directory\new_files").exists()
    assert Path(r"F:\main_directory\old_stuff\old_files").exists()
    assert not Path(r"F:\main_directory\old_files").exists()


def test_main_storage_folder_name_already_exists(
    fs, fake_directory, fake_parse_args, capsys
):
    """Fails if SystemExit not raised or folder exists message not displayed."""
    # Add folder with same name as storage folder to the fake directory
    fs.create_dir(Path(r"F:\main_directory\old_stuff"))

    with pytest.raises(SystemExit):
        oldfolder.main()

    captured = capsys.readouterr()
    assert captured.out == (
        "The operation was aborted because a folder named "
        "old_stuff already exists in that location.\n"
        "Please try again using a different storage folder name.\n"
    )


def test_main_file_path_not_found(fake_directory, monkeypatch, capsys):
    """Fails if SystemExit not raised or check path message not displayed."""

    def fake_args():
        return Namespace(
            path=Path(r"F:\main_directories"),
            number=1,
            storage="old_stuff",
            time_type="modified",
        )

    monkeypatch.setattr(oldfolder, "parse_arguments", fake_args)

    with pytest.raises(SystemExit):
        oldfolder.main()

    captured = capsys.readouterr()
    assert captured.out == (
        "The operation was aborted because the system cannot find "
        f"the specified file path: F:\\main_directories\n"
        "Please check the path and try again.\n"
    )


def test_main_no_file_operations_aborted_message_displayed(
    fake_directory, monkeypatch, capsys
):
    def fake_args():
        return Namespace(
            path=Path(r"F:\main_directory"),
            number=1,
            storage="old_stuff",
            time_type="accessed",
        )

    monkeypatch.setattr(oldfolder, "parse_arguments", fake_args)

    def fake_prepare(path, number, storage_folder, time_type):
        return []

    monkeypatch.setattr(oldfolder, "prepare_move", fake_prepare)

    oldfolder.main()

    captured = capsys.readouterr()
    assert captured.out == (
        "All subdirectories contain files with accessed times\n"
        "in the specified period so the operation was aborted\n"
    )


def test_main_correct_move_summary_displayed(
    fake_directory, fake_parse_args, monkeypatch, capsys
):
    def fake_prepare(path, number, storage_folder, time_type):
        return [
            (
                Path(r"F:\main_directory\old_files_1"),
                Path(r"F:\main_directory\old_stuff\old_files_1"),
            )
        ]

    monkeypatch.setattr(oldfolder, "prepare_move", fake_prepare)

    def fake_input(response):
        print("Would you like to proceed?: Y/N ")
        return "NO"

    monkeypatch.setattr(oldfolder, "input", fake_input)

    oldfolder.main()

    captured = capsys.readouterr()
    assert captured.out == (
        "Based on the modified times of the files contained within them,\n"
        "the subdirectories that will be moved to the old_stuff folder are:\n"
        "\t old_files_1\n"
        "Would you like to proceed?: Y/N \n"
        "Operation aborted\n"
    )


if __name__ == "__main__":
    pytest.main()
