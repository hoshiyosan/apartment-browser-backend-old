from apartment.parser import parse
from tests.data.aparts import aparts

def test_non_regression():
    for apart in aparts:
        data = parse(apart.article)
        assert apart.data == data
