# General
from flask_restx import Resource
import os
from flask import request

# Services
from resources.services.amazon_service import detect_text as amazon_detect_text
from resources.services.google_service import detect_text as google_detect_text
from resources.services.file_service import read_file
from resources.services.detection_service import get_closest_cosine


class ClosestMatch(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        text = data.get('text', '')
        whisky_ids = data.get('whisky_ids', '')

        detections = read_file('detections.json')

        closest_google = get_closest_cosine(
            text, detections, 0.0, 'google-1')

        best_whisky_ids = []
        for whisky_id in whisky_ids:
            found_obj = next(
                (x for x in closest_google if x['whisky_id'] == whisky_id), None)

            obj = {
                "whisky_id": whisky_id,
                "confidence": 0.0
            }

            if found_obj and found_obj['confidence'] >= 0.50:
                obj['confidence'] = found_obj['confidence']

            best_whisky_ids.append(obj)

        best_whisky_ids.sort(key=lambda x: x['confidence'], reverse=True)
        result = {
            "given_whisky_ids": whisky_ids,
            "best_whisky_ids": best_whisky_ids
        }

        return {'status': 'ok', 'result': result}, 200


class ClosestMatchFromFile(Resource):
    @classmethod
    def post(cls):
        cutoff = 0.7
        file = request.files['file']
        cutoff_input = request.form.get('cutoff')

        if not file:
            return {'status': 'failed', 'message': 'The image is missing.'}, 400

        if cutoff_input is not None:
            cutoff = float(cutoff_input)

        file.filename = "imageToScan.jpeg"
        file.save(f"{os.getcwd()}/cropped_images/{file.filename}")

        amazon_ocr = amazon_detect_text(file.filename, True)
        google1_ocr = google_detect_text(
            f"{os.getcwd()}/cropped_images/{file.filename}", file.filename)
        google2_ocr = ""

        detections = read_file('detections.json')

        amazon_closest = get_closest_cosine(
            amazon_ocr, detections, 0.50, 'amazon')

        google1_closest = get_closest_cosine(
            google1_ocr, detections, 0.50, 'google-1')

        google2_closest = []

        obj = {
            "current_photo_amazon": amazon_ocr,
            "current_photo_google_1": google1_ocr,
            "current_photo_google_2": google2_ocr,
            "results": {
                "amazon": amazon_closest,
                "google_1": google1_closest,
                "google_2": google2_closest,
            }
        }

        return {'status': 'ok', 'result': obj}, 200
