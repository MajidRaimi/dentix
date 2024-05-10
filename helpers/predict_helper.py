from ultralytics import YOLO
import os
import cv2

class PredictHelper:

    def __init__(self, model_path):
        self.model_path = model_path
        self.model = YOLO(model_path)

    def predict(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f'{image_path} not found')
        result = self.model.predict(image_path)
        for single_result in result:
            detected_boxes = single_result.boxes
            confidence_scores = [score.item() for score in detected_boxes.conf]
            class_values = detected_boxes.cls
            bounding_boxes = detected_boxes.xyxy
            class_names = single_result.names
            predicted_class_names = [class_names[int(cls)] for cls in class_values]
            results = list(zip(predicted_class_names, confidence_scores, bounding_boxes))
            # results = self.filter_results(results)
            return results

    def filter_results(self, results):
        best_results = {}
        for class_name, confidence, box in results:
            if class_name not in best_results or confidence > best_results[class_name][0]:
                best_results[class_name] = (confidence, box)
        filtered_results = [(class_name, *values) for class_name, values in best_results.items()]
        return filtered_results

    def draw_prediction(self, image_path, predictions):
        image = cv2.imread(image_path)
        for class_name, confidence, box in predictions:
            start_point = (int(box[0]), int(box[1]))
            end_point = (int(box[2]), int(box[3]))
            color = (162, 58, 70)
            thickness = 2
            image = cv2.rectangle(image, start_point, end_point, color, thickness)
            label = f"{class_name}: %{(confidence*100):.2f}"
            text_position = (start_point[0], start_point[1] - 10)
            image = cv2.putText(image, label, text_position, cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 2)
        labeled_path = image_path.replace('uploads', 'downloads')
        cv2.imwrite(labeled_path, image)
        return labeled_path