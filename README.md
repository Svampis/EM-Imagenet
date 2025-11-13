# EM-Imagenet

The EM algorithm implemented over a subset of ImageNet using the ImageNet-ReaL labels as ground truth for performance analysis

This repository needs all the images from ILSVRC2012_img_val.tar to be placed in assets/images/ in order to execute classify_images.py and classify_images_grok.py.
Since the labels themselves are already stored in this repository, this step is not necessarily needed in order to run the EM algorithm itself.
That being said, in order to execute the EM algorithm and produce the project deliverables, one must simply execute 
```
python3 main.py
```
on a machine with matplotlib installed via
```
pip3 install matplotlib
```
 
