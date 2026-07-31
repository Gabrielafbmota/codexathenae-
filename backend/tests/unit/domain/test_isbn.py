"""Unit tests for ISBN value object."""

import pytest

from codexathenae.domain.exceptions.book_exceptions import InvalidISBNError
from codexathenae.domain.value_objects.isbn import ISBN


class TestISBN10:
    def test_valid_isbn10(self) -> None:
        isbn = ISBN("0306406152")
        assert isbn.value == "0306406152"
        assert isbn.is_isbn10
        assert not isbn.is_isbn13

    def test_valid_isbn10_with_x_checksum(self) -> None:
        # 155860510X: 1*10+5*9+5*8+8*7+6*6+0*5+5*4+1*3+0*2+10*1 = 220, 220%11=0
        isbn = ISBN("155860510X")
        assert isbn.value == "155860510X"

    def test_isbn10_strips_hyphens(self) -> None:
        isbn = ISBN("0-306-40615-2")
        assert isbn.value == "0306406152"

    def test_isbn10_strips_spaces(self) -> None:
        isbn = ISBN("0 306 40615 2")
        assert isbn.value == "0306406152"

    def test_invalid_isbn10_checksum(self) -> None:
        with pytest.raises(InvalidISBNError):
            ISBN("0306406153")

    def test_invalid_isbn10_non_digit(self) -> None:
        with pytest.raises(InvalidISBNError):
            ISBN("030640615A")


class TestISBN13:
    def test_valid_isbn13(self) -> None:
        isbn = ISBN("9780306406157")
        assert isbn.value == "9780306406157"
        assert isbn.is_isbn13
        assert not isbn.is_isbn10

    def test_isbn13_strips_hyphens(self) -> None:
        isbn = ISBN("978-0-306-40615-7")
        assert isbn.value == "9780306406157"

    def test_invalid_isbn13_checksum(self) -> None:
        with pytest.raises(InvalidISBNError):
            ISBN("9780306406158")

    def test_invalid_isbn13_too_short(self) -> None:
        with pytest.raises(InvalidISBNError):
            ISBN("978030640615")


class TestISBNGeneral:
    def test_empty_string_is_invalid(self) -> None:
        with pytest.raises(InvalidISBNError):
            ISBN("")

    def test_random_string_is_invalid(self) -> None:
        with pytest.raises(InvalidISBNError):
            ISBN("not-an-isbn")

    def test_equality(self) -> None:
        assert ISBN("9780306406157") == ISBN("978-0-306-40615-7")

    def test_hash(self) -> None:
        s = {ISBN("9780306406157"), ISBN("978-0-306-40615-7")}
        assert len(s) == 1

    def test_str(self) -> None:
        assert str(ISBN("9780306406157")) == "9780306406157"

    def test_repr(self) -> None:
        assert "9780306406157" in repr(ISBN("9780306406157"))
