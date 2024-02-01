import unittest
import tempfile
import os
import shutil
from pathlib import Path

import tc_directory_cleaner.directory_cleaner as TDC


class TestFileOperations(unittest.TestCase):
    def create_folders_and_files(self, root_dir, paths):
        for path in paths:
            full_path = os.path.join(root_dir, path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            Path(full_path).touch()

    def setUp(self):
        # test dir 1
        self.temp_dir1 = tempfile.mkdtemp()

        files_and_directories1 = [
            "junk1",
            "junk2",
            "junk_dir/junk4",
            "caches/cache1/blah2",
            "caches/cache2/blah" "tasks/task1/task123",
            "tasks/task2/task234",
            "generic-worker.cfg", "generic-worker.cfg.bak"
        ]
        self.create_folders_and_files(self.temp_dir1, files_and_directories1)

    def tearDown(self):
        # Remove the temporary directory and its contents after the test
        shutil.rmtree(self.temp_dir1)

    def test_directory_cleaner(self):
        exception_list = ["generic-worker.cfg", "tasks", "caches"]
        dc = TDC.DirectoryCleaner(self.temp_dir1, exception_list)
        result = dc.clean_directory()
        # print(result)
        assert result["deleted"] == [
            str(Path(self.temp_dir1) / "junk2"),
            str(Path(self.temp_dir1) / "generic-worker.cfg.bak"),
            str(Path(self.temp_dir1) / "junk1"),
            str(Path(self.temp_dir1) / "junk_dir/junk4"),
            
        ]
        assert result["skipped"] == [
            str(Path(self.temp_dir1) / "tasks"),
            str(Path(self.temp_dir1) / "generic-worker.cfg"),
            str(Path(self.temp_dir1) / "caches"),
        ]

    def test_directory_cleaner_non_existent(self):
        exception_list = ["generic-worker.cfg", "tasks", "caches"]
        dc = TDC.DirectoryCleaner('/tmp/z838a8ca8a88c', exception_list)
        result = dc.clean_directory()
        assert result['errors'] == ['/tmp/z838a8ca8a88c']

if __name__ == "__main__":
    unittest.main()
