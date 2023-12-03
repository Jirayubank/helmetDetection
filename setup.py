from setuptools import setup, find_packages

setup(
    name='helmetDetection',
    version='1',
    packages=find_packages(),
    install_requires=[
        'pyserial==3.5',
        'numpy==1.26.0',
        'supervision==0.15.0',
        'ultralytics==8.0.196',
        'opencv-python==4.8.1.78',
        'paho-mqtt==1.6.1'
    ],
    url='https://github.com/Jirayubank/helmetDetection',
    license='',
    author='BankkV',
    author_email='jirayubank10@gmail.com',
    description='Helmet-Wearing Detection with Deep Learning usage YOLOv8',
    keywords='YOLOv8, deep learning, computer vision'
)
