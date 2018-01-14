import argparse
import json
import glob
import os

from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('data', metavar='d', type=str)
args = parser.parse_args()

empty_data = {'person': 0, 'bird': 0, 'cat': 0, 'cow': 0, 'dog': 0, 'horse': 0, 'sheep': 0, 'aeroplane': 0,
              'bicycle': 0, 'boat': 0, 'bus': 0, 'car': 0, 'motorbike': 0, 'train': 0,
              'bottle': 0, 'chair': 0, 'diningtable': 0, 'pottedplant': 0, 'sofa': 0, 'tvmonitor': 0}

metadata_template_name = '{}.metadata.json'


def get_file(base_path, path):
    filepath = os.path.join(base_path, path)
    return [l.strip() for l in open(filepath, 'rb').readlines()]


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def dump_metadata_file(base_path, filename, content):
    with open(os.path.join(base_path, metadata_template_name.format(filename)), 'w') as outfile:
        json.dump(content, outfile)


split_sets = defaultdict(set)

original_split_paths = glob.glob(os.path.join(args.data, 'ImageSets/Main/*.txt'))

for split_path in original_split_paths:
    t = get_file('', split_path)
    datapoint_splits = map(lambda x: x.split(' '), t)

    path_in_str = split_path
    clean_path = os.path.relpath(split_path, args.data)
    stem = os.path.splitext(os.path.basename(clean_path))[0]
    stems = stem.split('_')
    split = stems[-1]

    for datapoint in datapoint_splits:
        bucket = datapoint[0]
        value = int(datapoint[-1])

        if value == 1:
            s = split_sets[split]
            s.add(bucket)

LayoutTest = get_file(args.data, 'ImageSets/Layout/test.txt')
LayoutTrain = get_file(args.data, 'ImageSets/Layout/train.txt')
LayoutTrainVal = get_file(args.data, 'ImageSets/Layout/trainval.txt')
LayoutVal = get_file(args.data, 'ImageSets/Layout/val.txt')

SegmentationTest = get_file(args.data, 'ImageSets/Segmentation/test.txt')
SegmentationTrain = get_file(args.data, 'ImageSets/Segmentation/train.txt')
SegmentationTrainVal = get_file(args.data, 'ImageSets/Segmentation/trainval.txt')
SegmentationVal = get_file(args.data, 'ImageSets/Segmentation/val.txt')


def is_in_layout(bucket):
    return bucket in LayoutTrain or bucket in LayoutTrainVal or bucket in LayoutVal or bucket in LayoutTest


def is_in_segmentation(bucket):
    return bucket in SegmentationTrain or bucket in SegmentationTrainVal or bucket in SegmentationVal or bucket in SegmentationTest


def enrich_layout(bucket, data):
    data['LayoutTest'] = 1 if bucket in LayoutTest else 0
    data['LayoutTrain'] = 1 if bucket in LayoutTrain else 0
    data['LayoutTrainVal'] = 1 if bucket in LayoutTrainVal else 0
    data['LayoutVal'] = 1 if bucket in LayoutVal else 0
    return data


def enrich_segmentation(bucket, data):
    data['SegmentationTest'] = 1 if bucket in SegmentationTest else 0
    data['SegmentationTrain'] = 1 if bucket in SegmentationTrain else 0
    data['SegmentationTrainVal'] = 1 if bucket in SegmentationTrainVal else 0
    data['SegmentationVal'] = 1 if bucket in SegmentationVal else 0
    return data


def enrich(bucket, data):
    return enrich_segmentation(bucket, enrich_layout(bucket, data)) if is_in_layout(bucket) or is_in_segmentation(
        bucket) else data


def get_original_split(bucket):
    for split in ['train', 'test', 'val']:
        if bucket in split_sets[split]:
            return split


def get_layout_split(bucket):
    if is_in_layout(bucket):
        if bucket in LayoutTest:
            return 'test'
        if bucket in LayoutVal:
            return 'val'
        if bucket in LayoutTrain:
            return 'train'

    return None


def get_segmentation_split(bucket):
    if is_in_segmentation(bucket):
        if bucket in SegmentationTest:
            return 'test'
        if bucket in SegmentationVal:
            return 'val'
        if bucket in SegmentationTrain:
            return 'train'

    return None


class_data = {}

annotations = glob.glob(os.path.join(args.data, 'Annotations/*.xml'))
for path in annotations:
    import xml.etree.ElementTree

    e = xml.etree.ElementTree.parse(path)

    clean_path = os.path.relpath(path, args.data)
    bucket = os.path.splitext(os.path.basename(clean_path))[0]

    objects = e.findall('object')
    data = dict(empty_data)

    for o in objects:
        name = o.find('name').text
        data[name] += 1

    class_data[bucket] = data

metadataJson = {}  # 'file':{...}
pathlist = glob.glob(os.path.join(args.data, 'JPEGImages/*.jpg'))
for path in pathlist:
    # because path is object not string
    clean_path = os.path.relpath(path, args.data)
    bucket = os.path.splitext(os.path.basename(clean_path))[0]
    bucket_value = int(bucket)

    classes_data = dict(class_data[bucket])
    main_split = get_original_split(bucket)
    layout_split = get_layout_split(bucket)
    segmentation_split = get_segmentation_split(bucket)

    metadataJson[str(clean_path)] = enrich(bucket, merge_dicts(classes_data, {
        'type': 'Image',
        'MainSplit': main_split,
        'LayoutSplit': layout_split,
        'SegmentationSplit': segmentation_split,
        'bucket': bucket_value,
    }))

    dump_metadata_file(args.data, str(clean_path), metadataJson[str(clean_path)])

    metadataFilename = 'Annotations/{}.xml'.format(bucket)
    if os.path.exists(os.path.join(args.data, metadataFilename)):
        metadataJson[metadataFilename] = enrich(bucket, merge_dicts(classes_data, {
            'type': 'Annotation',
            'MainSplit': main_split,
            'LayoutSplit': layout_split,
            'SegmentationSplit': segmentation_split,
            'bucket': bucket_value,
        }))
        dump_metadata_file(args.data, metadataFilename, metadataJson[metadataFilename])

    metadataFilename = 'SegmentationClass/{}.png'.format(bucket)
    if os.path.exists(os.path.join(args.data, metadataFilename)):
        metadataJson[metadataFilename] = enrich(bucket, merge_dicts(classes_data, {
            'type': 'SegmentationClass',
            'MainSplit': main_split,
            'LayoutSplit': layout_split,
            'SegmentationSplit': segmentation_split,
            'bucket': bucket_value,
        }))
        dump_metadata_file(args.data, metadataFilename, metadataJson[metadataFilename])

    metadataFilename = 'SegmentationObject/{}.png'.format(bucket)
    if os.path.exists(os.path.join(args.data, metadataFilename)):
        metadataJson[metadataFilename] = enrich(bucket, merge_dicts(classes_data, {
            'type': 'SegmentationObject',
            'MainSplit': main_split,
            'LayoutSplit': layout_split,
            'SegmentationSplit': segmentation_split,
            'bucket': bucket_value,
        }))
        dump_metadata_file(args.data, metadataFilename, metadataJson[metadataFilename])
