from collections import namedtuple
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


@mock.patch.object(main, "get_import_dependency_list")
@mock.patch.object(main, "render")
@mock.patch.object(main, "collect_files_in_module")
@pytest.mark.parametrize(
    (
        "filepath",
        "split_files",
        "ignore_folder",
        "rankdir",
        "overlap",
        "ratio",
        "fontsize",
        "dpi",
        "shape",
        "fontname",
    ),
    (
        (
            "test",
            False,
            None,
            "LR",
            "scale",
            "fill",
            "16",
            "150",
            "rectangle",
            "Consolas",
        ),
        (
            "test",
            True,
            None,
            "LR",
            "scale",
            "fill",
            "16",
            "150",
            "rectangle",
            "Consolas",
        ),
        (
            "test",
            True,
            "ignore_folder",
            "LR",
            "scale",
            "fill",
            "16",
            "150",
            "rectangle",
            "Consolas",
        ),
    ),
)
def test_main(
    get_import_dependency_list_mock,
    render_mock,
    collect_files_in_module_mock,
    filepath,
    split_files,
    ignore_folder,
    rankdir,
    overlap,
    ratio,
    fontsize,
    dpi,
    shape,
    fontname,
):
    with mock.patch.object(
        main.argparse,
        "ArgumentParser",
    ) as argument_parser_mock:
        argument_parser_mock.return_value.parse_args.return_value = namedtuple(
            "ArgumentParser",
            [
                "filepath",
                "split_files",
                "ignore_folder",
                "rankdir",
                "overlap",
                "ratio",
                "fontsize",
                "dpi",
                "shape",
                "fontname",
            ],
        )(
            filepath,
            split_files,
            ignore_folder,
            rankdir,
            overlap,
            ratio,
            fontsize,
            dpi,
            shape,
            fontname,
        )
        assert main.main() == 0
        assert get_import_dependency_list_mock.call_count == 1
        assert collect_files_in_module_mock.call_count == 1
        assert render_mock.call_count == 1
