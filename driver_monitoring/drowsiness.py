import cv2
import mediapipe as mp
from scipy.spatial import distance

# ==================================
# Drowsiness Parameters
# ==================================

EAR_THRESHOLD = 0.27
DROWSY_FRAME_LIMIT = 5

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

closed_frames = 0

# ==================================
# MediaPipe Face Mesh
# ==================================

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ==================================
# EAR Calculation
# ==================================

def calculate_ear(eye_points):

    vertical_1 = distance.euclidean(
        eye_points[1],
        eye_points[5]
    )

    vertical_2 = distance.euclidean(
        eye_points[2],
        eye_points[4]
    )

    horizontal = distance.euclidean(
        eye_points[0],
        eye_points[3]
    )

    if horizontal == 0:
        return 0.30

    return (
        vertical_1 + vertical_2
    ) / (2.0 * horizontal)

# ==================================
# Eye Coordinates
# ==================================

def get_eye_coordinates(
    landmarks,
    eye_indices,
    width,
    height
):

    points = []

    for idx in eye_indices:

        x = int(
            landmarks[idx].x * width
        )

        y = int(
            landmarks[idx].y * height
        )

        points.append((x, y))

    return points

# ==================================
# Main Detection Function
# ==================================

def detect_drowsiness(frame):

    global closed_frames

    result = {
        "status": "Awake",
        "ear": 0.0,
        "closed_frames": closed_frames
    }

    try:

        if frame is None:
            return result

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(
            rgb_frame
        )

        # No face detected
        if not results.multi_face_landmarks:

            closed_frames = 0

            return {
                "status": "Awake",
                "ear": 0.0,
                "closed_frames": closed_frames
            }

        face_landmarks = (
            results.multi_face_landmarks[0]
        )

        h, w, _ = frame.shape

        landmarks = (
            face_landmarks.landmark
        )

        left_eye = get_eye_coordinates(
            landmarks,
            LEFT_EYE,
            w,
            h
        )

        right_eye = get_eye_coordinates(
            landmarks,
            RIGHT_EYE,
            w,
            h
        )

        left_ear = calculate_ear(
            left_eye
        )

        right_ear = calculate_ear(
            right_eye
        )

        ear = (
            left_ear +
            right_ear
        ) / 2.0

        # DEBUG
        print(
            f"EAR: {round(ear,3)} | Closed Frames: {closed_frames}"
        )

        if ear < EAR_THRESHOLD:

            closed_frames += 1

        else:

            closed_frames = 0

        if closed_frames >= DROWSY_FRAME_LIMIT:

            status = "Drowsy"

        else:

            status = "Awake"

        result = {
            "status": status,
            "ear": round(
                ear,
                3
            ),
            "closed_frames": closed_frames
        }

        return result

    except Exception as e:

        print(
            f"Drowsiness Detection Error: {e}"
        )

        return result

# ==================================
# Standalone Test
# ==================================

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    print(
        "Starting Drowsiness Detection..."
    )

    while True:

        success, frame = cap.read()

        if not success:
            break

        output = detect_drowsiness(
            frame
        )

        print(output)

        cv2.imshow(
            "Drowsiness Detection",
            frame
        )

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()

    cv2.destroyAllWindows()