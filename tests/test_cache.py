import pytest


def test_cache_hit(cache):
    cache.set("APPLES", "BANANAS")
    assert cache.get("APPLES") == "BANANAS"


def test_cache_miss(cache):
    assert cache.get("ORANGES") is None


def test_overwrite_cache(cache):
    cache.set("BLUE", "BERRIES")
    cache.set("BLUE", "SKY")
    assert cache.get("BLUE") == "SKY"
