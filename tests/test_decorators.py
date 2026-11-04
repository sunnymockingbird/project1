import os

import pytest

from src.decorators import log


@log()
def multiple(x: int, y: int) -> int:
    return x * y


@log()
def sample_div(x: int, y: int) -> float:
    return x / y


@pytest.mark.parametrize(
    "func, args, expected_name",
    [
        (multiple, (2, 5), "multiple"),
        (sample_div, (10, 5), "sample_div"),
    ],
)
def test_console_out1(capsys, func, args, expected_name) -> str:
    func(*args)
    captured = capsys.readouterr()
    expected_message = f"{expected_name} была вызвана и успешно завершила работу"
    assert expected_message in captured.out


@pytest.mark.parametrize(
    "func, args, expected_error, expected_message",
    [
        (multiple, ("2", "5"), TypeError, "multiple error: TypeError. Inputs: ('2', '5'), {}"),
        (sample_div, (10, 0), ZeroDivisionError, "sample_div error: ZeroDivisionError. Inputs: (10, 0), {}"),
    ],
)
def test_console_out2(capsys, func, args, expected_error, expected_message) -> str:
    with pytest.raises(expected_error):
        func(*args)
    captured = capsys.readouterr()
    assert expected_message in captured.out


@log("mylog.txt")
def multiply(x: int, y: int) -> int:
    return x * y


def test_file_multiple_success() -> None:
    result = multiply(3, 5)
    assert result == 15

    with open("mylog.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "multiply была вызвана и успешно завершила работу" in content
    os.remove("mylog.txt")


def test_file_multiple_error() -> None:
    with pytest.raises(TypeError):
        multiply("3", "5")

    with open("mylog.txt", "r", encoding="utf-8") as f:
        content = f.read()

    assert "multiply error: TypeError. Inputs: ('3', '5'), {}" in content
    os.remove("mylog.txt")
