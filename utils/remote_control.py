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