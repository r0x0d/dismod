import dis

import pytest


@pytest.fixture
def generate_instruction_set():
    def _call_dis(code: str):
        return list(dis.get_instructions(code))

    return _call_dis
