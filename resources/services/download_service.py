import requests
import os

def download_image(url, filename):
    with open(f'{os.getcwd()}/raw_images/{filename}.jpeg', 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
        
        print(f'Image {filename} downloaded sucessfully')
