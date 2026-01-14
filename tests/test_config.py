"""Tests for configuration utilities."""

import logging
import tempfile
from logging import CRITICAL, INFO, WARNING
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from rascal2.config import setup_logging


@pytest.mark.parametrize("level", [INFO, WARNING, CRITICAL])
@patch("rascal2.config.get_global_settings")
def test_setup_logging(mock_get_global, level):
    """Test that the logger is set up correctly."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "settings.ini"
        global_setting = MagicMock()
        global_setting.fileName.return_value = path
        mock_get_global.return_value = global_setting
        setup_logging(level)
        assert Path(tmp_dir, "rascal.log").is_file()

        log = logging.getLogger()
        assert log.level == level
        assert log.hasHandlers()
        logging.shutdown()
