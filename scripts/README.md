# The Helmet-Wearing Detection with Deel Learning

Using Hikvision IP camera as input, Using YOLOv8 as a prediction and detection then sending the data to Arduino to further microcontroller implementation

**Installation**

Install a `conda` env by

```curl
conda env create -f environment.yml
```

**Inference**

Go to `main.py` make change to `path_model`, `com_port` and `source`
if you going to use Arduino 
```curl
is_serial=True
```
or Mqtt 
```curl
is_mqtt=True
```
if not using pass `False`
then run the scripts

**Troubleshooting**
- can't open the Arduino port
  - try close and rerunning maybe the Arduino com port is busy

