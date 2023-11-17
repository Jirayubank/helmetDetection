# The Helmet-Wearing Detection with Deel Learning

Using Hikvision IP camera as input, Using YOLOv8 as a prediction and detection then sending the data to Arduino to further microcontroller implementation

**Installation**

Create a `conda` env by

```curl
conda create -n YOUR_ENV_NAME
```
When finished create env then install the requirements library

```curl
pip install "requirements.txt"
```

**Inference**

Go to `main.py` make change to `path_model`, `com_port` and `source`
then run the scripts

**Troubleshooting**
- can't open the Arduino port
  - try close and rerunning maybe the Arduino com port is busy

