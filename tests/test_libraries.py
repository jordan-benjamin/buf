# File name: test_libraries.py
# Author: Jordan Juravsky
# Date created: 23-08-2018

"""Tests buf.libraries."""

from unittest import TestCase, mock
import unittest
from buf import libraries
import os
import sys
import tempfile

class TestMakeDir(TestCase):
    """Tests buf.libraries.make_library."""

    def test_already_exists(self):
        """Tests that the function raises an error if the directory it is trying to create already exists."""
        with mock.patch("buf.libraries.os.path.exists", return_value = True):
            with self.assertRaises(IsADirectoryError):
                libraries.make_library_dir()

    def test_proper_directory_creation(self):
        """Tests that the function properly creates a directory if none exists."""
        with mock.patch("buf.libraries.os.path.exists", return_value = False):
            with mock.patch("buf.libraries.os.mkdir") as mock_make_dir:
                libraries.make_library_dir()
                mock_make_dir.assert_called_with(libraries.library_dir)

class TestEnsureLibraryDirExists(TestCase):
    """Tests buf.libraries.ensure_library_dir_exists."""

    def test_existence_check(self):
        """Tests that the function checks whether library_dir exists."""
        with mock.patch("buf.libraries.os.path.exists", side_effect = SystemExit) as mock_check:
            with self.assertRaises(SystemExit):
                libraries.ensure_library_dir_exists()
            mock_check.assert_called_with(libraries.library_dir)

    def test_directory_creation(self):
        """Tests that the function actually makes library_dir if it doesn't exist."""
        with mock.patch("buf.libraries.os.path.exists", return_value = False):
            with mock.patch("buf.libraries.os.mkdir") as mock_make_dir:
                libraries.ensure_library_dir_exists()
                mock_make_dir.assert_called_with(libraries.library_dir)

class TestAddLibraryFile(TestCase):
    """Tests buf.libraries.add_library_file."""

    def test_library_dir_existence_check(self):
        """Tests that the function ensures that library_dir has already been created."""
        with mock.patch("buf.libraries.ensure_library_dir_exists", side_effect = SystemExit) as mock_check:

            with self.assertRaises(SystemExit):
                libraries.add_library_file("file.txt")

            mock_check.assert_called()

    def test_file_already_exists_check(self):
        """Tests that the function raises an error if the file it is trying to create already exists."""
        with mock.patch("buf.libraries.os.path.exists", return_value = True):
            with self.assertRaises(FileExistsError):
                libraries.add_library_file("file.txt")

    def test_proper_file_creation(self):
        """Tests that the function properly creates a directory if none exists."""
        test_file_name = "file.txt"
        test_file_path = os.path.join(sys.prefix, libraries.library_dir, test_file_name)
        with mock.patch("buf.libraries.os.path.exists", return_value = False):
            with mock.patch("buf.libraries.ensure_library_dir_exists"):
                with mock.patch("buf.libraries.open") as mock_open:
                    libraries.add_library_file(test_file_name)
                    mock_open.assert_called_with(test_file_path, "w")


if __name__ == '__main__':
    unittest.main()