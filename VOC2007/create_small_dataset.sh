mkdir -p small_dataset/Annotations
mkdir -p small_dataset/JPEGImages

#get the first 10 files from the source folder into a small_dataset
find data/Annotations -maxdepth 1 -type f| sort |head -10 | xargs -I{} cp {} small_dataset/Annotations
find data/JPEGImages -maxdepth 1 -type f| sort | head -10 | xargs -I{} cp {} small_dataset/JPEGImages
