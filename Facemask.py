import cv2
import numpy as np


class EyeGlassesApp:

    def __init__(self, glasses_path="download (1).png"):
        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        # Load Face and Eye Haar Cascades
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

        if self.face_cascade.empty() or self.eye_cascade.empty():
            raise IOError("Unable to load one or more cascade classifier XML files.")

        # Load glasses image WITH alpha channel (must be a PNG with transparency)
        self.glasses_img = cv2.imread(glasses_path, cv2.IMREAD_UNCHANGED)
        if self.glasses_img is None:
            raise IOError(f"Could not load glasses image at '{glasses_path}'")
        if self.glasses_img.shape[2] != 4:
            raise ValueError(
                "Glasses image must have an alpha channel (RGBA PNG with a transparent background)."
            )

    @staticmethod
    def overlay_transparent(background, overlay, x, y):
        """Alpha-blend a BGRA `overlay` onto `background` at top-left corner (x, y).
        Handles overlays that are partially or fully off-frame."""
        bg_h, bg_w = background.shape[:2]
        ov_h, ov_w = overlay.shape[:2]

        # Clip the overlay region so it fits inside the frame
        x1, y1 = max(x, 0), max(y, 0)
        x2, y2 = min(x + ov_w, bg_w), min(y + ov_h, bg_h)

        if x1 >= x2 or y1 >= y2:
            return background  # Fully off-screen, nothing to draw

        # Corresponding region inside the overlay image itself
        ov_x1, ov_y1 = x1 - x, y1 - y
        ov_x2, ov_y2 = ov_x1 + (x2 - x1), ov_y1 + (y2 - y1)

        overlay_crop = overlay[ov_y1:ov_y2, ov_x1:ov_x2]
        alpha = overlay_crop[:, :, 3:4].astype(float) / 255.0  # shape (h, w, 1)

        bg_region = background[y1:y2, x1:x2].astype(float)
        fg_region = overlay_crop[:, :, :3].astype(float)

        blended = fg_region * alpha + bg_region * (1 - alpha)
        background[y1:y2, x1:x2] = blended.astype(np.uint8)

        return background

    def place_glasses(self, frame, eyes_in_face, face_origin):
        """Given eye boxes (relative to the face ROI) and the face's (x, y) origin
        in the full frame, resize/position the glasses to span both eyes."""
        if len(eyes_in_face) < 2:
            return  # Need at least two eyes to anchor the glasses reliably

        # Keep the two largest detections — most likely the real eyes
        eyes_sorted = sorted(eyes_in_face, key=lambda e: e[2] * e[3], reverse=True)[:2]
        # Order them left-to-right
        eyes_sorted = sorted(eyes_sorted, key=lambda e: e[0])

        (ex1, ey1, ew1, eh1), (ex2, ey2, ew2, eh2) = eyes_sorted
        fx, fy = face_origin

        # Eye centers in full-frame coordinates
        c1 = (fx + ex1 + ew1 // 2, fy + ey1 + eh1 // 2)
        c2 = (fx + ex2 + ew2 // 2, fy + ey2 + eh2 // 2)

        eye_distance = int(np.hypot(c2[0] - c1[0], c2[1] - c1[1]))
        if eye_distance <= 0:
            return

        # Glasses should be noticeably wider than just the eye-to-eye distance
        glasses_width = int(eye_distance * 2.2)
        scale = glasses_width / self.glasses_img.shape[1]
        glasses_height = int(self.glasses_img.shape[0] * scale)
        if glasses_width <= 0 or glasses_height <= 0:
            return

        resized = cv2.resize(
            self.glasses_img, (glasses_width, glasses_height), interpolation=cv2.INTER_AREA
        )

        # Rotate to match the tilt of the head (angle between the two eyes)
        angle = np.degrees(np.arctan2(c2[1] - c1[1], c2[0] - c1[0]))
        center = (glasses_width // 2, glasses_height // 2)
        rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            resized, rot_mat, (glasses_width, glasses_height),
            flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)
        )

        # Midpoint between the eyes = roughly where the glasses bridge should sit
        mid_x = (c1[0] + c2[0]) // 2
        mid_y = (c1[1] + c2[1]) // 2

        top_left_x = mid_x - glasses_width // 2
        top_left_y = mid_y - glasses_height // 2

        self.overlay_transparent(frame, rotated, top_left_x, top_left_y)

    def run(self):
        print("Eye Glasses Overlay Started.")
        print("Press 'q' to Quit")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame from camera.")
                break

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
            )

            for x, y, w, h in faces:
                roi_gray = gray[y: y + h, x: x + w]

                eyes = self.eye_cascade.detectMultiScale(
                    roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(15, 15)
                )

                self.place_glasses(frame, eyes, (x, y))

            cv2.imshow("Glasses Overlay", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = EyeGlassesApp("glasses_rgba.png")
    app.run()
