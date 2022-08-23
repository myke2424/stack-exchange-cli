from unittest.mock import call, patch

import pytest

from .fixtures import mock_redis_db, redis_cache


def test_redis_set(mock_redis_db, redis_cache):
    """Test setting a key and value in a redis cache"""
    key, value = "APPLES", "BANANAS"
    redis_cache.set(key, value)

    mock_redis_db.assert_has_calls([call().set(key, value)])


@patch("stack_exchange.cache.json", autospec=True)
def test_redis_set_serialize_dict_to_json(mock_json, redis_cache, mock_redis_db):
    """Test setting a dictionary in a redis cache will serialize the dictionary to JSON for storage"""

    key = "https://api.stackexchange.com/2.3/search/advanced?q=DFS+vs+BFS&site=stackoverflow"

    value = {"question_id": 123, "question_title": "DFS VS BFS", "accepted_answer_id": 50}

    redis_cache.set(key, value)
    mock_json.dumps.assert_called_with(value)

    # Assert we invoked redis.set with the request URI and serialized JSON value
    mock_redis_db.assert_has_calls([call().set(key, mock_json.dumps.return_value)])


@patch("stack_exchange.cache.json", autospec=True)
def test_redis_get_dict_value_deserialization(mock_json, redis_cache, mock_redis_db):
    """Tests getting a value that's JSON encoded will be deserialized and returned as a dict"""
    key = "https://api.stackexchange.com/2.3/search/advanced?q=DFS+vs+BFS&site=stackoverflow"
    value = {"question_id": 123, "question_title": "DFS VS BFS", "accepted_answer_id": 50}

    redis_cache.set(key, value)

    value_dict = redis_cache.get(key)  # value gets deserialized here to dict
    mock_json.loads.assert_called()
    assert value_dict == mock_json.loads.return_value


def test_redis_get_value(redis_cache, mock_redis_db):
    """Tests getting a value from a redis cache"""
    key, value = "APPLES", "BANANAS"
    redis_cache.set(key, value)
    redis_cache.get(key)

    mock_redis_db.assert_has_calls([call().get(key)])
