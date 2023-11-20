import serial
from ultralytics import YOLO
import supervision as sv
import numpy
import threading
import cv2


class HelmetDetection:
    def __init__(self, path_model: str, com_port: str, source):
        self.path = path_model
        self.model = YOLO(self.path, task='detect')
        self.port = serial.Serial(com_port, 9600)
        self.source = source
        self.img_size = 416
        self.color = sv.Color.from_hex('#17e87f')
        self.zone_in = numpy.array([[1200, 250],
                                    [1200, 800],
                                    [500, 800],
                                    [500, 250]])

    def detectionRun(self):
        box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=1,
            text_scale=0.5
        )

        for results in self.model.predict(source=self.source,
                                          show=False,
                                          stream=True,
                                          imgsz=(self.img_size, self.img_size),
                                          agnostic_nms=True,
                                          conf=0.5):

            frames = results.orig_img
            infer_speed = results.speed['inference']
            fps = 1000 / infer_speed
            zone = sv.PolygonZone(self.zone_in, (1600, 800))
            detections = sv.Detections.from_ultralytics(results)
            mask = zone.trigger(detections=detections)
            detections = detections[mask]
            # print(detections)

            labels = [
                f"{results.names[class_id]} {confidence * 100:0.2f}"
                for _, _, confidence, class_id, _
                in detections
            ]
            # print(labels)
            args = numpy.ndarray([])
            if detections.class_id.size > 0:
                args = detections.class_id
            elif detections.class_id.size == 0:
                args = numpy.ndarray([0])

            if args.size != 0:
                a = threading.Thread(target=self.arduino(args))
                a.start()

            frame = box_annotator.annotate(
                scene=frames,
                detections=detections,
                labels=labels
            )
            self.interface(frame, args, fps)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def interface(self, frame, args, fps):
        sv.draw_polygon(frame, self.zone_in, self.color)
        if self.Decision(args, 0.6) == 0:
            msg = "Please Wear Helmet!!!"
        elif self.Decision(args, 0.6) == 1:
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

    def arduino(self, class_id, threshold=0.6):
        decision = self.Decision(class_id=class_id, threshold=threshold)
        while True:
            if decision == 1:
                self.port.write(b'1')
                break
            elif decision == 0:
                self.port.write(b'0')
                break

    @classmethod
    def Decision(cls, class_id, threshold):
        decision = numpy.average(class_id)
        if decision >= threshold:
            decision = 1
        else:
            decision = 0
        return decision
