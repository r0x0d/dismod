from dis import Instruction
from unittest import mock

import pytest

from dismod import instruction


@pytest.mark.parametrize(
    ("current", "following", "expected"),
    ((108, 109, True), (108, 84, True), (108, 110, False)),
)
def test_check_from_statement(current, following, expected):
    assert (
        instruction._check_from_statement(current=current, following=following)
        == expected
    )


@pytest.mark.parametrize(
    ("previous", "current", "following", "expected"),
    (
        (None, 109, 109, True),
        (108, 109, None, True),
        (108, 84, None, True),
        (None, 109, None, True),
        (None, None, None, False),
    ),
)
def test_check_import_from_statement(previous, current, following, expected):
    assert (
        instruction._check_import_from_statement(
            previous=previous,
            current=current,
            following=following,
        )
        == expected
    )


@pytest.mark.parametrize(
    ("current", "following", "expected"),
    ((108, 108, True), (108, None, True), (108, 110, False)),
)
def test_check_single_import_statement(current, following, expected):
    assert (
        instruction._check_single_import_statement(
            current=current,
            following=following,
        )
        == expected
    )


@pytest.mark.parametrize(
    ("code", "expected"),
    (
        (
            """
import babel
            """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="babel",
                    argrepr="babel",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            """
from bz2 import BZ2Compressor
            """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="bz2",
                    argrepr="bz2",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=1,
                    argval="BZ2Compressor",
                    argrepr="BZ2Compressor",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            """
from json import *
           """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="json",
                    argrepr="json",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_STAR",
                    opcode=84,
                    arg=None,
                    argval=None,
                    argrepr="",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            """
hello = "world"
            """,
            [],
        ),
    ),
)
def test_extract_import_instructions(code, expected, generate_instruction_set):
    instructions = generate_instruction_set(code)
    assert (
        instruction._extract_import_instructions(instructions=instructions)
        == expected
    )


@pytest.mark.parametrize(
    ("code", "expected"),
    (
        (
            """
def t():
    from something import another_thing
            """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="something",
                    argrepr="something",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=1,
                    argval="another_thing",
                    argrepr="another_thing",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            """
hello = "world"
            """,
            [],
        ),
    ),
)
def test_convert_codeblocks_instructions(
    code,
    expected,
    generate_instruction_set,
):
    instructions = generate_instruction_set(code)

    assert (
        instruction._convert_codeblocks_instructions(instructions=instructions)
        == expected
    )


