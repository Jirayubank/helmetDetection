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
parser.add_argument('-user', '--mqtt_user', required=False,
                    help="setting username for mqtt", default='user')
parser.add_argument('-mqPass', '--mqtt_pass', required=False,
                    help="setting password for mqtt", default='pass')
parser.add_argument('-host', '--mqtt_host', required=False,
                    help="setting host for mqtt", default='localhost')
parser.add_argument('-port', '--mqtt_port', required=False,
                    help="setting port of mqtt host", default=1883)

args = parser.parse_args()


def main():
    helmet = HelmetDetection(
        path_model=args.model,
        source=args.source,
        is_serial=args.is_serial,
        is_mqtt=args.is_mqtt,
        mqtt_host=args.mqtt_host,
        mqtt_port=args.mqtt_port,
        mqtt_user=args.mqtt_user,
        mqtt_pass=args.mqtt_pass,
        com_port=args.com_port,
        rect_wh=500
    )
    helmet.detectionRun()


# run here
if __name__ == '__main__':
    m = threading.Thread(target=main)
    m.start()
