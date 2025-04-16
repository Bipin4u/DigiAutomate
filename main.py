from utils.video_recorder import record_video
from utils.log_capture import record_log
from utils.motion_detector import VideoCheck
from utils.remote_control import channelOperation
from utils.stream_file_modifier import modifyStreamFile
from utils.atsc_automation import automateATSC
from config import STREAM_LIST, LOG_DIR, VIDEO_DIR, OUTPUT_DIR

import os, time, threading, cv2

# Make directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

recording_flag = threading.Event()
log_flag = threading.Event()

MotionDetectorFlag = [0]
Motionloopcount = [0]
MotionCount = [0]
bugreportControlFlag = [0]

looprun = int(input('Enter how many loops to run: '))

os.system('adb devices')
os.system('adb shell am broadcast -a com.sony.dtv.tvinput.atsc3tuner.intent.CHANGE_ANDROID_TREE --ei android_tree_request_code 0')

for i, stream in enumerate(STREAM_LIST):
    for j in range(looprun):
        print(f'Loop: {i}_{j}')
        bugreportControlFlag[0] = 0

        recording_flag.set()
        log_flag.set()

        video_thread = threading.Thread(target=record_video, args=(i, j, Motionloopcount, MotionDetectorFlag, MotionCount, recording_flag))
        log_thread = threading.Thread(target=record_log, args=(i, j, log_flag))
        
        video_thread.start()
        log_thread.start()

        with open("data/keyevent.txt", "r") as file1:
            for line in file1:
                for word in line.strip():
                    channelOperation(word)
                    if word == 'D':
                        result = VideoCheck(MotionDetectorFlag, Motionloopcount, MotionCount)
                        if result == 'black picture':
                            log_flag.clear()
                            log_thread.join()
                            bugreportControlFlag[0] = 1
                            os.system('C:platform-toolsget_bugreport.bat')
        recording_flag.clear()
        video_thread.join()
        if not bugreportControlFlag[0]:
            log_flag.clear()
            log_thread.join()

    modifyStreamFile(i, STREAM_LIST)
    automateATSC()
