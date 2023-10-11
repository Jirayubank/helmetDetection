import cv2
from ultralytics import YOLO
import supervision as sv
import serial
import numpy


def main():
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5
    )

    # load model
    # model = YOLO("yolov8s-5.10ver1.pt")   # yolo
    model = YOLO('yolov8s-ver1.onnx', task='detect')   # onnx (run faster than yolo on cpu)
    img_size = 416

    for result in model.predict(source=0, show=False, stream=True, imgsz=(img_size, img_size), agnostic_nms=True,
                                conf=0.5):

        frame = result.orig_img
        detections = sv.Detections.from_ultralytics(result)

        labels = [
            f"{result.names[class_id]} {confidence * 100:0.2f}"
            for _, _, confidence, class_id, tracker_id
            in detections
        ]

        # control Arduino
        if detections.class_id.size > 0:
            arduino(detections.class_id)

        frame = box_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels
        )

        cv2.imshow("Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def Decision(class_id: list, threshold: float) -> int:
    decision = numpy.average(class_id)
    if decision >= threshold:
        decision = 1
    else:
        decision = 0
    return decision


def arduino(class_id: list, threshold=0.6) -> None:
    port = serial.Serial('COM3', 9600)
    decision = Decision(class_id=class_id, threshold=threshold)
    while True:
        if decision == 1:
            if port.write(b'1'):
                print("LED off")
                break
        elif decision == 0:
            if port.write(b'0'):
                print("LED on")
                break


if __name__ == "__main__":
    main()
