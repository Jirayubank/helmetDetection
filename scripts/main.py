import threading
from helmetDetection import HelmetDetection


def main():
    model = 'modelPath'
    com_port = 'comPort'
    source = 0
    helmet = HelmetDetection(
        path_model=model,
        source=source,
        is_serial=False,
        is_mqtt=False,
        com_port=com_port
    )
    helmet.detectionRun()


# run here
if __name__ == '__main__':
    m = threading.Thread(target=main)
    m.start()
