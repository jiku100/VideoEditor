import cv2, sys, glob
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUi()

    def setUi(self):
        self.resize(1920, 1280)
        self.setWindowTitle("VideoEditor - Zeron")
        self.mainWidget = QWidget()

        self.mainVBox = QVBoxLayout()
        self.mainWidget.setLayout(self.mainVBox)

        self.video = QLabel()
        self.video.resize(1600, 900)
        self.video.setScaledContents(True)
        self.btn = QPushButton("selasd")
        self.btn.resize(self.sizeHint())

        self.mainVBox.addWidget(self.video)
        self.mainVBox.addWidget(self.btn)
        self.setCentralWidget(self.mainWidget)
        # Test code
        self.cap = cv2.VideoCapture("Test-video.mp4")

        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000. / self.cap.get(cv2.CAP_PROP_FPS))


    def nextFrameSlot(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.video.setPixmap(pix)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     speed = [0.5, 0.75, 1.0, 1.5, 2.0]
#     curr_speed = 2
#     cap = cv2.VideoCapture("Test-video.mp4")
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     print(width, height)
#     base_delay = int(1000/fps)
#     delay = base_delay
#     isStop = False
#     isSaved = False
#     is_right_frames = False
#
#     if glob.glob("./Capture/*.jpg"):
#         last_capture_num = int(sorted(glob.glob("./Capture/*.jpg"))[-1][17:-4])
#     else:
#         last_capture_num = 0
#
#     while True:
#         if not isStop:
#             ret, frame = cap.read()
#         else:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, stop_frame)
#             ret, frame = cap.read()
#         if ret:
#             cv2.imshow('video', frame)
#             op = cv2.waitKeyEx(delay)
#             if op == 27:         # 'ESC' To end video
#                 break
#             elif op == 0x250000:
#                 curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
#                 target_frame = curr_frame - 5 * fps if curr_frame - 5 * fps > 0 else 0
#                 if isStop:
#                     stop_frame = target_frame
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
#             elif op == 0x270000:
#                 curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
#                 target_frame = curr_frame + 5 * fps if curr_frame + 5 * fps < cap.get(
#                     cv2.CAP_PROP_FRAME_COUNT) else cap.get(
#                     cv2.CAP_PROP_FRAME_COUNT)
#                 if isStop:
#                     stop_frame = target_frame
#                 cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
#             elif op == 0x260000:
#                 curr_speed = getIndex(speed, curr_speed + 1)
#                 delay = int(base_delay/speed[curr_speed])
#             elif op == 0x280000:
#                 curr_speed = getIndex(speed, curr_speed - 1)
#                 delay = int(base_delay/speed[curr_speed])
#             elif op == 32:       # 'SpaceBar' To stop frame
#                 if isStop:
#                     isStop = False
#                 else:
#                     isStop = True
#                     stop_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
#             elif op == 115:      # 's' To saved video
#                 if not isSaved:
#                     start_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
#                     print(f"start_frame: {start_frame}")
#                     isSaved = True
#                 else:
#                     end_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
#                     print(f"end_frame: {end_frame}")
#                     print(f"Save video from {start_frame} Frame to {end_frame} Frame?(yes or no)")
#                     is_right_frames = input('>> ')
#                     if "yes" in is_right_frames:
#                         is_right_frames = True
#                         break
#                     else:
#                         print("Try again to set end frame position (Press S) or Reset all setting positions (Press R)")
#             elif op == 114:      # 'r' To reset the start_frame
#                 if isSaved:
#                     print("Reset setting frame positions!!")
#                     isSaved = False
#             elif op == 99:      # 'c' To capture the frame
#                 output_name = "./Capture/capture" + str(last_capture_num) + ".jpg"
#                 cv2.imwrite(output_name, frame)
#                 last_capture_num += 1
#
#         else:
#             print("Video end")
#             break
#     if is_right_frames:
#         saved_frame_count = end_frame - start_frame + 1
#         fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#         out = cv2.VideoWriter('output.avi', fourcc, fps, (width,height))
#         cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
#         while(cap.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame):
#             ret, frame = cap.read()
#             if ret:
#                 out.write(frame)
#                 print('\r{:.1%}'.format((cap.get(cv2.CAP_PROP_POS_FRAMES) - start_frame)/saved_frame_count), end="")
#                 sys.stdout.flush()
#         print("\nEnd Save")
#         out.release()
#
#     print("End the video, Thanks to use!!")
#     cap.release()
#     cv2.destroyAllWindows()