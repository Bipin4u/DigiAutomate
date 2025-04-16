import subprocess
import os

def record_log(i, j):
    # Clear the logcat buffer
    os.system('adb logcat -c')
    process = subprocess.Popen(["adb", "logcat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    file = "C:\Users\bipin.kumar\OneDrive - HCL Technologies Ltd\Desktop\StabilityReport\logs\" + 'log_' + str(i) + '_' + str(j) + '.txt'
    with open(file, 'w') as fh:
        while log_flag.is_set():  # Loop runs while log_flag is True
            line = process.stdout.readline().decode('utf-8')  # Read line from adb logcat
            fh.write(line.strip())  # Write log line to file

