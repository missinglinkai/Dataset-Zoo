#!/usr/bin/env bash
echo "Downloading the data...."
rm -rf temp/
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar -P temp/
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar -P temp/

echo "Extracting ..."
rm -rf data/
mkdir data

tar xf temp/VOCtrainval_06-Nov-2007.tar -C data/ --strip-components=1
tar xf temp/VOCtest_06-Nov-2007.tar -C data/ --strip-components=1

echo "Cleaning ...."
mv data/VOC2007/* data
rm -rf data/VOC2007

echo "Done."