from unittest import mock

import pytest

from dismod import dot
from dismod.dependency import DependencyContainer


@mock.patch.object(dot.os, "mkdir")
@pytest.mark.parametrize(
    ("split_files", "renders_dir_exists"),
    (
        (True, True),
        (False, False),
    ),
)
def test_render(os_mkdir_mock, split_files, renders_dir_exists):
    with mock.patch.object(dot, "open"), mock.patch.object(
        dot.os.path,
        "exists",
        return_value=renders_dir_exists,
    ):
        dot.render(
            project_name="test",
            dependency_containers=[],
            rankdir="test",
            overlap="test",
            ratio="test",
            fontsize="16",
            dpi="150",
            shape="test",
            fontname="test",
            split_files=split_files,
        )


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
def test_render_multiple_files(
    filepath,
    imports,
):
    with mock.patch.object(dot, "open"):
        dependency_container = DependencyContainer(filepath=filepath)
        dependency_container.add_import(imports)
        dot._render_multiple_files(
            "test",
            [dependency_container],
            "LR",
            "scale",
            "fill",
            "16",
            "150",
            "rectangle",
            "Consolas",
        )


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
def test_render_cluster_files(
    filepath,
    imports,
):
    with mock.patch.object(dot, "open"):
        dependency_container = DependencyContainer(filepath=filepath)
        dependency_container.add_import(imports)
        dot._render_cluster_files(
            "test",
            [dependency_container],
            "LR",
            "scale",
            "fill",
            "16",
            "150",
            "rectangle",
            "Consolas",
        )
