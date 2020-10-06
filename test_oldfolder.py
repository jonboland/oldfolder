import pytest
from pathlib import Path

import oldfolder


@pytest.fixture
def fake_directory(fs):
    fs.create_dir(Path(r"F:\main_directory\new_files"))
    fs.create_dir(Path(r"F:\main_directory\old_files"))


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


def test_prepare_move(fs, monkeypatch):
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


def test_prepare_move_no_file_operations(fs, monkeypatch):
    fs.create_dir(Path(r"F:\main_directory\old_files_1"))

    def fake_stats(subdirectory, time_type):
        return [1646348608.0, 1614785000.0, 1614812608.0]

    monkeypatch.setattr(oldfolder, "_get_stats", fake_stats)

    result = oldfolder.prepare_move(Path(r"F:\main_directory"), 1, "old_stuff", "accessed")
    assert result == []


if __name__ == "__main__":
    pytest.main()
