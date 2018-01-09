### Download the dataset

Run `./download_data.sh` - it will download the dataset (train, val and test) and place them under the data folder

### Run the script to generate metadata

`./create_metadata.py ./data`

### Clean the data folder
Before uploading the metadata we need to remove some unneeded 
`rm -rf ./data/ImageSets`

### Sync the data:

`mali data sync [VOLUME ID] --dataPath ./data`

### Commit the version

`mali data commmit [VOLUME ID] -m [Message]`


![Query Console with Properties](resources/image1.png)



Original Dataset from: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/
Documentation: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/htmldoc/voc.html


Dataset files: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar and http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar 

http://academictorrents.com/details/c9db37df1eb2e549220dc19f70f60f7786d067d4

