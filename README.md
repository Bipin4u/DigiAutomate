# DigiAutomate

### Video Recording with Motion Detection:
The record_video function captures video from the default camera (index 0). It writes the video frames to a file and displays them in a window. Motion detection is implemented by comparing the current frame with a static background. If significant movement is detected, it is counted as motion. A timestamp is overlaid on each frame to log the exact time the frame was captured.

### Log Collection:
The record_log function captures real-time log data from the connected Android device using ADB. Logs are continuously written to a text file until the logging flag is cleared.

### Motion Detection Check:
The VideoCheck function periodically checks the motion detected in the video. It ensures that the video stream is functional and not just capturing a "black picture". If no motion is detected over multiple checks, the function flags the issue.

### Stream File Modification:
The modifyStreamFile function modifies an XML configuration file used by the streaming application to point to a new stream file. This is necessary for testing different streams.

### Automated Application Control:
The automateATSC function automates interactions with a Windows application (Atsc3Xpress.exe) using the pywinauto library. It opens a stream file in the application and handles dialog windows.

### Remote Control Simulation:
The channelOperation function simulates key presses on the Android device using ADB commands. This is used to simulate remote control operations on the device under test.

### Thread Management:
The script uses threading to run video recording, log collection, and other tasks concurrently. This allows for efficient and simultaneous execution of different processes.

### Control Flow:
The main loop iterates over a list of stream files and runs the video recording and log collection for each stream in a loop. After each iteration, it checks if there were any issues detected (e.g., no motion in the video), and if so, it collects a bug report.



