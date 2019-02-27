### Setup Environment
create a new virtualenv and install the requirements.txt

### Download the dataset

Prerequisite - you need to have `wget` available on your machine.
On OSX, run `brew install wget` if you don't have it installed.

Run `./download_data.sh` - it will download the dataset (train, val and test) and place them under the data folder

### Run the script to generate metadata

`python ./create_metadata.py ./data`

### Clean the data folder
Before uploading the metadata we need to remove some unneeded files


`rm -rf ./data/ImageSets`

### Sync the data:
We need to sync the data to a specific data volume. To list the data volumes you have access to run:

`ml data list`

It should produce a list of data volumes with ID's. You can create a new data volume on the console.


Once you have a Volume ID sync the data folder into it.

`ml data sync [VOLUME ID] --data-path ./data`

### Commit the version

`ml data commmit [VOLUME ID] -m [Message]`


![Query Console with Properties](resources/image1.png)



Original Dataset from: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/
Documentation: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/htmldoc/voc.html


Dataset files: http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar and http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar 

http://academictorrents.com/details/c9db37df1eb2e549220dc19f70f60f7786d067d4

