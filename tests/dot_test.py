from unittest import mock

import pytest

from dismod import dot
from dismod.dependency import DependencyContainer


@mock.patch.object(dot.os, "mkdir")
@pytest.mark.parametrize(
    ("filepath", "imports", "renders_dir_exists"),
    (
        (
            "test/test.py",
            [{"from_statement": None, "import_statements": ["os"]}],
            True,
        ),
        (
            "test/test.py",
            [
                {
                    "from_statement": "os",
                    "import_statements": ["path", "abspath"],
                },
            ],
            False,
        ),
    ),
)
def test_render_multiple_files(
    os_mkdir_mock,
    filepath,
    imports,
    renders_dir_exists,
):
    with mock.patch.object(dot, "open"), mock.patch.object(
        dot.os.path,
        "exists",
        return_value=renders_dir_exists,
    ):
        dependency_container = DependencyContainer(filepath=filepath)
        dependency_container.add_import(imports)
        dot.render_multiple_files("test", [dependency_container])


@mock.patch.object(dot.os, "mkdir")
@pytest.mark.parametrize(
    ("filepath", "imports", "renders_dir_exists"),
    (
        (
            "test/test.py",
            [{"from_statement": None, "import_statements": ["os"]}],
            True,
        ),
        (
            "test/test.py",
            [
                {
                    "from_statement": "os",
                    "import_statements": ["path", "abspath"],
                },
            ],
            False,
        ),
    ),
)
def test_render_cluster_files(
    os_mkdir_mock,
    filepath,
    imports,
    renders_dir_exists,
):
    with mock.patch.object(dot, "open"), mock.patch.object(
        dot.os.path,
        "exists",
        return_value=renders_dir_exists,
    ):
        dependency_container = DependencyContainer(filepath=filepath)
        dependency_container.add_import(imports)
        dot.render_cluster_files("test", [dependency_container])
