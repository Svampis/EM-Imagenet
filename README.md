# EM-Imagenet

The EM algorithm implemented over a subset of ImageNet using the ImageNet-ReaL labels as ground truth for performance analysis

This repository needs all the images from ILSVRC2012_img_val.tar to be placed in assets/images/ in order to execute classify_images.py and classify_images_grok.py. (These are the scripts used to obtain classification labels from the LLMs) You can sign up for access here. https://www.image-net.org/
<br>
In addition, this folder needs to be hosted over an https server and the URL contained in classify_images.py and classify_images_grok.py replaced with the URL they are hosted at so that this URL can be given to grok and OpenAI's LLM models so that they can download the images.
<br>
In addition, grok and OpenAI keys must be set as environment variables as XAI_API_KEY and OPENAI_API_KEY respectively. Overall the process of generating this data cost about $30 in API tokens more or less.
<br>
I would also recommend downscaling the images using ffmpeg to reduce API token use and upload time.
<br>
<b>That being said, since the labels acquired from these models, along with the ReaL labels are already stored in this repository, this step is not needed in order to run the EM algorithm itself.</b>
in order to execute the EM algorithm and produce the project deliverables, one must simply execute
```
python3 main.py
```
on a machine (or virtual environment) with matplotlib installed via
```
pip3 install matplotlib
```
This will print the various metrics that were taken and also produce graphs and confusion matrices and labeled image filenames in ./results/
