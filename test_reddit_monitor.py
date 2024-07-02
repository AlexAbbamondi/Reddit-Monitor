import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the function to be tested
from reddit_monitor import monitor_new_posts

class TestRedditMonitor(unittest.TestCase):
    @patch('reddit_monitor.reddit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_monitor_new_posts(self, mock_stdout, mock_reddit):
        # Create a mock submission
        mock_submission = MagicMock()
        mock_submission.title = "Test post about mesothelioma"
        mock_submission.url = "http://example.com/test_post"
        
        # Set up the mock to return the mock submission
        mock_reddit.subreddit.return_value.stream.submissions.return_value = [mock_submission]
        
        # Call the function
        monitor_new_posts(['all'], 'mesothelioma')

        # Check if the expected outputs were printed
        output = mock_stdout.getvalue()
        self.assertIn("New post found: Test post about mesothelioma", output)
        self.assertIn("URL: http://example.com/test_post", output)

if __name__ == '__main__':
    unittest.main()