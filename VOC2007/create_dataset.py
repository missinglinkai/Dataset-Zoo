from pathlib import Path
import argparse
import json
from faker import Faker
import xml.etree.ElementTree
from bs4 import BeautifulSoup

fake = Faker()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('data', metavar='d', type=str, help='an integer for the accumulator')
args = parser.parse_args()

empty_data = {'person': 0, 'bird': 0, 'cat': 0, 'cow': 0, 'dog': 0, 'horse': 0, 'sheep': 0, 'aeroplane': 0,
              'bicycle': 0, 'boat': 0, 'bus': 0, 'car': 0, 'motorbike': 0, 'train': 0,
              'bottle': 0, 'chair': 0, 'diningtable': 0, 'pottedplant': 0, 'sofa': 0, 'tvmonitor': 0}


def get_file(base_path, path):
    lines = set(map(lambda x: str(x).strip('\n'), open(str(Path(base_path).joinpath(path).absolute()), 'r')))
    return lines


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


LayoutTrain = get_file(args.data, 'Metadata/ImageSets/Layout/train.txt')
LayoutTrainVal = get_file(args.data, 'Metadata/ImageSets/Layout/trainval.txt')
LayoutVal = get_file(args.data, 'Metadata/ImageSets/Layout/val.txt')

SegmentationTrain = get_file(args.data, 'Metadata/ImageSets/Segmentation/train.txt')
SegmentationTrainVal = get_file(args.data, 'Metadata/ImageSets/Segmentation/trainval.txt')
SegmentationVal = get_file(args.data, 'Metadata/ImageSets/Segmentation/val.txt')


def is_in_layout(bucket):
    return bucket in LayoutTrain or bucket in LayoutTrainVal or bucket in LayoutVal


def is_in_segmentation(bucket):
    return bucket in SegmentationTrain or bucket in SegmentationTrainVal or bucket in SegmentationVal


def enrich_layout(bucket, data):
    data['LayoutTrain'] = 1 if bucket in LayoutTrain else 0
    data['LayoutTrainVal'] = 1 if bucket in LayoutTrainVal else 0
    data['LayoutVal'] = 1 if bucket in LayoutVal else 0
    return data


def enrich_segmentation(bucket, data):
    data['SegmentationTrain'] = 1 if bucket in SegmentationTrain else 0
    data['SegmentationTrainVal'] = 1 if bucket in SegmentationTrainVal else 0
    data['SegmentationVal'] = 1 if bucket in SegmentationVal else 0
    return data


def enrich(bucket, data):
    return enrich_segmentation(bucket, enrich_layout(bucket, data)) if is_in_layout(bucket) or is_in_segmentation(
        bucket) else data


class_data = {}

annotations = Path(args.data).glob('Annotations/*.xml')
for path in annotations:
    with open(str(Path(path).absolute())) as fp:
        soup = BeautifulSoup(fp)

    path_in_str = str(path)
    clean_path = path.relative_to(args.data)
    stem = clean_path.stem
    bucket = str(stem)

    objects = soup.findAll("object")
    data = dict(empty_data)

    for o in objects:
        name = o.contents[1].contents[0]
        data[name] = data[name] + 1 if data.has_key(name) else 1
    class_data[bucket] = data

metadataJson = {}  # 'file':{...}
pathlist = Path(args.data).glob('JPEGImages/*.jpg')
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    clean_path = path.relative_to(args.data)
    name = clean_path.name
    stem = clean_path.stem
    bucket = str(stem)

    classes_data = dict(class_data[bucket])

    metadataJson[str(clean_path)] = enrich(bucket, merge_dicts(classes_data, {
        'type': 'Image',
        'bucket': bucket,
    }))

    metadataFilename = 'Annotations/{}.xml'.format(stem)
    metadataJson[metadataFilename] = enrich(bucket, merge_dicts(classes_data, {
        'type': 'Annotation',
        'bucket': bucket,
    }))

    metadataFilename = 'SegmentationClass/{}.png'.format(stem)
    if Path(args.data).joinpath(metadataFilename).exists():
        metadataJson[metadataFilename] = enrich(bucket, merge_dicts(classes_data, {
            'type': 'SegmentationClass',
            'bucket': bucket,
        }))

    metadataFilename = 'SegmentationObject/{}.png'.format(stem)
    if Path(args.data).joinpath(metadataFilename).exists():
        metadataJson[metadataFilename] = enrich(bucket, merge_dicts(classes_data, {
            'type': 'SegmentationObject',
            'bucket': bucket,
        }))

with open('metadata.json', 'w') as outfile:
    json.dump(metadataJson, outfile)
