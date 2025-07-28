![Photo01](https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/repo_cover.jpg)

# YOLO Watchdog

[Click here for English](https://github.com/kysutrung/yolo_watchdog/blob/main/ENG_README.md)

Hệ Thống Trợ Lý Giám Sát An Toàn Ứng Dụng Công Nghệ Học Máy 

Keyword: yolov8, esp now, python app, hardware design.

## 📑 Mô Tả Dự Án

Xây dựng một hệ thống máy quay giám sát dựa trên thuật toán học máy YOLO (You Only Look Once). Cho phép xác định ra các tình huống nguy hiểm dựa trên việc xác định được các vật thể bị cấm trong từng khu vực riêng biệt. Tăng độ an toàn cho các khu vực bằng việc đảm bảo các tình huống vi phạm an toàn khả năng phát hiện ra các tình huống không đảm bảo an toàn như việc thiếu đồ bảo hộ, không có người vận hành ở các vị trí quan trọng. Sau khi phát hiện được những tình huống, hệ thống sẽ kích hoạt cơ chế thông áo gửi tới người làm công tác giám sát từ xa thông qua sóng không dây ESP-NOW. Hỗ trợ những giám sát viên làm việc hiệu quả và nhanh chóng hơn.

## ❓ YOLO Là Gì Và Tại Sao Sử Dụng YOLO
__YOLO__ (You Only Look Once) là một mô hình mạng CNN cho việc phát hiện, nhận dạng, phân loại đối tượng. Yolo được tạo ra từ việc kết hợp giữa các convolutional layers và connected layers.Trong đóp các convolutional layers sẽ trích xuất ra các feature của ảnh, còn full-connected layers sẽ dự đoán ra xác suất đó và tọa độ của đối tượng.

Thuật toán này phù hợp cho việc phân tích và phát hiện ra nhiều đối tượng trong một khung hình cùng lúc với tốc độ theo giờ gian thực.

<br>

<p align="center"><strong>Sơ Đồ Thuật Toán Của Khổi Xử Lý Hình Ảnh</strong></p>

![Photo01](https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/image_processor_diagram.png)

## ❓ Sơ Lược Về Giao Thức ESP-NOW
__ESP-NOW__  là một giao thức được phát triển bới Espressif, cho phép nhiều thiết bị giao tiếp với nhau mà không cần dùng Wifi. Giao thức tương tự như kết nối không dây 2.4GHz công suất thấp. ESP-NOW cho phép gửi gói tin tối đa 250kb nên hoàn toàn phù hợp cho việc gửi một thông điệp với nội dung cảnh báo giữa các thiết bị trong hệ thống giám sát an toàn.

<br>

<p align="center"><strong>Remote Monitor Unit Algorithm Diagram</strong></p>

![Photo02](https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/remote_monitor_diagram.png)

## 💻 Danh Sách Các Chức Năng Của Hệ Thống

__Bộ Phận Phân Tích Hình Ảnh__
- [x] Phát hiện vật thể với mô hình học máy tự huấn luyện
- [x] 

__Bộ Phận Cảnh Báo Từ Xa__
- [x] Receive notification via ESP NOW
- [x] Alert depend on setting
- [ ] Good looking UI using SquareLine Studio
- [ ] Notification history
- [ ] Expansion port
- [ ] Connection lost notification 

__Bộ Phận Theo Dõi Tự Động__
- [x] Auto move camera facing to object

__Ứng Dụng Điều Khiển Window__
- [x] Whole system work right in Windows OS
- [x] Control UI
- [x] Display realtime video
- [x] Select prohibited objects in each area
- [ ] Running with every PC



## 📥 Installation Guide
### 1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirement libraries. Check if pip is installed, install if not.

```bash
pip --version
```

__For YOLOv5__

```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
```

__For YOLOv8__

```bash
git clone https://github.com/ultralytics/ultralytics
cd ultralytics
pip install -r requirements.txt
```

__For YOLO training and Python programming__

OpenCV for work with image data from camera. Pyserial for send data via USB port.

```bash
pip install opencv-python
pip install pyserial
```
Check if Pytorch is installed. Find the installation command suitable for your machine on [the official Pytorch website](https://pytorch.org/get-started/locally/) if your machine does not have it installed.

```bash
import torch
print(torch.__version__)   # Kiểm tra phiên bản
print(torch.cuda.is_available())   # Kiểm tra CUDA có khả dụng không
```

__For Raspberry Pi__

[How to install YOLOv8 requirement on Raspberry Pi](https://youtu.be/XzhTq-nk8GQ?si=78NhyxwTwYLjlhmm)

[How to run a program on startup for Raspberry Pi](https://youtu.be/Gl9HS7-H0mI?si=B7nPfKp_ZTQQLSHU) (make sure your Raspberry Pi is set up to run without a display.)

### 2. Train your own YOLO.

We've found some quick and effective video tutorials for you:

[How to train YOLOv8 with custom dataset using your local PC](https://youtu.be/gRAyOPjQ9_s?si=JTgtRKwl3u6fy0oe)

[How to capture and label training data to improve object detection model accuracy using labelImg tool](https://youtu.be/v0ssiOY6cfg?si=RaRrdKB-cuZYgdFo)

[How to fix labelImg crashing while selecting create rect box](https://youtu.be/5jHPuwo8z1o?si=pQSAGxQLbj22FRrF)

### 3. Device Setup

This is how these code work in our system design, you can do the way you want.

__All variable names, comments in code and UI are now in Vietnamese. English language is being edited and will be updated soon.__

<br>

<p align="center"><strong>System Design Diagram</strong></p>

![Photo01](https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/system_design_diagram.png)

__Camera Unit__

"Capture and process image" part - copy [image_processor code](https://github.com/kysutrung/yolo_watchdog/tree/main/image_processor) to sd card of Raspberry Pi, make sure it is in the same folder as the YOLO weight file.

"Notification sender" part - load ESP32 dev board with [alert_sender code](https://github.com/kysutrung/yolo_watchdog/tree/main/alert_sender), find MAC address of ESP32 with [find MAC code](https://github.com/kysutrung/yolo_watchdog/tree/main/alert_sender/find_mac_tool)

__Remote Monitor Unit__

ESP32 Custom Remote Monitor device - load with [custom_remote_monitor code](https://github.com/kysutrung/yolo_watchdog/tree/main/alert_receiver/custom_remote_monitor)

or

M5StickCplus2 IOT device - load with [m5stick_receiver code](https://github.com/kysutrung/yolo_watchdog/tree/main/alert_receiver/m5_stick_device/m5stick_receiver)


## 🛠️ Prototype 001

<p align="center">
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/camUnit.jpg" alt="Mô tả 1" width="400"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/rmUnit.jpg" alt="Mô tả 2" width="400"/>
</p>

These are how the hardware look when we are done. This prototype cost 80 USD in 2024.

__📖 Testing__

YOLO weight test:

<p align="center">
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/anh_test03.jpg" alt="Mô tả 1" width="400"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/anh_test04.jpg" alt="Mô tả 2" width="400"/>
</p>

System operation test:

<p align="center">
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/anh_test01.jpg" alt="Mô tả 1" width="400"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/anh_test02.jpg" alt="Mô tả 2" width="400"/>
</p>

System operation test with M5StickC Plus2:

<p align="center">
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/m5_ui_05.png" alt="Mô tả 1" width="400"/>
</p>

<p align="center">
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/m5_ui_01.png" alt="Mô tả 1" width="200"/>
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/m5_ui_02.png" alt="Mô tả 2" width="200"/>
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/m5_ui_03.png" alt="Mô tả 3" width="200"/>
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/m5_ui_04.png" alt="Mô tả 4" width="200"/>
</p>

M5StickC Plus2 firmware with Vietnamese language is available on M5 Burner App:

<br>

<p align="center">
  <img src="https://github.com/kysutrung/yolo_watchdog/blob/main/mediaa/m5buner.png" alt="Mô tả 1" width="400"/>
</p>







## 👏 References

[Ultralytics](https://github.com/ultralytics/ultralytics) - YOLO

[TheCodingBug](https://www.youtube.com/@TheCodingBug) - YOLO

[Edje Electronics](https://www.youtube.com/@EdjeElectronics) -YOLO

[Freedomwebtech](https://github.com/freedomwebtech) - Raspberry Pi

[Sam Westby](https://www.youtube.com/@SamWestbyTech) - Raspberry Pi

[Big-Bratan](https://github.com/Big-Bratan) - M5stick UI

## 📞 Support
If you have any questions or suggestions, feel free!!!
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
