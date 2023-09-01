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
        # Run trough compare images
        for k in self.CompareImages:
            # Check if compare image is set in settings.ini
            if not f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_REF_{k}' in Settings:
                raise IndexError(f'Compare image not set in settings.ini - RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_REF_{k}')
            # Get some position and size values
            x = int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_REF_{k}']['SubframeX'])
            y = int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_REF_{k}']['SubframeY'])
            h = self.CompareImages[k].shape[0]
            w = self.CompareImages[k].shape[1]
            # Work on images
            cropped_img = screen_img[y:y+h, x:x+w] # img[y:y+h, x:x+w]
            diff_img = cv2.absdiff(cropped_img, self.CompareImages[k])
            mask = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
            # Apply filter
            th = 5
            imask =  mask>th
            canvas = np.zeros_like(self.CompareImages[k], np.uint8)
            canvas[imask] = self.CompareImages[k][imask]
            # Count black values
            valueCanvas = np.sum(canvas == 0)
            # Debug output
            if int(k) in self.DebugImages:
                folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..' , 'debug')
                Path(folder).mkdir(parents=True, exist_ok=True)
                cv2.imwrite(os.path.join(folder, f"compare_{k}.png"), self.CompareImages[k])
                cv2.imwrite(os.path.join(folder, f"cropped_{k}.png"), cropped_img)
                cv2.imwrite(os.path.join(folder, f"diff_{k}.png"), diff_img)
                cv2.imwrite(os.path.join(folder, f"mask_{k}.png"), mask)
                cv2.imwrite(os.path.join(folder, f"canvas_{k}.png"), canvas)
                print('-----------------------------')
                print(f'valueCanvas ({k}): {str(valueCanvas)}')
                print('Contains: True' if valueCanvas > int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_REF_{k}']['Sensitivity']) else 'Contains: False')
            
            # Enough pixels met condition?
            if valueCanvas > int(Settings[f'RESOLUTION_{Settings["GENERAL"]["ScreenResolution"]}_REF_{k}']['Sensitivity']):
                return True, int(k)
        return False, -1

    # Get new screenshot
    def _getNewScreenCapture(self):
        img = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        return img
        #cv2.imwrite("image1.png", img)

ScreenCapture = CScreenCapture()