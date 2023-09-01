############################################################################
# Perodically take screen image and compare it with reference images
# Date: 01.09.2023
############################################################################

import numpy as np
import os, cv2, pyautogui
from pathlib import Path
from .settings import Settings

class CScreenCapture:

    DebugImages = []                # Add indices here for images which sould be created (Debug only)
    CompareImages = dict()

    def __init__(self) -> None:
        self.loadCompareImages()
    
    def loadCompareImages(self):
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..' , 'src', 'compare', Settings["GENERAL"]["GameSelection"], Settings["GENERAL"]["ScreenResolution"])
        for file in os.listdir(folder):
            if file.endswith(".png"):
                fileName = Path(file).stem
                self.CompareImages[fileName] = cv2.imread(os.path.join(folder, file))

    def doesContainSubImage(self):
        screen_img = self._getNewScreenCapture()

        # Run trough 3 parts of settings.ini
        for i in range(1, 4):
            # Check if setting in settings.ini can be detected
            if f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_{i}' not in Settings:
                raise IndexError(f'Compare image not set in settings.ini - RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_{i}')
            # Check if reference is used
            if int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_{i}']['Used']) == 0:
                continue
            # Get some position and size values
            refImage = self.CompareImages[Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_{i}']['RefImageName']]
            x = int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_{i}']['SubframeX'])
            y = int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_{i}']['SubframeY'])
            h = refImage.shape[0]
            w = refImage.shape[1]

            # Work on images
            cropped_img = screen_img[y:y+h, x:x+w] # img[y:y+h, x:x+w]
            diff_img = cv2.absdiff(cropped_img, refImage)
            mask = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
            # Apply filter
            th = 5
            imask =  mask>th
            canvas = np.zeros_like(refImage, np.uint8)
            canvas[imask] = refImage[imask]
            # Count black values
            valueCanvas = np.sum(canvas == 0)
            # Debug output
            if int(i) in self.DebugImages:
                folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..' , 'debug')
                Path(folder).mkdir(parents=True, exist_ok=True)
                cv2.imwrite(os.path.join(folder, f"compare_{i}.png"), refImage)
                cv2.imwrite(os.path.join(folder, f"cropped_{i}.png"), cropped_img)
                cv2.imwrite(os.path.join(folder, f"diff_{i}.png"), diff_img)
                cv2.imwrite(os.path.join(folder, f"mask_{i}.png"), mask)
                cv2.imwrite(os.path.join(folder, f"canvas_{i}.png"), canvas)
                print('-----------------------------')
                print(f'valueCanvas ({i}): {str(valueCanvas)}')
                print('Contains: True' if valueCanvas > int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_{i}']['Sensitivity']) else 'Contains: False')
            
            # Enough pixels met condition?
            if valueCanvas > int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_{i}']['Sensitivity']):
                return True, int(i)
        return False, -1

    # Get new screenshot
    def _getNewScreenCapture(self):
        img = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        return img
        #cv2.imwrite("image1.png", img)

ScreenCapture = CScreenCapture()