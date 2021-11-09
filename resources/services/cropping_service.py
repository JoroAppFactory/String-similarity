# Global
import cv2
import os
import ntpath
import glob
from pathlib import Path


def initialize_class_names(source_file):
    with open(source_file, 'rt') as f:
        return f.read().rstrip('\n').split('\n')


def initialize_detection_model(base_path):
    configPath = f'{base_path}/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = f'{base_path}/frozen_inference_graph.pb'
    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    return net


def get_image_name(imagePath):
    imgName = ntpath.basename(imagePath)
    imgName = imgName.replace(".jpg", "")
    imgName = imgName.replace(".jpeg", "")
    imgName = imgName.replace(".png", "")
    imgName = imgName.replace(".gif", "")
    imgName = imgName.replace(" ", "")
    return imgName


def write_to_file(directory, name, file):
    cv2.imwrite(f"{directory}/{name}.jpeg", file)


def start_crop():
    print('Start cropping...')
    base_path = os.getcwd()

    classNames = initialize_class_names(f'{base_path}/coco.names')
    net = initialize_detection_model(base_path)

    images_path = glob.glob(f"{os.path.join(base_path, 'raw_images')}/*")

    index = 0
    for imagePath in images_path:
        try:
            img = cv2.imread(imagePath)
            imgName = get_image_name(imagePath)

            classIds, confs, bbox = net.detect(img, confThreshold=0.5)

            # Write every whisky in separate folder
            # directory = os.path.join(os.getcwd(), 'cropped', imgName)

            # Write all in one folder
            directory = os.path.join(base_path, 'cropped_images')

            Path(directory).mkdir(parents=True, exist_ok=True)

            if(len(classIds) > 0 and len(confs) > 0):
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    if(classNames[classId-1].upper() == 'BOTTLE' and box[3] >= 700):
                        # box  ->  [X,Y,W,H]
                        cropped_image = img[box[1]:box[1] +
                                            box[3], box[0]:box[0]+box[2]]

                    write_to_file(
                        directory, f"{imgName}-{index}", cropped_image)
                    print(f'Image - {index} cropped succesfully')
                    index += 1

        except Exception as e:
            print(str(e))

    print('Cropping ended succesfully')
