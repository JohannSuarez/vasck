#! /bin/bash




# For each file in the given directory, use jp2a on it,
# pipe the text file into a folder, with the txt file name based 
# on its jpeg.


# You also need to check the folder.
# Create it, otherwise clean it

if [ -d jpeg_images/ ]
then 
  echo "JPEG directory found."
else 
  echo "ERROR: JPEG directory not found. Creating"
  mkdir jpeg_images
fi  


if [ -d ascii/ ]
then 
  echo "Ascii Directory found. Cleaning.."
  rm -rf ascii/*
else 
  echo "Ascii directory not found. Creating.."
  mkdir ascii
fi  

for item in jpeg_images/*.jpg ; do

  # For each jpeg file in jpeg_images/
  # Run jp2a on it, and save its output to ascii/

  txt_name=${item%.*}
  stripped_text_name=${txt_name##*/}
  folder="ascii/${stripped_text_name}.txt"
  echo "Output name is ${folder}"
  jp2a ${item} > ${folder}

done
  
