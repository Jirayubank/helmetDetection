from ultralytics import YOLO
import cv2
import supervision as sv
import numpy
import subprocess
import threading
import serial
import paho.mqtt.client as mqtt


class HelmetDetection:
    def __init__(self, path_model: str, com_port: str, source, is_mqtt: bool, is_serial: bool):
        self.model = YOLO(path_model, task='detect')
        self.isSerial = is_serial
        self.isMqtt = is_mqtt
        self.source = source
        self.img_size = 416
        self.color = sv.Color.from_hex('#17e87f')

        if self.isSerial:
            self.port = serial.Serial(com_port, 9600)

        if self.isMqtt:
            self.cli = mqtt.Client()
            self.cli.connect("localhost", 1883, 60)

        if type(self.source) != int:
            self.zone_in = numpy.array([
                [1200, 250],
                [1200, 800],
                [500, 800],
                [500, 250]
            ])
            self.w = 1600
            self.h = 800

        else:
            self.zone_in = numpy.array([
                [100, 250],
                [100, 500],
                [400, 500],
                [400, 250]
            ])
            self.w = 500
            self.h = 500

    def detectionRun(self):
        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=1,
            text_scale=0.5
        )

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
                    mq = threading.Thread(target=self.mqttPaho(args))
                    mq.start()

            frame = box_annotator.annotate(
                scene=frames,
                detections=detections,
                labels=labels
            )

            self.interface(frame, args, fps)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def interface(self, frame: numpy.ndarray, args: numpy.ndarray, fps: float):
        sv.draw_polygon(frame, self.zone_in, self.color)
        if self.decision(args, 0.6) == 0:
            msg = "Please Wear Helmet!!!"
        elif self.decision(args, 0.6) == 1:
            msg = "Good to go!!!"
        else:
            msg = "For you safety ride"
        sv.draw_text(frame, text=f"{int(fps)}/30fps",
                     text_anchor=sv.Point(x=80, y=20),
                     text_color=self.color,
                     text_scale=0.7,
                     text_thickness=2)
        sv.draw_text(frame, text=f"{msg}",
                     text_anchor=sv.Point(x=800, y=100),
                     text_color=self.color,
                     text_scale=1,
                     text_thickness=2)

        cv2.imshow('Detection', frame)

    def arduino(self, class_id: numpy.ndarray, threshold=0.6):
        decision = self.decision(class_id=class_id, threshold=threshold)
        while True:
            if decision:
                self.port.write(b'1')
                break
            elif not decision:
                self.port.write(b'0')
                break

    def mqttPaho(self, class_id: numpy.ndarray, threshold=0.6):
        decision = self.decision(class_id=class_id, threshold=threshold)
        if decision:
            self.cli.publish("/py", "on")
        elif not decision:
            self.cli.publish("/py", "off")
            # self.cli.disconnect()
        return

    @classmethod
    def decision(cls, class_id: numpy.ndarray, threshold: float):
        decision = numpy.average(class_id)
        if decision >= threshold:
            decision = 1
        else:
            decision = 0
        return decision
