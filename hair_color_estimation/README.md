
# Hair Color Estimation

Finds the hair color of a person from an image.
Based on https://github.com/aobo-y/hair-dye

## Directory Structure
```
hair_seg
    │   dataset.py
    │   evaluate.py
    │   main.py
    │
    ├───checkpoints
    │   └───default
    │           train_16.tar
    │
    ├───models
    │       hairnet.py
    │       unit.py
    │       __init__.py
    │
    └───utils
            checkpoint.py
            image.py
            __init__.py
```

## How to run?
1. clone the repo

2. install requirements from requirements.txt
`pip install -r requirements.txt`

3. get checkpoint from [here](https://drive.google.com/file/d/1x_QFQwX7WcqruU4fjXeNgHKhs7n2uzpp/view?usp=sharing) and copy the file to `hair_seg/checkpoints/default/`
(refer [Directory Structure](#directory-structure) for more detail)

4. run main.py and pass an additional argument as the image path
 `python hair_seg/main.py path/to/image.jpg`