# EM-Imagenet

The EM algorithm implemented over a subset of ImageNet using the ImageNet-ReaL labels as ground truth for performance analysis

## EM Execution instructions
<b>Since the labels acquired from the LLM models themselves are already stored in this repository, it is possible to execute the EM algorithm without the actual dataset and without collecting labels from the LLM models
in order to execute the EM algorithm and produce the project deliverables, one must simply execute</b>

```
python3 main.py
```

on a machine (or virtual environment) with matplotlib installed via

```
pip3 install matplotlib
```

This will print the various metrics that were taken and also produce graphs and confusion matrices and labeled image filenames in ./results/

## Data collection instructions
This repository needs all the images from ILSVRC2012_img_val.tar to be placed in assets/images/ in order to execute classify_images.py and classify_images_grok.py. (These are the scripts used to obtain classification labels from the LLMs) You can sign up for access here. https://www.image-net.org/
<br>
In addition, grok and OpenAI keys must be set as environment variables as XAI_API_KEY and OPENAI_API_KEY respectively. Overall the process of generating this data cost about $30 in AI tokens more or less.
<br>
Once this is done, you can invoke
```
python3 classify_images.py ./assets/image_names.txt [output_file_name] [openai model name]
```
to start classifying images. For grok, we only use 1 model so it is hardcoded into the script. For this you can simply invoke
```
python3 classify_images_grok.py ./assets/image_names.txt [output_file_name]
```
After this, the output of these programs must be further processed by convert_to_json.py, which puts them into a json format with the numerical class designations replaced with class names.
Overall, the process to acquire the data from the LLMs is
```
# Obtain labels from LLM models (warning, costs about $30)
python3 classify_images.py ./assets/image_names.txt ./llm_classifications/gpt41mini_classifications.txt gpt-4.1-mini
python3 classify_images.py ./assets/image_names.txt ./llm_classifications/gpt41nano_classifications.txt gpt-4.1-nano
python3 classify_images.py ./assets/image_names.txt ./llm_classifications/gpt4o_classifications.txt gpt-4o
python3 classify_images_grok.py ./assets/image_names.txt  ./llm_classifications/grok2_classifications.txt

# Convert labels to json format
python3 convert_to_json ./llm_classifications/gpt41mini_classifications.txt > ./llm_classifications/gpt41mini_classifications.json
python3 convert_to_json ./llm_classifications/gpt41nano_classifications.txt > ./llm_classifications/gpt41nano_classifications.json
python3 convert_to_json ./llm_classifications/gpt4o_classifications.txt > ./llm_classifications/gpt4o_classifications.json
python3 convert_to_json ./llm_classifications/grok2_classifications.txt > ./llm_classifications/grok2_classifications.json
```
<br>

