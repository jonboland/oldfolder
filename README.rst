Old Folder
==========

.. figure:: docs/oldfolder.png
  :alt: Sepia tone picture of an old folder

|

Spring cleans a file directory by storing away its old subdirectories
if they haven’t been modified for a given period of time.

Old Folder can be used via a command line interface:

.. code-block:: shell-session

 F:\>py oldfolder.py -h
 usage: oldfolder.py [-h] [-t {modified,accessed,created}] path number storage

 Move old subdirectories that contain files which haven't been modified for a given period of time.
 Moves can also be specified based on created or accessed time.

 positional arguments:
  path                  Path of directory where subdirectories can be found.
  number                Number of years since files in subdirectories were modified, accessed, or created.
  storage               Name of storage folder to place the old subdirectories inside. The storage folder
                        location will be the specifed path.

 optional arguments:
  -h, --help            show this help message and exit
  -t {modified,accessed,created}, --time_type {modified,accessed,created}
                        Time stat type to base the move on.

Pass the path of the main directory, the length of time and the storage folder name to the program:

.. code-block:: shell-session

 F:\>py oldfolder.py "F:\main_directory" 1 "old_stuff"

Subdirectories that don't contain any files modified in the period will be listed for storage:

.. code-block:: shell-session

 Based on the modified times of the files contained within them,
 the subdirectories that will be moved to the old_stuff folder are:
          old_files_1
          old_files_2
 Would you like to proceed?: Y/N

You see a simple before and after example below:

Before
~~~~~~

.. code-block:: shell-session

 F:\my_directory>tree /F
 ...
 F:.
 ├───new_files_1
 │   │   new_file.jpg
 │   │
 │   ├───second_level_folder_1
 │   │       really_new_file.txt
 │   │
 │   └───second_level_folder_2
 │           very_new_file.txt
 │
 ├───new_files_2
 │       fairly_new_file.txt
 │
 ├───old_files_1
 │   │   old_file.txt
 │   │
 │   └───second_level_folder_1
 │       │   old_file_as_well.txt
 │       │
 │       └───third_level_folder
 │               really_old_file.jpg
 │
 └───old_files_2
     │   another_old_file.txt
     │
     └───old_second_level_folder
             oldest_file.jpg
             old_file_2.txt

After
~~~~~

.. code-block:: shell-session

 F:\my_directory>tree /F
 ...
 F:.
  ├───new_files_1
  │   │   new_file.jpg
  │   │
  │   ├───second_level_folder_1
  │   │       really_new_file.txt
  │   │
  │   └───second_level_folder_2
  │           very_new_file.txt
  │
  ├───new_files_2
  │       fairly_new_file.txt
  │
  └───old_stuff
      ├───old_files_1
      │   │   old_file.txt
      │   │
      │   └───second_level_folder_1
      │       │   old_file_as_well.txt
      │       │
      │       └───third_level_folder
      │               really_old_file.jpg
      │
      └───old_files_2
          │   another_old_file.txt
          │
          └───old_second_level_folder
                  oldest_file.jpg
                  old_file_2.txt
