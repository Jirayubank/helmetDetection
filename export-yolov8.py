from ultralytics import YOLO

model = YOLO('yolov8s-5.10ver1.pt')

model.export(task='detect', format='onnx', imgsz=416)
