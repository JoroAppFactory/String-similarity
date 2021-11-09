# Global
import glob
import os
import ntpath
import sys
import requests

# Resources
from resources.services.detection_service import export_detections
from resources.services.cropping_service import start_crop
from resources.services.amazon_service import upload_file
from resources.services.file_service import read_file
from resources.services.download_service import download_image


def download_whiskies_images():
    base_image_url = "https://whiskys.s3.eu-west-2.amazonaws.com/big/"
    file = read_file('specific-whiskys.json')

    for obj in file:
        download_image(
            f"{base_image_url}{obj['image']}", obj['whisky_id'])


def run():
    # Plan:
    # 0. Get the given whiskys by ID and download locally their images
    # 1. Run the autocrop
    # 2. Upload images to Amazon S3 ( Storage )
    # 3. Export to detections.json or database

    # 0.
    try:
        download_whiskies_images()
    except:
        print('Downloading the images for given whiskys failed..')

    # 1.
    try:
        start_crop()
    except:
        print(f'Cropping failed - {sys.exc_info()[0]}')

    # 2.
    try:
        print('Start uploading to AWS S3..')
        path = glob.glob(f"{os.path.join(os.getcwd(), 'cropped_images')}/*")
        for imagePath in path:
            imgName = ntpath.basename(imagePath)
            upload_file(imgName)
        print('Uploading to AWS S3 finished!')

    except:
        print(f'Uploading to AWS S3 failed - {sys.exc_info()[0]}')

    # 3.
    try:
        export_detections()
    except:
        print(f'Failed to export detections - {sys.exc_info()[0]}')


run()
