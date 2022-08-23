import pytest

from stack_exchange import utils
from unittest.mock import patch, mock_open
import pathlib


@patch.object(pathlib.Path, 'is_file')
@patch.object(pathlib.Path, 'open', new_callable=mock_open, read_data="data")
@patch('stack_exchange.utils.yaml', autospec=True)
def test_load_yaml_file_when_file_exists(mock_yaml, mock_path_open, mock_is_file):
    file_path = "/mnt/c/users/test_user/test.yaml"
    mock_is_file.return_value = True

    yaml = utils.load_yaml_file(file_path)
    mock_yaml.load.assert_called_with(mock_path_open.return_value, Loader=mock_yaml.FullLoader)
    assert yaml == mock_yaml.load.return_value


@patch.object(pathlib.Path, 'is_file')
def test_load_yaml_file_raises_file_not_found(mock_is_file):
    file_path = "/mnt/c/users/test_user/test.yaml"
    mock_is_file.return_value = False

    with pytest.raises(FileNotFoundError):
        utils.load_yaml_file(file_path)


def test_html_to_markdown():
    html = '<h1>Question | 2010-07-26 | 443 votes</h1>'
    expected = '''Question | 2010-07-26 | 443 votes
=================================

'''
    markdown = utils.html_to_markdown(html)

    assert markdown.markup == expected


def test_epoch_time_to_datetime():
    epoch_timestamp = 1235349008
    expected = "2009-02-22"
    assert utils.epoch_time_to_datetime_str(epoch_timestamp) == expected