import time

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
