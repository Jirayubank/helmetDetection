# The Helmet-Wearing Detection with Deep Learning

Easier to use the code, please use the `environment.yml` file to create a `conda` environment.
Run the program via command-line check out the guide below.

## Installation
**Conda**

Install a `conda` env by

```curl
conda env create -f environment.yml
```
check the official guide [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)

**Pip**

Install a `pip` env by

```curl
pip install -r requirements.txt
```

## Usage
**Run the program**

```curl
python main.py model source
```
Replace model with your actual model path and replace source with your actual video path

**Arduino Enable**
```curl
python main.py model source -a True -cP 'COM_PORT'
```
Replace COM_PORT with your actual COM port

**Mqtt Enable**
```curl
python main.py model source -mq True -H 'HOST' -P 'PORT' -u 'USERNAME' -p 'PASSWORD'
```
Make sure that the mqtt broker is running and the mqtt client is connected to the broker
And your current directory is `scripts`.

## Troubleshooting

**Conda**
- can't find the `conda` command
  - make sure that you have `conda` installed

**Arduino**
- can't open the Arduino port
  - try close and rerunning maybe the Arduino com port is busy

