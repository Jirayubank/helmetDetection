import cv2
from ultralytics import YOLO
import supervision as sv
import serial
import numpy
import threading
import subprocess

port = serial.Serial('COM8', 9600)


def main():
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5
    )

    color = sv.ColorPalette.default()
    zone_in = numpy.array([[500, 50],
                           [500, 400],
                           [100, 400],
                           [100, 50]])
    # load model
    model = YOLO('../helmet-detect/yolov8s-ver3-0111.onnx', task='detect')   # onnx (run faster than yolo on cpu) ver2
    source = 'rtsp'    # TODO: connect with ip cam
    img_size = 416

    # vid = '../test/detect_demo.mp4'
    # img = '../test/BikesHelmets76.png'

    for results in model.predict(source=source,
                                 show=False,
                                 stream=True,
                                 imgsz=(img_size, img_size),
                                 agnostic_nms=True,
                                 conf=0.5):

        frames = results.orig_img
        zone = sv.PolygonZone(zone_in, (1600, 800))
        detections = sv.Detections.from_ultralytics(results)
        mask = zone.trigger(detections=detections)
        detections = detections[mask]

        labels = [
            f"{results.names[class_id]} {confidence * 100:0.2f}"
            for _, _, confidence, class_id, tracker_id
            in detections
        ]

        args = numpy.ndarray([])
        if detections.class_id.size > 0:
            args = detections.class_id
        elif detections.class_id.size == 0:
            args = numpy.ndarray([0])
        if args.size != 0:
            a = threading.Thread(target=arduino, args=args)
            a.start()

        frame = box_annotator.annotate(
            scene=frames,
            detections=detections,
            labels=labels
        )
        sv.draw_polygon(frame, zone_in, color.colors[1])
        cv2.imshow('Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def Decision(class_id: numpy.ndarray, threshold: float) -> int:
    decision = numpy.average(class_id)
    if decision >= threshold:
        decision = 1
    else:
        decision = 0
    return decision


def arduino(class_id: numpy.ndarray, threshold=0.6) -> None:
    # port = serial.Serial('COM4', 9600)
    decision = Decision(class_id=class_id, threshold=threshold)
    while True:
        if decision == 1:
            port.write(b'1')
            break
        elif decision == 0:
            port.write(b'0')
            break


if __name__ == "__main__":
    m = threading.Thread(target=main)
    m.start()
