"""Emotion detection using Watson NLP library."""
import requests


def emotion_detector(text_to_analyze):
    """Detect emotions in the given text using Watson NLP.

    Args:
        text_to_analyze (str): The text to analyze for emotions.

    Returns:
        dict: A dictionary containing emotion scores and the dominant emotion,
              or a dict with None values if input is blank or an error occurs.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
        }

    url = (
        'https://sn-watson-emotion.labs.skills.network/v1/'
        'watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    headers = {
        'Content-Type': 'application/json',
        'grpc-metadata-mm-model-id': 'emotion_aggregated-workflow_lang_en_stock',
    }
    input_json = {'raw_document': {'text': text_to_analyze}}

    try:
        response = requests.post(url, json=input_json, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
        }

    if not response.ok:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None,
        }

    result = response.json()
    emotion_predictions = result.get('emotionPredictions', [{}])
    emotions = emotion_predictions[0].get('emotion', {}) if emotion_predictions else {}

    anger = emotions.get('anger', 0)
    disgust = emotions.get('disgust', 0)
    fear = emotions.get('fear', 0)
    joy = emotions.get('joy', 0)
    sadness = emotions.get('sadness', 0)

    emotion_scores = {
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'joy': joy,
        'sadness': sadness,
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'joy': joy,
        'sadness': sadness,
        'dominant_emotion': dominant_emotion,
    }
