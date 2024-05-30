import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
import httpx

import git
import openai

from aider import models
from aider.coders import Coder
from aider.coders.base_coder import ExhaustedContextWindow
from aider.dump import dump  # noqa: F401
from aider.io import InputOutput
from tests.utils import ChdirTemporaryDirectory, GitTemporaryDirectory


class TestCoder(unittest.TestCase):
    def setUp(self):
        self.patcher = patch("aider.coders.base_coder.check_model_availability")
        self.mock_check = self.patcher.start()
        self.mock_check.return_value = True

    def tearDown(self):
        self.patcher.stop()


    def test_allowed_to_edit(self):
        with GitTemporaryDirectory():
            repo = git.Repo()

            fname = Path("added.txt")
            fname.touch()
            repo.git.add(str(fname))

            fname = Path("repo.txt")
            fname.touch()
            repo.git.add(str(fname))

            repo.git.commit("-m", "init")

            # YES!
            io = InputOutput(yes=True)
            coder = Coder.create(models.GPT4, None, io, fnames=["added.txt"])

            self.assertTrue(coder.allowed_to_edit("added.txt"))
            self.assertTrue(coder.allowed_to_edit("repo.txt"))
            self.assertTrue(coder.allowed_to_edit("new.txt"))

            self.assertIn("repo.txt", str(coder.abs_fnames))
            self.assertIn("new.txt", str(coder.abs_fnames))

            self.assertFalse(coder.need_commit_before_edits)


    def test_run_with_file_deletion(self):
        # Create a few temporary files

        tempdir = Path(tempfile.mkdtemp())

        file1 = tempdir / "file1.txt"
        file2 = tempdir / "file2.txt"

        file1.touch()
        file2.touch()

        files = [file1, file2]

        # Initialize the Coder object with the mocked IO and mocked repo
        coder = Coder.create(models.GPT4, None, io=InputOutput(), fnames=files)

        def mock_send(*args, **kwargs):
            coder.partial_response_content = "ok"
            coder.partial_response_function_call = dict()

        coder.send = MagicMock(side_effect=mock_send)

        # Call the run method with a message
        coder.run(with_message="hi")
        self.assertEqual(len(coder.abs_fnames), 2)

        file1.unlink()

        # Call the run method again with a message
        coder.run(with_message="hi")
        self.assertEqual(len(coder.abs_fnames), 1)


    # Added this test to see if RepoMap will include references to classes.
    # It does not (i.e. neither get_repo_map nor get_ranked_tags_map will include ExhaustedContextWindow
    # in the defs from base_coder.py for this file).  Pretty sure the issue is that the scm query for
    # Python does not match the reference to ExhaustedContextWindow in the assertRaises call.
    def test_send_new_user_message(self):
        with ChdirTemporaryDirectory():
            # Mock the IO object
            mock_io = MagicMock()

            # Initialize the Coder object with the mocked IO and mocked repo
            coder = Coder.create(models.GPT4, None, mock_io)

            # Call the run method and assert that InvalidRequestError is raised
            with self.assertRaises(ExhaustedContextWindow):
                coder.send_new_user_message(inp="hi")



if __name__ == "__main__":
    unittest.main()
