import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


requirements = ['opencv-contrib-python',
                'opencv-python', 'mediapipe', 'mouse', 'pyautogui']

for r in requirements:
    try:
        install(r)
    except:
        print('>>> Failed to install', r,'<<<')
