import pytest

from dismod.dependency import DependencyContainer


@pytest.mark.parametrize(("filepath"), (("test/test.py"),))
def test_dependency_container_initialize(filepath):
    dependency_container = DependencyContainer(filepath=filepath)

    assert dependency_container.filepath == filepath
    assert dependency_container.basename == "test.test.py"


@pytest.mark.parametrize(
    ("filepath", "imports"),
    (("test/test.py", [{"from_statement": "", "import_statements": []}]),),
)
def test_dependency_container_add_import(filepath, imports):
    dependency_container = DependencyContainer(filepath=filepath)
    assert dependency_container.filepath == filepath
    assert dependency_container.basename == "test.test.py"

    dependency_container.add_import(imports)

    assert dependency_container.imports == imports
