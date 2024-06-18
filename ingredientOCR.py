from google.cloud import vision
import os
import re

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/cc-c241-ps246-60ba32f0ad56.json"

# Initialize a vision client
vision_client = vision.ImageAnnotatorClient()

def extract_ingredients(gcs_uri):
    """Extract ingredients from an image at the specified Google Cloud Storage URI."""
    matches = re.match(r'gs://([^/]+)/(.+)', gcs_uri)
    if not matches:
        return "Invalid GCS URI", False
    bucket_name = matches.group(1)
    file_name = matches.group(2)

    try:
        result = vision_client.text_detection(image={'source': {'image_uri': gcs_uri}})
        detections = result.text_annotations

        if detections:
            full_text = detections[0].description
            cleaned_text = re.sub(r'.*ingredients:', '', full_text, flags=re.I).replace('\n', ' ')
            return [ingredient.strip().lower() for ingredient in cleaned_text.split(',')], True
    except Exception as error:
        return f'Failed to detect text: {error}', False
