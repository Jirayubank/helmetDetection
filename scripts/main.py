import argparse
import threading
from helmetDetection import HelmetDetection

parser = argparse.ArgumentParser()
parser.add_argument('model', help="Path of YOLOv8 model")
parser.add_argument('source', help="Detection source")
parser.add_argument('-a', '--arduino',
                    help="Enable serial communication", default=False)
parser.add_argument('-mq', '--mqtt',
                    help="Enable mqtt communication", default=False)
parser.add_argument('-cP', '--com_port',
                    help="required if isArduino is Enable", default='COM8')
parser.add_argument('-u', '--user',
                    help="setting username for mqtt", default='user')
parser.add_argument('-pw', '--password',
                    help="setting password for mqtt", default='pass')
parser.add_argument('-H', '--host',
                    help="setting host for mqtt", default='localhost')
parser.add_argument('-P', '--mqtt_port',
                    help="setting port of mqtt host", default=1883)

args = parser.parse_args()


def main():
    helmet = HelmetDetection(
        path_model=args.model,
        source=args.source,
        is_serial=args.arduino,
        is_mqtt=args.mqtt,
        mqtt_host=args.host,
        mqtt_pass=args.password,
        mqtt_user=args.user,
        mqtt_port=args.mqtt_port,
        com_port=args.com_port,
        rect_wh=500
    )
    helmet.detectionRun()


if __name__ == '__main__':
    m = threading.Thread(target=main)
    m.start()
