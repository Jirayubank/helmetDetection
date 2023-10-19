# helmetDetection
[YOLOv8](https://github.com/ultralytics/ultralytics) powered Helmet Wearing Detection Project

``Dataset > Training > Validation > Detect > Control``   
is the main concept of this project 
Hook up arduino, python and AI object Detection together the form an AI security system

Firstly create virtual environment (ie. conda)
Then install the requirement lib for running detection 

```curl
pip install "requirements.txt"
```
before running the `detect-webcam.py` if you don't want to connect with arduino yet just commented it  
check your arduino com-port before running with arduino (ie. 'COM3' 'dev/tty')

**Dataset**  
[Dataset (Roboflow)](https://app.roboflow.com/bvoqueworkspace/helmet-wearing-detection-7yx0s/1)  

**Train Validation (Roboflow Notebook)**  
[Training Notebook](https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/train-yolov8-object-detection-on-custom-dataset.ipynb)  

**Other Document to read**  
[Yolov8 Docs](https://docs.ultralytics.com/)  
