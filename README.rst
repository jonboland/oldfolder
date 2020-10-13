Old Folder
==========

.. figure:: https://raw.githubusercontent.com/jonboland/oldfolder/master/docs/oldfiles.png
  :alt: Black and white picture of stacks of old folders

|

Old Folder spring cleans a file directory by storing away subdirectories
that haven't been modified for a given period.

Usage
~~~~~

Python 3.6+ must be preinstalled.

Old Folder can then be pip installed from `PyPI`_ and used via a command line interface:

.. code-block:: shell-session

 F:\>oldfolder -h
 usage: oldfolder [-h] [-t {modified,accessed,created}] path number storage

 Move old subdirectories that contain files which haven't been modified for
 a given period of time.
 Moves can also be specified based on created or accessed time.

 positional arguments:
  path                  Path of directory where subdirectories can be found.
  number                Number of years since files in subdirectories were
                        modified, accessed, or created.
  storage               Name of storage folder to place the old
                        subdirectories inside. The storage folder
                        location will be the specifed path.

 optional arguments:
  -h, --help            show this help message and exit
  -t {modified,accessed,created}, --time_type {modified,accessed,created}
                        Time stat type to base the move on.

Or you can run it directly:

.. code-block:: shell-session

 F:\>py oldfolder.py -h

Pass the path of the main directory, the length of time and the storage folder name to the program:

.. code-block:: shell-session

 F:\>oldfolder "F:\main_directory" 1.5 "old_stuff"

Subdirectories that don't contain any files modified during the period will be listed for storage:

.. code-block:: shell-session

 Based on the modified times of the files contained within them,
 the subdirectories that will be moved to the old_stuff folder are:
          old_files_1
          old_files_2
 Would you like to proceed?: Y/N

Before
~~~~~~

.. code-block:: shell-session

 F:\main_directory>tree /F
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

 F:\main_directory>tree /F
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

You can read more about the program towards the end of this `shutil article`_.

Importing
~~~~~~~~~

You can also use Old Folder's functions in your own projects:


.. code-block:: python

    import oldfolder


    file_operations = oldfolder.prepare_move("F:\main_directory" 1.5 "old_stuff")

    oldfolder.move_files(file_operations)


License
~~~~~~~

Old Folder is offered under the `BSD 3 Clause license`_.


Protecting Your Data
~~~~~~~~~~~~~~~~~~~~

As with other utilities that employ Python's shutil module to carry out high-level
file operations, proceeding with caution and creating a backup
of your data prior to use is strongly recommended.


Operating System
~~~~~~~~~~~~~~~~

Old Folder is intended to be operating system independent, but has so far only
been tested on Windows.




.. _`PyPI`: https://pypi.org/project/oldfolder/
.. _`shutil article`: https://blog.finxter.com/python-shutil-high-level-file-operations-demystified
.. _`BSD 3 Clause License`: https://github.com/jonboland/oldfolder/blob/master/LICENSE
