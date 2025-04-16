import cv2, datetime, time
import os

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


