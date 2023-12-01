import threading
from helmetDetection import HelmetDetection


def main():
    model = 'YOLOv8s-ver6-2111.onnx'
    com_port = 'COM8'
    # source = 'rtsp://admin:tatc1234@192.168.1.64:554/Streaming/Channels/101'
    source = 0
    helmet = HelmetDetection(
        path_model=model,
        source=source,
        is_serial=False,
        is_mqtt=False,
        com_port=com_port,
        rect_wh=300
    )
    helmet.detectionRun()


# run here
if __name__ == '__main__':
    m = threading.Thread(target=main)
    m.start()
