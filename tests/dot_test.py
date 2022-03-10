from unittest import mock

import pytest

from dismod import dot
from dismod.dependency import DependencyContainer


@pytest.mark.parametrize(
    ("filepath", "imports"),
    (
        (
            "test/test.py",
            [{"from_statement": None, "import_statements": ["os"]}],
        ),
        (
            "test/test.py",
            [
                {
                    "from_statement": "os",
                    "import_statements": ["path", "abspath"],
                },
            ],
        ),
    ),
)
@mock.patch.object(dot, "graphviz")
def test_read_multiple_files(graphviz_mock, filepath, imports):
    dependency_container = DependencyContainer(filepath=filepath)
    dependency_container.add_import(imports)

    dot.render_multiple_files([dependency_container])
