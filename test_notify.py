import unittest
from unittest.mock import patch, MagicMock
import notify
import config
import datetime


class TestNotifyDontDisturb(unittest.TestCase):
    def setUp(self):
        self.test_tag = "test_token"
        config.tokens[self.test_tag] = "test_bark_token"
        config.dont_disturb_hours[self.test_tag] = [
            {"begin": 13, "end": 14}
        ]

    def tearDown(self):
        if self.test_tag in config.tokens:
            del config.tokens[self.test_tag]
        if self.test_tag in config.dont_disturb_hours:
            del config.dont_disturb_hours[self.test_tag]

    @patch('notify.requests.post')
    @patch('notify.push_ntfy')
    @patch('notify.datetime')
    def test_notify_outside_dont_disturb_hours(self, mock_datetime, mock_push_ntfy, mock_post):
        mock_now = MagicMock()
        mock_now.hour = 12
        mock_datetime.datetime.now.return_value = mock_now

        notify.notify("test_title", "test_body", self.test_tag)

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        self.assertEqual(payload['level'], 'timeSensitive')

    @patch('notify.requests.post')
    @patch('notify.push_ntfy')
    @patch('notify.datetime')
    def test_notify_inside_dont_disturb_hours(self, mock_datetime, mock_push_ntfy, mock_post):
        mock_now = MagicMock()
        mock_now.hour = 13
        mock_datetime.datetime.now.return_value = mock_now

        notify.notify("test_title", "test_body", self.test_tag)

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        self.assertEqual(payload['level'], 'passive')

    @patch('notify.requests.post')
    @patch('notify.push_ntfy')
    @patch('notify.datetime')
    def test_notify_at_boundary_start(self, mock_datetime, mock_push_ntfy, mock_post):
        mock_now = MagicMock()
        mock_now.hour = 13
        mock_datetime.datetime.now.return_value = mock_now

        notify.notify("test_title", "test_body", self.test_tag)

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        self.assertEqual(payload['level'], 'passive')

    @patch('notify.requests.post')
    @patch('notify.push_ntfy')
    @patch('notify.datetime')
    def test_notify_at_boundary_end(self, mock_datetime, mock_push_ntfy, mock_post):
        mock_now = MagicMock()
        mock_now.hour = 14
        mock_datetime.datetime.now.return_value = mock_now

        notify.notify("test_title", "test_body", self.test_tag)

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        self.assertEqual(payload['level'], 'timeSensitive')

    @patch('notify.requests.post')
    @patch('notify.push_ntfy')
    def test_notify_with_no_dont_disturb_config(self, mock_push_ntfy, mock_post):
        tag = "no_config_token"
        config.tokens[tag] = "test_bark_token"

        notify.notify("test_title", "test_body", tag)

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        self.assertEqual(payload['level'], 'timeSensitive')
        
        del config.tokens[tag]

    @patch('notify.requests.post')
    @patch('notify.push_ntfy')
    @patch('notify.datetime')
    def test_notify_with_multiple_time_periods(self, mock_datetime, mock_push_ntfy, mock_post):
        tag = "multi_period_token"
        config.tokens[tag] = "test_bark_token"
        config.dont_disturb_hours[tag] = [
            {"begin": 1, "end": 3},
            {"begin": 13, "end": 14},
            {"begin": 20, "end": 23},
        ]

        mock_now = MagicMock()
        mock_now.hour = 2
        mock_datetime.datetime.now.return_value = mock_now

        notify.notify("test_title", "test_body", tag)

        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        self.assertEqual(payload['level'], 'passive')
        
        del config.tokens[tag]
        del config.dont_disturb_hours[tag]


if __name__ == '__main__':
    unittest.main()
