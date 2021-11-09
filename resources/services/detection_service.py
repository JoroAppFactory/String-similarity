# General
import json
import os
import difflib

# Services
from resources.services.amazon_service import get_bucket_files
from resources.services.amazon_service import detect_text as amazon_detect_text
from resources.services.google_service import detect_text as google_detect_text
from resources.services.file_service import write_to_file
from resources.services.cosine_similarity_service import distance as cs_distance


def get_whisky_from_filename(filename):
    whisky_id = str(filename).replace('.png', '')
    dash_index = whisky_id.find('-')

    whisky_id = whisky_id[0: dash_index]
    return int(whisky_id)


def get_closest_cosine(text, detections, minConfidence, type):
    search_field = []
    for detection in detections:
        search_field.append(detection[type])

    closest_matches = []
    for x in search_field:
        confidence = cs_distance(str(text), str(x))

        if confidence < minConfidence:
            continue

        closest_matches.append({"compared_text": x, "confidence": confidence})

    # reverse was True
    closest_matches.sort(key=lambda x: x['confidence'], reverse=True)

    result = []
    seen_whiskys = set()
    for match in closest_matches:
        founded = next(
            (x for x in detections if x[type] == match['compared_text']), None)

        if founded is not None:
            whisky_id = get_whisky_from_filename(founded['filename'])

            if whisky_id not in seen_whiskys:
                seen_whiskys.add(whisky_id)
                result.append(
                    {"whisky_id": whisky_id, "confidence": match['confidence']})

    return result


def get_closest(text, detections, cutoff, type):
    search_field = []
    for detection in detections:
        search_field.append(detection[type])

    closest_matches = []
    for x in search_field:
        percentage = difflib.SequenceMatcher(
            None, str(text).lower(), str(x).lower()).ratio()

        if percentage <= cutoff:
            continue

        closest_matches.append({"compared_text": x, "percentage": percentage})

    # reverse was True
    closest_matches.sort(key=lambda x: x['percentage'], reverse=True)

    result = []
    seen_whiskys = set()
    for match in closest_matches:
        founded = next(
            (x for x in detections if x[type] == match['compared_text']), None)

        if founded is not None:
            whisky_id = get_whisky_from_filename(founded['filename'])

            if whisky_id not in seen_whiskys:
                seen_whiskys.add(whisky_id)
                result.append(
                    {"whisky_id": whisky_id, "percentage": match['percentage']})

    return result


def export_detections():
    print('Export detections to json started...')
    bucket_files = get_bucket_files()
    detections = []

    for file in bucket_files:
        amazon_detect_text_result = amazon_detect_text(file.key, False)

        google_detect_text_1_result = google_detect_text(
            f"{os.path.join(os.getcwd(), 'cropped_images')}/{file.key}", file.key)
        google_detect_text_2_result = "soon..."

        print(f'{file.key} exported succesfully!')
        detections.append(
            {
                "filename": file.key,
                "amazon": amazon_detect_text_result,
                "google-1": google_detect_text_1_result,
                "google-2": google_detect_text_2_result
            }
        )

    write_to_file(f"{os.getcwd()}/detections.json", json.dumps(
        detections, ensure_ascii=False))
    print('Export detections to json finished!')
