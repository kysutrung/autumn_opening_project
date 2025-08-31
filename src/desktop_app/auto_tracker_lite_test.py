#khai báo thư viện

import cv2
import serial
import time
import math
from ultralytics import YOLO

#khai báo biến toàn cục

PORT = "COM8"      #mở Device Manager lên xem máy tính nhận bo esp đang ở COM bao nhiêu điền vào đây
BAUD = 9600
CAM_ID = 1 
WIDTH, HEIGHT = 640, 480

SERVO1_INIT = 90   #trái-phải
SERVO2_INIT = 90   #lên-xuống
SERVO_MIN, SERVO_MAX = 0, 180

DEAD_ZONE = 100     #tính theo đơn vị px, đại diện cho vùng chết xung quanh tâm
Kp_x = 0.12        #hệ số P cho trục X, chuyển đổi từ px sang độ
Kp_y = 0.12        #hệ số P cho trục Y
MAX_STEP = 4       #giới hạn bước thay đổi góc mỗi lần gửi
SMOOTH_ALPHA = 0.35  #càng lớn càng bám nhanh, chạy từ 0 đến 1
CONF_THRES = 0.35 
DEVICE = "cuda"

#tần suất gửi lệnh sang ESP
SERIAL_HZ = 30

#khai báo các hàm

def clamp(v, lo, hi):
    return max(lo, min(hi, v))


class ServoController:
    def __init__(self, port, baud):
        self.ser = None
        try:
            self.ser = serial.Serial(port, baud, timeout=0)
            time.sleep(1.5)
            print(f"Kết nối {port} @ {baud}")
        except Exception as e:
            print(f"Không mở được cổng {port}: {e}")

        self.servo1 = SERVO1_INIT
        self.servo2 = SERVO2_INIT
        self._last_send = 0.0
        self._min_interval = 1.0 / SERIAL_HZ if SERIAL_HZ > 0 else 0.0

    def send(self, idx, angle):
        if self.ser is None:
            return
        now = time.time()
        if now - self._last_send < self._min_interval:
            return
        try:
            cmd = f"{idx}:{int(angle)}\n"
            self.ser.write(cmd.encode())
            self._last_send = now
        except Exception as e:
            print("[Lỗi Serial 3]", e)

    def center(self):
        self.servo1 = SERVO1_INIT
        self.servo2 = SERVO2_INIT
        self.send(1, self.servo1)
        self.send(2, self.servo2)

#main

def main():
    print("Đang Chạy Chương Trình!!!")

    model = YOLO("yolov8n.pt")

    cap = cv2.VideoCapture(CAM_ID)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    if not cap.isOpened():
        print("[Lỗi Camera 1]")
        return

    cx0, cy0 = WIDTH // 2, HEIGHT // 2 

    target_cx, target_cy = cx0, cy0
    have_target = False

    sc = ServoController(PORT, BAUD)
    sc.center()

    while True:
        ok, frame = cap.read()
        if not ok:
            print("[Lỗi Camera 2]")
            break

        results = model.predict(
            frame,
            conf=CONF_THRES,
            device=DEVICE,
            classes=[0],  
            verbose=False
        )

        boxes = results[0].boxes if results and results[0] is not None else []
        if boxes is not None and len(boxes) > 0:

            best = max(
                boxes,
                key=lambda b: float((b.xyxy[0][2]-b.xyxy[0][0]) * (b.xyxy[0][3]-b.xyxy[0][1]))
            )
            x1, y1, x2, y2 = map(int, best.xyxy[0].tolist())
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if not have_target:
                target_cx, target_cy = cx, cy
                have_target = True
            else:
                target_cx = int(SMOOTH_ALPHA * cx + (1 - SMOOTH_ALPHA) * target_cx)
                target_cy = int(SMOOTH_ALPHA * cy + (1 - SMOOTH_ALPHA) * target_cy)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (target_cx, target_cy), 4, (0, 0, 255), -1)
        else:
            have_target = False

        if have_target:
            err_x = target_cx - cx0  
            err_y = target_cy - cy0   

            adj_x = 0 if abs(err_x) < DEAD_ZONE else err_x
            adj_y = 0 if abs(err_y) < DEAD_ZONE else err_y

            delta_pan  = -Kp_x * adj_x  
            delta_tilt = -Kp_y * adj_y

            delta_pan  = clamp(delta_pan, -MAX_STEP, MAX_STEP)
            delta_tilt = clamp(delta_tilt, -MAX_STEP, MAX_STEP)

            sc.servo1 = clamp(sc.servo1 + delta_pan,  SERVO_MIN, SERVO_MAX)
            sc.servo2 = clamp(sc.servo2 + delta_tilt, SERVO_MIN, SERVO_MAX)

            sc.send(1, round(sc.servo1))
            sc.send(2, round(sc.servo2))

        cv2.circle(frame, (cx0, cy0), 5, (255, 0, 0), -1)
        cv2.putText(frame, f"Truc X:{int(sc.servo1)}  Truc Y:{int(sc.servo2)}",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(frame, f"Dead Zone:{DEAD_ZONE}px  Kp({Kp_x:.2f},{Kp_y:.2f})",
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.imshow("Camera Theo Doi Thong Minh", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('t'):
            break
        if key == ord('g'):
            sc.center()

    cap.release()
    cv2.destroyAllWindows()
    print("Thoát Chương Trình!!!!")
    

if __name__ == "__main__":
    main()
