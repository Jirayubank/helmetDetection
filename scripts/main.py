import threading
from helmetDetection import HelmetDetection


def main():
    model = 'YOLOv8s-ver6-2111.onnx'
    com_port = 'COM3'
    source = 0
    helmet = HelmetDetection(
        path_model=model,
        source=source,
        is_serial=True,
        is_mqtt=True,
        com_port=com_port,
        rect_wh=300
    )
    helmet.detectionRun()


# run here
if __name__ == '__main__':
    m = threading.Thread(target=main)
    m.start()
