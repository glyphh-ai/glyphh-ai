"""
Property-based tests for marketplace example models.

These tests validate universal properties across all example models
in the glyphh-ai/examples directory.
"""

import os
import re
import ast
import pytest

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


def get_all_model_files():
    """Get all .py files in examples directory."""
    if not os.path.exists(EXAMPLES_DIR):
        return []
    return [
        f for f in os.listdir(EXAMPLES_DIR)
        if f.endswith('.py') and f != '__init__.py' and f != 'README.md'
    ]


# Feature: marketplace-example-models, Property 2: Filename Snake Case Format
@pytest.mark.parametrize("filename", get_all_model_files())
def test_filename_snake_case(filename):
    """For any model file, filename matches snake_case pattern."""
    pattern = r'^[a-z][a-z0-9_]*\.py$'
    assert re.match(pattern, filename), f"{filename} is not snake_case"


# Feature: marketplace-example-models, Property 1: Model File Structure Completeness
@pytest.mark.parametrize("filename", get_all_model_files())
def test_model_file_structure(filename):
    """For any model file, required components exist."""
    filepath = os.path.join(EXAMPLES_DIR, filename)
    with open(filepath, 'r') as f:
        content = f.read()
        tree = ast.parse(content)

    # Check docstring exists
    assert ast.get_docstring(tree), f"{filename} missing module docstring"

    # Check for required imports and calls
    assert 'EncoderConfig' in content, f"{filename} missing EncoderConfig"
    assert 'Concept' in content, f"{filename} missing Concept"
    assert '.export(' in content, f"{filename} missing export call"
    assert 'print(' in content, f"{filename} missing print statements"


def test_model_count():
    """Verify we have exactly 50 model files."""
    files = get_all_model_files()
    assert len(files) == 50, f"Expected 50 models, found {len(files)}"
