# Suspicious Activity Simulator

A real-time surveillance system designed to **detect violent or suspicious human behavior** using deep learning and computer vision. This simulator helps automate threat detection from live or recorded video streams and instantly notifies security personnel via Telegram alerts.

---

## Project Overview

The **Suspicious Activity Simulator** combines AI-powered violence detection, human detection, and alert mechanisms into a unified desktop application. Built in Python using TensorFlow, OpenCV, and CustomTkinter, it allows security teams to monitor live camera feeds and receive real-time alerts for suspicious activities.

---

## Features

* ✅ Real-time violence detection using a custom-trained CNN.
* ✅ Human detection using SSD MobileNet V2 COCO.
* ✅ GUI-based surveillance dashboard using CustomTkinter.
* ✅ Live webcam and recorded video analysis support.
* ✅ Telegram alert integration for immediate incident notifications.
* ✅ User login/signup system with secure bcrypt-based password hashing.

---

## System Requirements

### Hardware

* **CPU**: Intel Core i5/i7 (Quad-core or better)
* **RAM**: Minimum 8 GB
* **Storage**: 256 GB SSD
* **Camera**: HD Webcam or CCTV (720p+)
* **GPU** *(Optional)*: NVIDIA GTX 1650 or higher for faster inference

### Software

* **OS**: Windows 10/11
* **Language**: Python 3.x
* **IDE**: VS Code / PyCharm

### Libraries & Tools

* `opencv-python`
* `tensorflow`, `keras`
* `numpy`, `pandas`, `matplotlib`
* `customtkinter`
* `sqlite3`
* `bcrypt`
* `requests` (for Telegram API)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Models Used

> **Note:** Due to file size and repository limitations, not all model files are included here. Contact the author to access trained models or retraining instructions.

| Model File                         | Description                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| `modelnew.h5`                      | Custom CNN model trained on 700 videos (350 violent, 350 non-violent)                |
| `ssd_mobilenet_v2_coco_2018_03_29` | Pre-trained object detection model for human recognition (from TensorFlow Model Zoo) |
| *(Optional)* YOLOv2                | Evaluated for performance in object detection scenarios                              |

---

##  How It Works

1. **User Authentication:** Secure login using bcrypt-hashed credentials.
2. **Live Feed:** Captures webcam/CCTV video frames.
3. **Detection:**

   * Humans detected using SSD MobileNet V2
   * Suspicious activity classified using `modelnew.h5`
4. **Alerts:** Instant Telegram message with activity info and timestamp.
5. **Logs:** Suspicious events stored in database with time, type, and screenshot.

---

## Limitations & Future Enhancements

### Current Limitations

* Limited multi-camera support
* Only visual activity detection (no sound analysis)
* Model files not included due to storage constraints

### Planned Enhancements

* Cloud-based video and alert logging
* Mobile app integration for remote monitoring
* Facial recognition for suspect identification
* Audio event detection (e.g., screams, gunshots)

---

## Contact

For model access or queries:
**Dishant Uprety**
Email: `dishantuprety@gmail.com`

---

## License

This project is licensed under the [MIT License](LICENSE).

