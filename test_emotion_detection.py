"""Unit tests for the emotion_detector function."""
import unittest
from unittest.mock import patch, MagicMock
from EmotionDetection.emotion_detection import emotion_detector


def _mock_response(emotions):
    """Create a mock requests.Response with the given emotion scores."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.ok = True
    mock_resp.json.return_value = {
        'emotionPredictions': [{'emotion': emotions}]
    }
    return mock_resp


class TestEmotionDetector(unittest.TestCase):
    """Tests for the emotion_detector function."""

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_joy_emotion(self, mock_post):
        """Test that joy is detected as the dominant emotion for positive text."""
        mock_post.return_value = _mock_response(
            {'anger': 0.05, 'disgust': 0.03, 'fear': 0.04, 'joy': 0.85, 'sadness': 0.03}
        )
        result = emotion_detector('I am glad this happened')
        self.assertEqual(result['dominant_emotion'], 'joy')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_anger_emotion(self, mock_post):
        """Test that anger is detected as the dominant emotion for angry text."""
        mock_post.return_value = _mock_response(
            {'anger': 0.80, 'disgust': 0.05, 'fear': 0.06, 'joy': 0.04, 'sadness': 0.05}
        )
        result = emotion_detector('I am really mad about this')
        self.assertEqual(result['dominant_emotion'], 'anger')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_disgust_emotion(self, mock_post):
        """Test that disgust is detected as the dominant emotion for disgusting text."""
        mock_post.return_value = _mock_response(
            {'anger': 0.05, 'disgust': 0.78, 'fear': 0.06, 'joy': 0.04, 'sadness': 0.07}
        )
        result = emotion_detector('I feel disgusted just hearing about this')
        self.assertEqual(result['dominant_emotion'], 'disgust')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_sadness_emotion(self, mock_post):
        """Test that sadness is detected as the dominant emotion for sad text."""
        mock_post.return_value = _mock_response(
            {'anger': 0.04, 'disgust': 0.03, 'fear': 0.05, 'joy': 0.06, 'sadness': 0.82}
        )
        result = emotion_detector('It is really sad about this')
        self.assertEqual(result['dominant_emotion'], 'sadness')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_fear_emotion(self, mock_post):
        """Test that fear is detected as the dominant emotion for fearful text."""
        mock_post.return_value = _mock_response(
            {'anger': 0.05, 'disgust': 0.04, 'fear': 0.79, 'joy': 0.05, 'sadness': 0.07}
        )
        result = emotion_detector('I am scared to death by this')
        self.assertEqual(result['dominant_emotion'], 'fear')

    def test_blank_input_returns_none(self):
        """Test that blank input returns None for all fields."""
        result = emotion_detector('')
        self.assertIsNone(result['dominant_emotion'])
        self.assertIsNone(result['anger'])
        self.assertIsNone(result['disgust'])
        self.assertIsNone(result['fear'])
        self.assertIsNone(result['joy'])
        self.assertIsNone(result['sadness'])

    def test_whitespace_input_returns_none(self):
        """Test that whitespace-only input returns None for all fields."""
        result = emotion_detector('   ')
        self.assertIsNone(result['dominant_emotion'])

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_result_has_all_keys(self, mock_post):
        """Test that result contains all expected emotion keys."""
        mock_post.return_value = _mock_response(
            {'anger': 0.05, 'disgust': 0.03, 'fear': 0.04, 'joy': 0.85, 'sadness': 0.03}
        )
        result = emotion_detector('I am happy today')
        self.assertIn('anger', result)
        self.assertIn('disgust', result)
        self.assertIn('fear', result)
        self.assertIn('joy', result)
        self.assertIn('sadness', result)
        self.assertIn('dominant_emotion', result)

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_400_response_returns_none(self, mock_post):
        """Test that a non-OK API response returns None for all fields."""
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.ok = False
        mock_post.return_value = mock_resp
        result = emotion_detector('some text')
        self.assertIsNone(result['dominant_emotion'])
        self.assertIsNone(result['anger'])

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_network_error_returns_none(self, mock_post):
        """Test that a network error returns None for all fields."""
        import requests as req
        mock_post.side_effect = req.exceptions.ConnectionError('Network error')
        result = emotion_detector('some text')
        self.assertIsNone(result['dominant_emotion'])
        self.assertIsNone(result['anger'])


if __name__ == '__main__':
    unittest.main()
