# EM-Imagenet

The EM algorithm implemented over a subset of ImageNet using the ImageNet-ReaL labels as ground truth for performance analysis

This repository needs all the images from ILSVRC2012_img_val.tar to be placed in assets/images/ in order to execute classify_images.py and classify_images_grok.py.
In addition, this folder needs to be hosted over an http server and the URL contained in classify_images.py and classify_images_grok.py replaced with the URL they are hosted at.
In addition, grok and OpenAI keys must be set as environment variables as XAI_API_KEY and OPENAI_API_KEY respectively. Overall the process of generating this data cost about $30 in AI tokens more or less.
<br><br>
That being said, since the labels themselves are already stored in this repository, this step is not necessarily needed in order to run the EM algorithm itself.
in order to execute the EM algorithm and produce the project deliverables, one must simply execute 
```
python3 main.py
```
on a machine with matplotlib installed via
```
pip3 install matplotlib
```
 
