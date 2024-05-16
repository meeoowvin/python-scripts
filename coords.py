import pyautogui
import time

print("Move the mouse over the 'Browse' button and press Ctrl+C to exit.")
try:
    while True:
        x, y = pyautogui.position()
        position_str = f"X: {x}, Y: {y}"
        print(position_str, end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nCoordinates captured. Use these coordinates in your script.")