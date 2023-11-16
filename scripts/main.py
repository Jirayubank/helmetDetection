import threading
import helmetDetection


def main():
    model = 'YOLOv8s-ver4-1611.onnx'
    com_port = 'com port of arduino (check devmgmt.msc)'
    source = 'your input source'
    helmet = helmetDetection.HelmetDetection(path_model=model,
                                             com_port=com_port,
                                             source=source
                                             )
    helmet.detectionRun()


# run here
if __name__ == '__main__':
    m = threading.Thread(target=main)
    m.start()
