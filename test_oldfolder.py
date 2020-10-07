import pytest
from pathlib import Path

import oldfolder


@pytest.fixture
def fake_directory(fs):
    fs.create_dir(Path(r"F:\main_directory\new_files"))
    fs.create_dir(Path(r"F:\main_directory\old_files"))


@pytest.fixture
def fake_time(monkeypatch):
    def fake_now():
        return 1602058053.0
    monkeypatch.setattr(oldfolder.time, "time", fake_now)


def test_prepare_move_existing_storage_folder(fs, fake_directory, capsys):
    fs.create_dir(Path(r"F:\main_directory\old_stuff"))

    with pytest.raises(SystemExit):
        oldfolder.prepare_move(Path(r"F:\main_directory"), 1, "old_stuff", "modified")

    captured = capsys.readouterr()
    assert captured.out == (
        "The operation has been aborted because a folder\n"
        "named old_stuff already exists in that location.\n"
        "Please try again using a different storage folder name.\n"
    )


def test_prepare_move(fs, fake_time, monkeypatch):
    fs.create_dir(Path(r"F:\main_directory\old_files_1"))

    def fake_stats(subdirectory, time_type):
        return [1546348608.0, 1514785000.0, 1514812608.0]

    monkeypatch.setattr(oldfolder, "_get_stats", fake_stats)

    result = oldfolder.prepare_move(Path(r"F:\main_directory"), 1, "old_stuff", "created")
    assert result == [
        (
            Path(r"F:\main_directory\old_files_1"),
            Path(r"F:\main_directory\old_stuff\old_files_1"),
        )
    ]


def test_prepare_move_no_file_operations(fs, fake_time, monkeypatch):
    fs.create_dir(Path(r"F:\main_directory\old_files_1"))

    def fake_stats(subdirectory, time_type):
        return [1646348608.0, 1614785000.0, 1614812608.0]

    monkeypatch.setattr(oldfolder, "_get_stats", fake_stats)

    result = oldfolder.prepare_move(Path(r"F:\main_directory"), 1, "old_stuff", "accessed")
    assert result == []


def test_move_files(fake_directory, capsys):
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

    captured = capsys.readouterr()
    assert captured.out == ("Operation complete\n")


def test_main(monkeypatch, capsys):
    def fake_prepare(path, number, storage_folder, time_type):
        return [
            (
                Path(r"F:\main_directory\old_files_1"),
                Path(r"F:\main_directory\old_stuff\old_files_1"),
            )
        ]

    monkeypatch.setattr(oldfolder, "prepare_move", fake_prepare)

    try:
        oldfolder.main(Path(r"F:\main_directory"), 1, "old_stuff", "modified")
    except OSError:
        pass

    captured = capsys.readouterr()
    assert captured.out == (
        "Based on the modified times of the files contained within them,\n"
        "the subdirectories that will be moved to the old_stuff folder are:\n"
        "\t old_files_1\n"
        "Would you like to proceed?: Y/N "
    )


def test_main_no_file_operations(monkeypatch, capsys):
    def fake_prepare(path, number, storage_folder, time_type):
        return []

    monkeypatch.setattr(oldfolder, "prepare_move", fake_prepare)

    oldfolder.main(Path(r"F:\main_directory"), 1, "old_stuff", "accessed")

    captured = capsys.readouterr()
    assert captured.out == (
        "All subdirectories contain files with accessed times\n"
        "in the specified period so the operation was aborted\n"
    )


if __name__ == "__main__":
    pytest.main()
