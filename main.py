import threading
import helmetDetection


def main():
    model = 'YOLOv8s-ver4-1611.onnx'
    com_port = 'COM8'
    source = 'rtsp://admin:tatc1234@192.168.1.64:554/Streaming/Channels/101'
    helmet = helmetDetection.HelmetDetection(path_model=model,
                                             com_port=com_port,
                                             source=source
                                             )
    helmet.detectionRun()


# run here
if __name__ == '__main__':
    m = threading.Thread(target=main)
    m.start()
