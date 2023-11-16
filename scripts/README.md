# The Helmet-Wearing Detection with Deel Learning

Using Hikvision IP camera as a input, Using YOLOv8 as a predict and detection then send
the data to arduino to further microcontroller implementation

**Installation**

create an `conda` env by

```curl
conda create -n YOUR_ENV_NAME
```
When finished create env then install the requirements library

```curl
pip install "requirements.txt"
```

when The installation has done move on to the inference

**Inference**

Go to `main.py` make change to `path_model`, `com_port` and `source`
then run the scripts

**Troubleshooting**
- can't open the arduino port
  - try close and rerun again maybe the arduino com port is busy

