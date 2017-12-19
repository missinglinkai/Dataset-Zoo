Original Dataset from: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/
Documentation: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/htmldoc/voc.html


Dataset files: http://academictorrents.com/details/c9db37df1eb2e549220dc19f70f60f7786d067d4

### Install

1. Create a new virtualenv
2. run `pip install -r requirements.txt`
3. download the dataset into 'data' folder. the dataset includes to zipped files - one for trainval and one for test. 
Merge the two extracted folders. 
You should have 5 folders under data: 
    * 'Annotations' 
    * 'ImageSets' 
    * 'JPEGImages' 
    * 'SegmentationClass' 
    * 'SegmentationObject'
4. run `python create_dataset.py ./data` - this will produce a metadata.json file.

### Upload the data files
Now that the metadata.json was produced you can safely remove the `ImageSets` folder. 
we will not upload the metadata files.

`mali data add [VOLUME ID] --files ./data`

### Upload metadata:

`mali data metadata add [VOLUME ID] -df metadata.json`