@pytest.mark.parametrize(
    ("filepath", "contents", "expected"),
    (
        (
            "test.py",
            """
from json import *
        """,
            [
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=0,
                    argval=0,
                    argrepr="0",
                    offset=0,
                    starts_line=2,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=1,
                    argval=("*",),
                    argrepr="('*',)",
                    offset=2,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="json",
                    argrepr="json",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_STAR",
                    opcode=84,
                    arg=None,
                    argval=None,
                    argrepr="",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=2,
                    argval=None,
                    argrepr="None",
                    offset=8,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="RETURN_VALUE",
                    opcode=83,
                    arg=None,
                    argval=None,
                    argrepr="",
                    offset=10,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            "test.py",
            """
variable = 'hi'
        """,
            [
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=0,
                    argval="hi",
                    argrepr="'hi'",
                    offset=0,
                    starts_line=2,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="STORE_NAME",
                    opcode=90,
                    arg=0,
                    argval="variable",
                    argrepr="variable",
                    offset=2,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=1,
                    argval=None,
                    argrepr="None",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="RETURN_VALUE",
                    opcode=83,
                    arg=None,
                    argval=None,
                    argrepr="",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            "test.py",
            """
import os
        """,
            [
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=0,
                    argval=0,
                    argrepr="0",
                    offset=0,
                    starts_line=2,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=1,
                    argval=None,
                    argrepr="None",
                    offset=2,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os",
                    argrepr="os",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="STORE_NAME",
                    opcode=90,
                    arg=0,
                    argval="os",
                    argrepr="os",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=1,
                    argval=None,
                    argrepr="None",
                    offset=8,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="RETURN_VALUE",
                    opcode=83,
                    arg=None,
                    argval=None,
                    argrepr="",
                    offset=10,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            "test.py",
            """""",
            [
                Instruction(
                    opname="LOAD_CONST",
                    opcode=100,
                    arg=0,
                    argval=None,
                    argrepr="None",
                    offset=0,
                    starts_line=1,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="RETURN_VALUE",
                    opcode=83,
                    arg=None,
                    argval=None,
                    argrepr="",
                    offset=2,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
    ),
)
def test_get_instructions_from_file(filepath, contents, expected):
    with mock.patch.object(instruction, "open") as open_file_read_mock:
        open_file_read_mock.return_value.__enter__.return_value.read = (
            lambda: contents
        )
        assert instruction.get_instructions_from_file(filepath) == expected


@pytest.mark.parametrize(
    ("code", "expected"),
    (
        (
            """
import os
hello = "world"
            """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os",
                    argrepr="os",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            """
from os import path
            """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os",
                    argrepr="os",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=1,
                    argval="path",
                    argrepr="path",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            """
def func_import():
    from os import path
            """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os",
                    argrepr="os",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=1,
                    argval="path",
                    argrepr="path",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            """
import json
def func_import():
    from os import path
            """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os",
                    argrepr="os",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=1,
                    argval="path",
                    argrepr="path",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="json",
                    argrepr="json",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
        (
            """
from os.path import abspath
from os.path import altsep
from os.path import basename
from os.path import join
            """,
            [
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os.path",
                    argrepr="os.path",
                    offset=4,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=1,
                    argval="abspath",
                    argrepr="abspath",
                    offset=6,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os.path",
                    argrepr="os.path",
                    offset=16,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=2,
                    argval="altsep",
                    argrepr="altsep",
                    offset=18,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os.path",
                    argrepr="os.path",
                    offset=28,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=3,
                    argval="basename",
                    argrepr="basename",
                    offset=30,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_NAME",
                    opcode=108,
                    arg=0,
                    argval="os.path",
                    argrepr="os.path",
                    offset=40,
                    starts_line=None,
                    is_jump_target=False,
                ),
                Instruction(
                    opname="IMPORT_FROM",
                    opcode=109,
                    arg=4,
                    argval="join",
                    argrepr="join",
                    offset=42,
                    starts_line=None,
                    is_jump_target=False,
                ),
            ],
        ),
    ),
)
def test_get_import_instructions(code, expected, generate_instruction_set):
    instructions = generate_instruction_set(code)
    assert (
        instruction.get_import_instructions(instructions=instructions)
        == expected
    )


@pytest.mark.parametrize(
    ("code", "expected"),
    (
        (
            """
from . import test_case
            """,
            [{"from_statement": ".", "import_statements": ["test_case"]}],
        ),
        (
            """
import configparser
import os
from json import *
from os.path import abspath
from os.path import altsep
from os.path import basename
from os.path import join

try:
    import something
    from bz2 import BZ2Compressor
except Exception:
    pass


def test():
    import babel
    from _yaml import warnings
            """,
            [
                {"from_statement": None, "import_statements": ["babel"]},
                {"from_statement": "_yaml", "import_statements": ["warnings"]},
                {
                    "from_statement": None,
                    "import_statements": ["configparser"],
                },
                {"from_statement": None, "import_statements": ["os"]},
                {"from_statement": "json", "import_statements": ["*"]},
                {
                    "from_statement": "os.path",
                    "import_statements": [
                        "abspath",
                        "altsep",
                        "basename",
                        "join",
                    ],
                },
                {"from_statement": None, "import_statements": ["something"]},
                {
                    "from_statement": "bz2",
                    "import_statements": ["BZ2Compressor"],
                },
            ],
        ),
        (
            """
import configparser
import os
from json import *
from os.path import abspath, altsep, basename, join
            """,
            [
                {
                    "from_statement": None,
                    "import_statements": ["configparser"],
                },
                {"from_statement": None, "import_statements": ["os"]},
                {"from_statement": "json", "import_statements": ["*"]},
                {
                    "from_statement": "os.path",
                    "import_statements": [
                        "abspath",
                        "altsep",
                        "basename",
                        "join",
                    ],
                },
            ],
        ),
        (
            """
import os
            """,
            [{"from_statement": None, "import_statements": ["os"]}],
        ),
    ),
)
def test_parse_instructions(code, expected, generate_instruction_set):
    instructions = generate_instruction_set(code)
    instructions = instruction.get_import_instructions(
        instructions=instructions,
    )
    assert (
        instruction.parse_instructions(instructions=instructions) == expected
    )
