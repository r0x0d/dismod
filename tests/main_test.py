from unittest import mock

import pytest

from dismod import main


def test_create_argument_parser():
    parser = main.create_argument_parser()
    assert "dismod" in parser.prog


@mock.patch.object(main, "get_instructions_from_file")
@mock.patch.object(main, "parse_instructions")
@mock.patch.object(main, "DependencyContainer")
@pytest.mark.parametrize(
    ("files", "instructions", "expected"),
    (
        (["file1.py", "file2.py"], ["something"], 2),
        (["file1.py", "file2.py"], [], 0),
    ),
)
def test_get_import_dependency_list(
    get_instructions_from_file_mock,
    parse_instructions_mock,
    dependency_container_mock,
    files,
    instructions,
    expected,
):
    with mock.patch.object(
        main,
        "get_import_instructions",
        return_value=instructions,
    ):
        assert len(main.get_import_dependency_list(files)) == expected


@mock.patch("dismod.main.create_argument_parser")
@mock.patch("dismod.main.get_import_dependency_list")
@mock.patch("dismod.main.render_multiple_files")
@mock.patch("dismod.main.collect_files_in_module")
def test_main(
    create_argument_parser_mock,
    get_import_dependency_list_mock,
    render_multiple_files_mock,
    collect_files_in_module_mock,
):
    assert main.main() == 0
    assert create_argument_parser_mock.called == 1
    assert get_import_dependency_list_mock.called == 1
    assert render_multiple_files_mock.called == 1
    assert collect_files_in_module_mock.called == 1
