from ultralytics import YOLO
import torchvision  

class Model:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame, conf_threshold=0.5, iou_threshold=0.4):
        # Realizar a detecção usando o modelo YOLO
        results = self.model.predict(frame)
        
        # Filtrar resultados com base no limiar de confiança
        filtered_results = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                # Aplicar Non-Maximum Suppression (NMS) para evitar detecções duplicadas
                keep = torchvision.ops.nms(boxes.xyxy, boxes.conf, iou_threshold)
                filtered_boxes = [boxes[i] for i in keep if boxes[i].conf.item() > conf_threshold]
                if filtered_boxes:
                    result.boxes = filtered_boxes
                    filtered_results.append(result)
        return filtered_results
    
    def predict(self, image_path):
        results = self.model.predict(image_path, save=False, imgsz=640, conf=0.7)
        # Processar lista de resultados
        if results:
            for result in results:
                result.save(filename='result.jpg')  # salvar no disco
