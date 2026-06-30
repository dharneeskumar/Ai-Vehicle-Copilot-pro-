import cv2
from ultralytics import YOLO

MODEL_PATH = "yolov8n.pt"

PERSON_CLASS_ID = 0
PHONE_CLASS_ID = 67

CONFIDENCE_THRESHOLD = 0.40

try:
    model = YOLO(MODEL_PATH)
    print("YOLO Model Loaded Successfully")
except Exception as e:
    print(f"Model Load Error: {e}")
    model = None


def detect_distraction(frame):

    result = {
        "status": "Focused",
        "phone_detected": False,
        "confidence": 0.0
    }

    try:
        if model is None:
            return result

        # ❌ DO NOT flip here (handled in app.py or drowsiness module)
        # frame = cv2.flip(frame, 1)

        detections = model(
            frame,
            imgsz=416,
            verbose=False
        )

        person_detected = False
        phone_detected = False
        max_phone_confidence = 0.0

        for detection in detections:

            for box in detection.boxes:

                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                if class_id == PERSON_CLASS_ID:
                    person_detected = True

                elif class_id == PHONE_CLASS_ID:
                    phone_detected = True

                    if confidence > max_phone_confidence:
                        max_phone_confidence = confidence

        # Decision logic
        if person_detected and phone_detected:
            status = "Distracted"
        else:
            status = "Focused"

        return {
            "status": status,
            "phone_detected": phone_detected,
            "confidence": round(max_phone_confidence, 3)
        }

    except Exception as e:
        print(f"Distraction Detection Error: {e}")
        return result


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    try:
        while True:

            success, frame = cap.read()

            if not success:
                break

            output = detect_distraction(frame)

            print(output)

            cv2.imshow("Distraction Detection", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()