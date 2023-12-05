from ultralytics import YOLO
import cv2
import supervision as sv
import numpy
import subprocess
import threading
import serial
import paho.mqtt.client as mqtt


class HelmetDetection:
    """
    Class for helmet detection using YOLO model.

    Args:
        path_model (str): Path to the YOLO model.
        source: Image source for detection. If an integer, it represents the camera index;
                if a string, it represents the path to an image or video file.
        is_mqtt (bool): Flag indicating whether MQTT (Message Queuing Telemetry Transport) is enabled.
        is_serial (bool): Flag indicating whether serial communication is enabled.
        com_port (str, optional): COM port for serial communication if `is_serial` is True.
        rect_wh (int, optional): Width and height of the rectangular detection zone (default is 300).

    Attributes:
        model: YOLO model instance for object detection.
        isSerial (bool): Flag indicating whether serial communication is enabled.
        isMqtt (bool): Flag indicating whether MQTT is enabled.
        source: Image source for detection.
        img_size (int): Size of the input image for detection.
        rect_wh (int): Width and height of the rectangular detection zone.
        color (str): Color for visualizations.
        port (str): Serial port instance if `is_serial` is True.
        cli: MQTT Client instance if `is_mqtt` is True.
        zone_in (numpy.ndarray): Coordinates defining the detection zone.
        w (int): Width of the detection zone.
        h (int): Height of the detection zone.

    Methods:
        detectionRun(): Run the helmet detection process.
        interface(frames, detections, labels, args, fps): Display the detection interface.
        arduino(class_id, threshold): Communicate with Arduino based on detection results.
        mqttPaho(class_id, threshold): Publish MQTT messages based on detection results.
        decision(class_id, threshold): Make a decision based on the average confidence of detected classes.
        setColor(hex_color): Set color based on a hexadecimal color code.

    Note:
        The `detectionRun` method continuously performs helmet detection and updates the interface
        with real-time information. It also communicates with Arduino and/or publishes MQTT messages
        based on detection results.
    """
    # TODO: segmentation mode

    def __init__(self, path_model: str, source, is_mqtt: bool, is_serial: bool, com_port=None, rect_wh=300) -> None:
        self.model = YOLO(path_model, task='detect')
        self.isSerial = is_serial
        self.isMqtt = is_mqtt
        self.source = source
        self.img_size = 416
        self.rect_wh = rect_wh

        if self.isSerial and com_port is not None:
            self.port = serial.Serial(com_port, 9600)

        if self.isMqtt:
            self.cli = mqtt.Client()
            self.cli.connect("localhost", 1883, 60)

        if not isinstance(self.source, int):
            self.w = 1600
            self.h = 800
        else:
            self.w = 640
            self.h = 480
        center_x = self.w / 2
        center_y = self.h / 2
        self.zone_in = numpy.array([
            [(center_x - (self.rect_wh / 2)), (center_y - (self.rect_wh / 2))],
            [(center_x - (self.rect_wh / 2)), (center_y + (self.rect_wh / 2))],
            [(center_x + (self.rect_wh / 2)), (center_y + (self.rect_wh / 2))],
            [(center_x + (self.rect_wh / 2)), (center_y - (self.rect_wh / 2))]
        ])
        self.zone_in = self.zone_in.astype(int)

    def detectionRun(self):
        for results in self.model.predict(
                source=self.source,
                show=False,
                stream=True,
                imgsz=(self.img_size, self.img_size),
                agnostic_nms=True,
                conf=0.5
        ):
            frames = results.orig_img
            infer_speed = results.speed['inference']
            fps = 1000 / infer_speed

            zone = sv.PolygonZone(self.zone_in, (self.w, self.h))
            detections = sv.Detections.from_ultralytics(results)
            mask = zone.trigger(detections=detections)
            detections = detections[mask]

            labels = [
                f"{results.names[class_id]} {confidence * 100:0.2f}"
                for _, _, confidence, class_id, _
                in detections
            ]
            args = numpy.ndarray([])
            if detections.class_id.size > 0:
                args = detections.class_id
            elif detections.class_id.size == 0:
                args = numpy.ndarray([0])

            if args.size != 0:
                if self.isSerial:
                    a = threading.Thread(target=self.arduino(args))
                    a.start()
                if self.isMqtt:
                    mq = threading.Thread(target=self.mqttPaho, args=args)
                    mq.start()

            self.interface(
                frames=frames,
                detections=detections,
                labels=labels,
                args=args,
                fps=fps
            )
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def interface(self, frames, detections, labels, args, fps):
        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=1,
            text_scale=0.5
        )
        frame = box_annotator.annotate(
            scene=frames,
            detections=detections,
            labels=labels
        )
        sv.draw_polygon(frame, self.zone_in, self.setColor('17e87f'))
        if self.decision(args, 0.6) == 0:
            msg = "Please Wear Helmet!!!"
        elif self.decision(args, 0.6) == 1:
            msg = "Good to go!!!"
        else:
            msg = "For you safety ride"
        msg_x = int(self.w / 2)
        msg_y = int(self.h * 0.125)
        fps_x = int(self.w / 10)
        fps_y = int(self.h * 0.025)

        sv.draw_text(frame, text=f"{int(fps)}/30fps",
                     text_anchor=sv.Point(x=fps_x, y=fps_y),
                     text_color=self.setColor('7c2de2'),
                     text_scale=0.7,
                     text_thickness=2)
        sv.draw_text(frame, text=f"{msg}",
                     text_anchor=sv.Point(x=msg_x, y=msg_y),
                     text_color=self.setColor('ef709b'),
                     text_scale=1,
                     text_thickness=2)

        cv2.imshow('Detection', frame)

    def arduino(self, class_id, threshold=0.6):
        decision = self.decision(class_id=class_id, threshold=threshold)
        while True:
            if decision:
                self.port.write(b'1')
                break
            elif not decision:
                self.port.write(b'0')
                break

    def mqttPaho(self, class_id: numpy.ndarray, threshold=0.6):
        if self.decision(class_id=class_id, threshold=threshold):
            self.cli.publish("/py", "on")
        else:
            self.cli.publish("/py", "off")
        return

    @staticmethod
    def setColor(hex_color: str):
        color = sv.Color.from_hex(hex_color)
        return color

    @staticmethod
    def decision(class_id: numpy.ndarray, threshold: float) -> int:
        return 1 if numpy.average(class_id) >= threshold else 0
