import time
import cv2
import threading
import datetime
import subprocess
import os
import Remote_keys as rc
import xml.etree.ElementTree as ET
from pywinauto.application import Application

# Define the font to be used in the video frame
font = cv2.FONT_HERSHEY_SIMPLEX

def record_video(i, j, Motionloopcount, MotionDetectorFlag, MotionCount):
    # Initialize the background to None (for motion detection)
    static_back = None
    # Start capturing video from the default camera (change if using multiple cameras)
    cap = cv2.VideoCapture(0)
    # Define the codec and create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  
    out = cv2.VideoWriter(
        "C:\Users\bipin.kumar\OneDrive - HCL Technologies Ltd\Desktop\StabilityReport\video\"
        + "video" + str(i) + "_" + str(j) + '_' + "_".join(str(datetime.datetime.now())[:-7].split(" ")).replace(":", "-") + ".avi",
        fourcc, 20.0, (640, 480)
    )
    
    while recording_flag.is_set():  # Loop runs while recording_flag is True
        ret, frame = cap.read()  # Read frame from the camera
        cv2.imshow('frame', frame)  # Display the current frame
        # Write the frame to the video file with a timestamp
        out.write(cv2.putText(frame, str(datetime.datetime.now())[:-7], (25, 25), font, 1, (0, 255, 255), 2, cv2.LINE_4))
        time.sleep(.1)  # Small delay between frames
        if MotionDetectorFlag[0] == 1:  # Check if motion detection is enabled
            Motionloopcount[0] += 1  # Increment the motion loop count
            motion = 0  # Initialize motion to 0 (no motion)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
            gray = cv2.GaussianBlur(gray, (21, 21), 0)  # Apply GaussianBlur to reduce noise
            if static_back is None:  # If static_back is None, set it to the current frame
                static_back = gray 
                continue
            # Compute the absolute difference between the current frame and the background
            diff_frame = cv2.absdiff(static_back, gray)
            # Apply threshold to the difference frame to highlight the motion
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)  # Dilate to fill in holes
            # Find contours in the thresholded frame
            cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in cnts:
                if cv2.contourArea(contour) < 10000:  # Ignore small contours
                    continue
                motion = 1  # Motion detected
            if motion == 1:
                MotionCount[0] += 1  # Increment motion count if motion detected
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Stop recording if 'q' is pressed
            break
    
    # Release video capture and writer objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()  # Close the video window

