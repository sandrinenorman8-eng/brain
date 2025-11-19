import pytest
import os
import tempfile
from utils.file_utils import safe_read, safe_write, validate_path

def test_safe_write_and_read():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test.txt")
        content = "Test content"
        
        safe_write(filepath, content, create_backup=False)
        
        assert os.path.exists(filepath)
        
        read_content = safe_read(filepath)
        assert read_content == content

def test_safe_write_with_backup():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test.txt")
        
        safe_write(filepath, "Original", create_backup=False)
        safe_write(filepath, "Updated", create_backup=True)
        
        backup_files = [f for f in os.listdir(tmpdir) if f.startswith("test.txt.backup_")]
        assert len(backup_files) == 1

def test_validate_path_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test.txt")
        result = validate_path(filepath, tmpdir)
        assert result == os.path.abspath(filepath)

def test_validate_path_traversal():
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "..", "outside.txt")
        with pytest.raises(ValueError, match="Path traversal detected"):
            validate_path(filepath, tmpdir)

def test_safe_read_file_not_found():
    with pytest.raises(FileNotFoundError):
        safe_read("nonexistent_file.txt")
