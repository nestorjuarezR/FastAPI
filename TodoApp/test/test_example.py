import pytest

def test_equial_or_not_equal():
    assert 3 == 3
    assert 3 != 1



def test_is_instance():
    assert isinstance("tHis is a string", str)
    assert not isinstance('10', int)



def test_boolean():
    validate = True
    assert validate is True
    assert ('Hello' == 'word') is False


class Student:
    def __init__(self, first_name : str, last_name : str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years