def record_log(i, j):
    # Clear the logcat buffer
    os.system('adb logcat -c')
    process = subprocess.Popen(["adb", "logcat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    file = "C:\Users\bipin.kumar\OneDrive - HCL Technologies Ltd\Desktop\StabilityReport\logs\" + 'log_' + str(i) + '_' + str(j) + '.txt'
    with open(file, 'w') as fh:
        while log_flag.is_set():  # Loop runs while log_flag is True
            line = process.stdout.readline().decode('utf-8')  # Read line from adb logcat
            fh.write(line.strip() + '
')  # Write log line to file

# Function to check video for motion detection
def VideoCheck(MotionDetectorFlag, Motionloopcount, MotionCount):
    for i in range(4):  # Loop 4 times
        MotionDetectorFlag[0] = 1  # Enable motion detection
        Motionloopcount[0] = 0  # Reset motion loop count
        MotionCount[0] = 0  # Reset motion count
        time.sleep(7)  # Wait for 7 seconds
        MotionDetectorFlag[0] = 0  # Disable motion detection
        # Check if no motion was detected or if motion was detected for less than 20% of the time
        if MotionCount[0] == 0 or Motionloopcount[0] / MotionCount[0] < .2:
            print('black picture')
            if i == 3:
                return 'black picture'
        else:
            print('Ok video')
            return 'Ok video'

# Function to modify the XA3 file
def modifyStreamFile():
    root = ET.parse('C:Streamphoenix_35_060220_0948am.xa3')
    root.find('Atsc3/Subframe/Plp/Source/PcapFile').attrib['filename'] = "C:Stream\" + streamList[i]
    root.write("C:Streamdemo.XA3")

# Function to automate stream selection in the ATSC application
def automateATSC():
    app = Application(backend="uia").connect(path=r"C:Usersipin.kumarOneDrive - HCL Technologies LtdDesktopAtsc3XpressAtsc3Xpress.exe")
    main_dlg = app.window(title_re=".*Atsc3Xpress*")
    openfile = main_dlg.child_window(title="toolStrip1", auto_id="toolStrip1", control_type="ToolBar").child_window(title="Open", control_type="Button")
    openfile.click_input()  # Click the Open button
    time.sleep(3)
    try:
        # Handle the save prompt, if it appears
        smallwindow = main_dlg.child_window(title="Save", control_type="Window").child_window(title="No", auto_id="7", control_type="Button")
        smallwindow.click_input()
    except:
        pass
    app_file = Application().connect(title_re=".*Open")
    file_dlg = app_file.window(title_re=".*Open*")
    time.sleep(2)
    filev = file_dlg.child_window(title="&Open", class_name="Button")
    filev.click_input()  # Click the Open button
    time.sleep(2)

# Initial flags and variables
MotionDetectorFlag = [0]
Motionloopcount = [0]
MotionCount = [0]
os.system('adb devices')
os.system('adb shell am broadcast -a com.sony.dtv.tvinput.atsc3tuner.intent.CHANGE_ANDROID_TREE --ei android_tree_request_code 0')
recording_flag = threading.Event()
log_flag = threading.Event()
looprun = int(input('Enter how many loops to run: '))
streamList =  [
    'Dual_1PID_DRC_ML_200_100_H265_ATSC3_59fps94.pcap',
    'NAB0005_2019-06-07_A.pcap','phoenix_35_060220_0948am.pcap',
    'SD_20190321_191429_CEA-CC.r2.pcap',
    'P_DRM-OTA-G1P-SK-CENC8-S1_20200624_1702.pcap'
]
os.mkdir("C:\Users\bipin.kumar\OneDrive - HCL Technologies Ltd\Desktop\StabilityReport")
os.mkdir("C:\Users\bipin.kumar\OneDrive - HCL Technologies Ltd\Desktop\StabilityReport\logs")
os.mkdir("C:\Users\bipin.kumar\OneDrive - HCL Technologies Ltd\Desktop\StabilityReport\video")
bugreportControlFlag = [0]

for i in range(len(streamList)):  # Loop through the list of streams
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Stop if 'q' is pressed
        break
    time.sleep(2)
    for j in range(looprun):  # Loop for the specified number of times
        bugreportControlFlag[0] = 0  # Reset bug report control flag
        recording_flag.set()  # Set recording flag to True
        video_thread = threading.Thread(target=record_video, args=(i, j, Motionloopcount, MotionDetectorFlag, MotionCount,))
        video_thread.start()  # Start the video recording thread

        log_flag.set()  # Set log flag to True
        log_thread = threading.Thread(target=record_log, args=(i, j,))
        log_thread.start()  # Start the log recording thread

        print('loop: ' + str(i) + '_' + str(j))
        with open("keyevent.txt", "r+") as file1:
            for line in file1:
                for word in line:
                    print(word, end='')
                    rc.channelOperation(str(word))  # Perform channel operation based on the key
                    if word == 'D':  # If 'D' is pressed, check the video
                        video_Check_output = ''
                        video_Check_output = VideoCheck(MotionDetectorFlag, Motionloopcount, MotionCount)
                        if video_Check_output == 'black picture':  # If video is black, stop logging and generate bug report
                            log_flag.clear()
                            log_thread.join()
                            bugreportControlFlag[0] = 1
                            os.system('C:platform-toolsget_bugreport.bat')

        recording_flag.clear()
        video_thread.join()  # Stop the video recording thread
        if bugreportControlFlag == 0:
            log_flag.clear()
            log_thread.join()  # Stop the log recording thread
        else:
            pass

    modifyStreamFile()  # Modify the stream file
    automateATSC()  # Automate the ATSC stream selection

    demo = 'HssHsssuuursrsrsrsrsrsressedsesesesdsesssemmmIsse'
    # for i in demo:
    #     rc.channelOperation(i)


import os
import time

# Function to perform channel operations based on the key input
def channelOperation(key):
    match key:
        case "+":  # Channel Plus
            os.system('adb shell input keyevent 166')
        case "-":  # Channel Minus
            os.system('adb shell input keyevent 167')
        case "0":  # Zero
            os.system('adb shell input keyevent 7')
        case "1":  # One
            os.system('adb shell input keyevent 8')
        case "2":  # Two
            os.system('adb shell input keyevent 9')
        case "3":  # Three
            os.system('adb shell input keyevent 10')
        case "4":  # Four
            os.system('adb shell input keyevent 11')
        case "5":  # Five
            os.system('adb shell input keyevent 12')
        case "6":  # Six
            os.system('adb shell input keyevent 13')
        case "7":  # Seven
            os.system('adb shell input keyevent 14')
        case "8":  # Eight
            os.system('adb shell input keyevent 15')
        case "9":  # Nine
            os.system('adb shell input keyevent 16')
        case ".":  # Dot
            os.system('adb shell input keyevent 56')
        case "u":  # Up
            os.system('adb shell input keyevent 19')
        case "l":  # Left
            os.system('adb shell input keyevent 21')
        case "r":  # Right
            os.system('adb shell input keyevent 22')
        case "d":  # Down
            os.system('adb shell input keyevent 20')
        case "H":  # Home
            os.system('adb shell input keyevent 3')
        case "e":  # Enter
            os.system('adb shell input keyevent 23')
        case "T":  # TV
            os.system('adb shell input keyevent 170')
        case "P":  # Power
            os.system('adb shell input keyevent 26')
        case "N":  # Netflix
            os.system('adb shell input keyevent 191')
        case "i":  # Input
            os.system('adb shell input keyevent 165')
        case "j":  # Input
            os.system('adb shell input keyevent 229')
        case "I":  # Input
            os.system('adb shell input keyevent 178')
        case "g":  # Input
            os.system('adb shell input keyevent 172')
        case "R":  # Red
            os.system('adb shell input keyevent 183')
        case "G":  # Green
            os.system('adb shell input keyevent 184')
        case "Y":  # Yellow
            os.system('adb shell input keyevent 185')
        case "B":  # Blue
            os.system('adb shell input keyevent 186')
        case "b":  # Back
            os.system('adb shell input keyevent 4')
        case "S":  # CC
            os.system('adb shell input keyevent 175')
        case "H":  # Help
            os.system('adb shell input keyevent 259')
        case "Y":  # YouTube (Play/Pause)
            os.system('adb shell input keyevent 85')
        case "s":  # Second delay
            time.sleep(1)
        case "m":  # Minute delay
            time.sleep(60)
        case "q":  # Quarter-minute delay
            time.sleep(15)
        case "h":  # Hour delay
            time.sleep(3600)
