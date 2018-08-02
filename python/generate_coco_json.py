#!/usr/bin/env python3

__version__ = "0.1.0"
__license__ = "GPLv3"
__status__ = "Prototype"

import datetime
import json
import os
import re
import fnmatch
from skimage import morphology, filters
from PIL import Image
import numpy as np
from annotation_data import AnnotationData
from annotation_data import get_metadata
from pycococreatortools import pycococreatortools

DATA_DIR = '../data'
IMAGE_DIR = '../data/images'
ANNOTATION_DIR = '../data/annotations'

INFO = {
    "description": "China-Unicom-CCTV",
    "url": "https://github.com/waspinator/js-segment-annotator",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "ken han",
    "date_created": datetime.datetime.now().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

# CATEGORIES = [
#     {
#         'id': 1,
#         'name': 'skin',
#         'supercategory': 'human'
#     },
#     {
#         'id': 2,
#         'name': 'hair',
#         'supercategory': 'human'
#     },
#     {
#         'id': 3,
#         'name': 'dress',
#         'supercategory': 'clothes'
#     }
# ]
CATEGORIES = [
    {
        "id": 1,
        "name": "person",
        "supercategory": "person"
    },
    {
        "id": 2,
        "name": "bicycle",
        "supercategory": "vehicle"
    },
    {
        "id": 3,
        "name": "car",
        "supercategory": "vehicle"
    },
    {
        "id": 4,
        "name": "motorcycle",
        "supercategory": "vehicle"
    },
    {
        "id": 5,
        "name": "airplane",
        "supercategory": "vehicle"
    },
    {
        "id": 6,
        "name": "bus",
        "supercategory": "vehicle"
    },
    {
        "id": 7,
        "name": "train",
        "supercategory": "vehicle"
    },
    {
        "id": 8,
        "name": "truck",
        "supercategory": "vehicle"
    },
    {
        "id": 9,
        "name": "boat",
        "supercategory": "vehicle"
    },
    {
        "id": 10,
        "name": "traffic light",
        "supercategory": "outdoor"
    },
    {
        "id": 11,
        "name": "fire hydrant",
        "supercategory": "outdoor"
    },
    {
        "id": 13,
        "name": "stop sign",
        "supercategory": "outdoor"
    },
    {
        "id": 14,
        "name": "parking meter",
        "supercategory": "outdoor"
    },
    {
        "id": 15,
        "name": "bench",
        "supercategory": "outdoor"
    },
    {
        "id": 16,
        "name": "bird",
        "supercategory": "animal"
    },
    {
        "id": 17,
        "name": "cat",
        "supercategory": "animal"
    },
    {
        "id": 18,
        "name": "dog",
        "supercategory": "animal"
    },
    {
        "id": 19,
        "name": "horse",
        "supercategory": "animal"
    },
    {
        "id": 20,
        "name": "sheep",
        "supercategory": "animal"
    },
    {
        "id": 21,
        "name": "cow",
        "supercategory": "animal"
    },
    {
        "id": 22,
        "name": "elephant",
        "supercategory": "animal"
    },
    {
        "id": 23,
        "name": "bear",
        "supercategory": "animal"
    },
    {
        "id": 24,
        "name": "zebra",
        "supercategory": "animal"
    },
    {
        "id": 25,
        "name": "giraffe",
        "supercategory": "animal"
    },
    {
        "id": 27,
        "name": "backpack",
        "supercategory": "accessory"
    },
    {
        "id": 28,
        "name": "umbrella",
        "supercategory": "accessory"
    },
    {
        "id": 31,
        "name": "handbag",
        "supercategory": "accessory"
    },
    {
        "id": 32,
        "name": "tie",
        "supercategory": "accessory"
    },
    {
        "id": 33,
        "name": "suitcase",
        "supercategory": "accessory"
    },
    {
        "id": 34,
        "name": "frisbee",
        "supercategory": "sports"
    },
    {
        "id": 35,
        "name": "skis",
        "supercategory": "sports"
    },
    {
        "id": 36,
        "name": "snowboard",
        "supercategory": "sports"
    },
    {
        "id": 37,
        "name": "sports ball",
        "supercategory": "sports"
    },
    {
        "id": 38,
        "name": "kite",
        "supercategory": "sports"
    },
    {
        "id": 39,
        "name": "baseball bat",
        "supercategory": "sports"
    },
    {
        "id": 40,
        "name": "baseball glove",
        "supercategory": "sports"
    },
    {
        "id": 41,
        "name": "skateboard",
        "supercategory": "sports"
    },
    {
        "id": 42,
        "name": "surfboard",
        "supercategory": "sports"
    },
    {
        "id": 43,
        "name": "tennis racket",
        "supercategory": "sports"
    },
    {
        "id": 44,
        "name": "bottle",
        "supercategory": "kitchen"
    },
    {
        "id": 46,
        "name": "wine glass",
        "supercategory": "kitchen"
    },
    {
        "id": 47,
        "name": "cup",
        "supercategory": "kitchen"
    },
    {
        "id": 48,
        "name": "fork",
        "supercategory": "kitchen"
    },
    {
        "id": 49,
        "name": "knife",
        "supercategory": "kitchen"
    },
    {
        "id": 50,
        "name": "spoon",
        "supercategory": "kitchen"
    },
    {
        "id": 51,
        "name": "bowl",
        "supercategory": "kitchen"
    },
    {
        "id": 52,
        "name": "banana",
        "supercategory": "food"
    },
    {
        "id": 53,
        "name": "apple",
        "supercategory": "food"
    },
    {
        "id": 54,
        "name": "sandwich",
        "supercategory": "food"
    },
    {
        "id": 55,
        "name": "orange",
        "supercategory": "food"
    },
    {
        "id": 56,
        "name": "broccoli",
        "supercategory": "food"
    },
    {
        "id": 57,
        "name": "carrot",
        "supercategory": "food"
    },
    {
        "id": 58,
        "name": "hot dog",
        "supercategory": "food"
    },
    {
        "id": 59,
        "name": "pizza",
        "supercategory": "food"
    },
    {
        "id": 60,
        "name": "donut",
        "supercategory": "food"
    },
    {
        "id": 61,
        "name": "cake",
        "supercategory": "food"
    },
    {
        "id": 62,
        "name": "chair",
        "supercategory": "furniture"
    },
    {
        "id": 63,
        "name": "couch",
        "supercategory": "furniture"
    },
    {
        "id": 64,
        "name": "potted plant",
        "supercategory": "furniture"
    },
    {
        "id": 65,
        "name": "bed",
        "supercategory": "furniture"
    },
    {
        "id": 67,
        "name": "dining table",
        "supercategory": "furniture"
    },
    {
        "id": 70,
        "name": "toilet",
        "supercategory": "furniture"
    },
    {
        "id": 72,
        "name": "tv",
        "supercategory": "electronic"
    },
    {
        "id": 73,
        "name": "laptop",
        "supercategory": "electronic"
    },
    {
        "id": 74,
        "name": "mouse",
        "supercategory": "electronic"
    },
    {
        "id": 75,
        "name": "remote",
        "supercategory": "electronic"
    },
    {
        "id": 76,
        "name": "keyboard",
        "supercategory": "electronic"
    },
    {
        "id": 77,
        "name": "cell phone",
        "supercategory": "electronic"
    },
    {
        "id": 78,
        "name": "microwave",
        "supercategory": "appliance"
    },
    {
        "id": 79,
        "name": "oven",
        "supercategory": "appliance"
    },
    {
        "id": 80,
        "name": "toaster",
        "supercategory": "appliance"
    },
    {
        "id": 81,
        "name": "sink",
        "supercategory": "appliance"
    },
    {
        "id": 82,
        "name": "refrigerator",
        "supercategory": "appliance"
    },
    {
        "id": 84,
        "name": "book",
        "supercategory": "indoor"
    },
    {
        "id": 85,
        "name": "clock",
        "supercategory": "indoor"
    },
    {
        "id": 86,
        "name": "vase",
        "supercategory": "indoor"
    },
    {
        "id": 87,
        "name": "scissors",
        "supercategory": "indoor"
    },
    {
        "id": 88,
        "name": "teddy bear",
        "supercategory": "indoor"
    },
    {
        "id": 89,
        "name": "hair drier",
        "supercategory": "indoor"
    },
    {
        "id": 90,
        "name": "toothbrush",
        "supercategory": "indoor"
    }
],

ANNOTATOR_CATEGORIES = {
    'person': {'id': 1, 'is_crowd': True},
}


def main():
    """ Main entry point of the app """

    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    segmentation_id = 1
    image_id = 1

    for root, directories, files in os.walk(IMAGE_DIR):
        file_types = ['*.jpeg', '*.jpg']
        file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
        files = [os.path.join(root, f) for f in files]
        files = [f for f in files if re.match(file_types, f)]

        # go through each image
        for i, filename in enumerate(files):
            print(filename)
            parent_directory = root.split(os.path.sep)[-1]
            basename_no_extension = os.path.splitext(
                os.path.basename(filename))[0]
            image = Image.open(filename)
            image_info = pycococreatortools.create_image_info(
                image_id, os.path.basename(filename), image.size)
            #print(image_info)
            coco_output["images"].append(image_info)

            # go through each associated annotation
            for root, directories, files in os.walk(ANNOTATION_DIR):
                file_types = ['*.png']
                file_types = r'|'.join([fnmatch.translate(x)
                                        for x in file_types])
                file_name_prefix = basename_no_extension + '.*'
                files = [os.path.join(root, f) for f in files]
                files = [f for f in files if re.match(file_types, f)]
                files = [f for f in files if re.match(
                    file_name_prefix, os.path.splitext(os.path.basename(f))[0])]

                for filename in files:
                    parent_directory = root.split(os.path.sep)[-1]
                    basename_no_extension = os.path.splitext(
                        os.path.basename(filename))[0]
                    annotation_array = np.array(Image.open(filename))
                    # load annotation information
                    annotation_metadata = get_metadata(filename)
                    print(annotation_metadata)
                    annotation_data = AnnotationData(
                        annotation_array, annotation_metadata)
                    object_classes = annotation_data.get_classes()
                    #print(object_classes)

                    # go through each class
                    for j, object_class in enumerate(object_classes):
                        if ANNOTATOR_CATEGORIES.get(object_class) == None:
                            print("missing: {}".format(object_class))
                            continue

                        # go through each object
                        for object_instance in range(object_classes[object_class]):
                            object_mask = annotation_data.get_mask(
                                object_class, object_instance)
                            if object_mask is not None:
                                object_mask = object_mask.astype(np.uint8)

                                annotation_info = pycococreatortools.create_annotation_info(segmentation_id, image_id,
                                                                                            ANNOTATOR_CATEGORIES.get(object_class), object_mask, image.size, tolerance=2)
                                print(annotation_info)

                                if annotation_info is not None:
                                    coco_output["annotations"].append(
                                        annotation_info)
                                    segmentation_id = segmentation_id + 1

            image_id = image_id + 1

    with open('{}/coco.json'.format(DATA_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    main()
