import pytest


class NotInRnage(Exception):
    def __init__(self, message='value not in range'):
        self.message=message
        super().__init__(self.message)


def test_generic():
    a=5
    with pytest.raises(NotInRnage):
        if a not in range(10, 20):
            raise NotInRnage