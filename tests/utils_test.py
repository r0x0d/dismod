import sys
from unittest import mock

import pytest

from dismod import utils


@pytest.mark.skipif(sys.platform == "win32", reason="Unix specific test")
@pytest.mark.parametrize(
    ("filepath", "filepath_walk", "expected"),
    (
        (
            "test",
            [("test", [], ["test.py", "test2.py", "test_not_py.txt"])],
            ["test/test.py", "test/test2.py"],
        ),
        ("test", [("test", [], ["test_not_py.txt"])], []),
        ("test", [], []),
    ),
)
def test_collect_files_in_module(filepath, filepath_walk, expected):
    with mock.patch.object(
        utils.os,
        "walk",
        return_value=filepath_walk,
    ) as os_walk_mock:
        assert utils.collect_files_in_module(filepath=filepath) == expected
        assert os_walk_mock.called
        assert os_walk_mock.call_count == 1


@pytest.mark.skipif(
    sys.platform != "win32",
    reason="Windows specific test",
)
@pytest.mark.parametrize(
    ("filepath", "filepath_walk", "expected"),
    (
        (
            "test",
            [("test", [], ["test.py", "test2.py", "test_not_py.txt"])],
            ["test\\test.py", "test\\test2.py"],
        ),
        ("test", [("test", [], ["test_not_py.txt"])], []),
        ("test", [], []),
    ),
)
def test_collect_files_in_module_win32(filepath, filepath_walk, expected):
    with mock.patch.object(
        utils.os,
        "walk",
        return_value=filepath_walk,
    ) as os_walk_mock:
        assert utils.collect_files_in_module(filepath=filepath) == expected
        assert os_walk_mock.called
        assert os_walk_mock.call_count == 1


@pytest.mark.parametrize(
    ("iterable", "expected"),
    (
        (
            ["first", "second", "third"],
            [
                (None, "first", "second"),
                ("first", "second", "third"),
                ("second", "third", None),
            ],
        ),
        (
            ["first", "second"],
            [(None, "first", "second"), ("first", "second", None)],
        ),
        (
            [],
            [],
        ),
    ),
)
def test_neighborhood(iterable, expected):
    assert list(utils.neighborhood(iterable=iterable)) == expected


@pytest.mark.parametrize(
    ("key", "value", "iterable", "expected"),
    (
        (
            "some_key",
            "some_value",
            [{"some_key": "some_value"}],
            (0, {"some_key": "some_value"}),
        ),
        (
            "some_key",
            "some_value",
            [],
            (None, None),
        ),
        (
            "some_key",
            "some_value",
            [{"some_key": "some_value"}, {"some_key": "some_value"}],
            (0, {"some_key": "some_value"}),
        ),
        (
            "some_key",
            "some_value",
            [{"some_key": "test"}],
            (None, None),
        ),
        (
            "some_key",
            "some_value",
            [{"some_key": "test"}, {"some_key": "some_value"}],
            (1, {"some_key": "some_value"}),
        ),
    ),
)
def test_search_key_in_iterable(key, value, iterable, expected):
    assert (
        utils.search_key_in_iterable(key=key, value=value, iterable=iterable)
        == expected
    )


@pytest.mark.parametrize(
    ("elements", "chunk_size", "expected"),
    (
        ([1, 2, 3, 4, 5, 6, 7, 8, 10], 2, [[1, 3, 5, 7, 10], [2, 4, 6, 8]]),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 10],
            4,
            [[1, 5, 10], [2, 6], [3, 7], [4, 8]],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 10],
            6,
            [[1, 7], [2, 8], [3, 10], [4], [5], [6]],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 10],
            8,
            [[1, 10], [2], [3], [4], [5], [6], [7], [8]],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 10],
            10,
            [[1], [2], [3], [4], [5], [6], [7], [8], [10], []],
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 10],
            5,
            [[1, 6], [2, 7], [3, 8], [4, 10], [5]],
        ),
    ),
)
def test_split_list_in_chunks(elements, chunk_size, expected):
    assert (
        list(
            utils.split_list_in_chunks(
                elements=elements,
                chunk_size=chunk_size,
            ),
        )
        == expected
    )
