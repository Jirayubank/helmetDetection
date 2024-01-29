import argparse
import threading
from helmetDetection import HelmetDetection

parser = argparse.ArgumentParser()
parser.add_argument('-path', '--model', required=True,
                    help="Path of YOLOv8 model")
parser.add_argument('-s', '--source', required=True,
                    help="Detection source")
parser.add_argument('-isArduino', '--is_serial', required=False,
                    help="Enable serial communication", default=False)
parser.add_argument('-isMqtt', '--is_mqtt', required=False,
                    help="Enable mqtt communication", default=False)
parser.add_argument('-comPort', '--com_port', required=False,
                    help="required if isArduino is Enable", default='COM8')

args = parser.parse_args()


def main():
    helmet = HelmetDetection(
        path_model=args.model,
        source=args.source,
        is_serial=args.is_serial,
        is_mqtt=args.is_mqtt,
        com_port=args.com_port,
        rect_wh=500
    )
    helmet.detectionRun()


# run here
if __name__ == '__main__':
    m = threading.Thread(target=main)
    m.start()
