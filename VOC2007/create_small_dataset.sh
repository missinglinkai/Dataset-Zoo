#!/usr/bin/env bash
DEFAULTNUMBEROFITEMS=10
DEFAULTTARGETDIR=small_dataset

NUMBEROFITEMS=${1:-$DEFAULTNUMBEROFITEMS}
TARGETDIR=${2:-$DEFAULTTARGETDIR}

mkdir -p $TARGETDIR/Annotations
mkdir -p $TARGETDIR/JPEGImages

#get the first $1 files from the source folder into a $2
find data/Annotations -maxdepth 1 -type f | sort | head -$NUMBEROFITEMS | xargs -I{} cp {} $TARGETDIR/Annotations
find data/JPEGImages  -maxdepth 1 -type f | sort | head -$NUMBEROFITEMS | xargs -I{} cp {} $TARGETDIR/JPEGImages
