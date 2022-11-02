import pytest
import os
from core.utilities.basics import get_env_file


class TestBasicUtilities:
    def test_file_exists(self):
        with pytest.raises(Exception):
            get_env_file(key="ENV_FILE1")
