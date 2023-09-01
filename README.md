# Streaming Auto Overlay
## About Streaming Auto Ovlerlay  
Control automatically a [streamlaps](https://streamlabs.com/) map overlay for games like **Hell Let Loose** or **Squad**.  
  
Streaming auto overlay is checking perodically your screen for distinctive images. If a match is detected [streamlaps](https://streamlabs.com/) gets a command to display the map overlay.  
No more worries about your key stroke events gets out of sync with the game you play.  
  
Currently streaming auto overlay is in testing phase

## Installation
Be sure you meet following requirements:  
- Python 3.9
- pip install numpy
- pip install opencv-python
- pip install [PySLOBS](https://github.com/Julian-O/PySLOBS/tree/master)
- pip install pyautogui
- Streamlabs OBS 1.13

## Setting it up
### autooverlay.ini  
Program settings
```config
# General settings
[GENERAL]
RefreshTime = 0.05                                  # Refresh time [s]
GameSelection=HLL                                   # Sub folder where the reference images are stored
ScreenResolution = 2560x1440                        # Resolution you are playing with and reference image resolutions
SlobsOverlayName_REF1 = OverlayIMG_SpawnScreen      # Streamlabs name of source which represents your overlay
SlobsOverlayName_REF2 = OverlayIMG_IngameMap        # Streamlabs name of source which represents your overlay
SlobsOverlayName_REF3 = OverlayIMG_MapCommander     # Streamlabs name of source which represents your overlay

# Information about first reference image
[RESOLUTION_2560x1440_1]
Used = 1                                            # Reference setting is used. If not set to false
SubframeX = 1787                                    # Where to expect the ref image - Start position X
SubframeY = 713                                     # Where to expect the ref image - Start position Y
Sensitivity = 20000                                 # Sensitivity value
RefImageName = 2                                    # Name of reference image to compare to 
Comment = SPAWN SCREEN                              # Free text

# Information about second reference image
[RESOLUTION_2560x1440_2]
Used = 1                                            # Reference setting is used. If not set to false
SubframeX = 1642                                    # Where to expect the ref image - Start position X
SubframeY = 1134                                    # Where to expect the ref image - Start position Y
Sensitivity = 10000                                 # Sensitivity value
RefImageName = 2                                    # Name of reference image to compare to 
Comment = MAP                                       # Free text

# Information about third reference image
[RESOLUTION_2560x1440_3]    
Used = 1                                            # Reference setting is used. If not set to false
SubframeX = 1379                                    # Where to expect the ref image - Start position X
SubframeY = 1136                                    # Where to expect the ref image - Start position Y
Sensitivity = 10000                                 # Sensitivity value
RefImageName = 2                                    # Name of reference image to compare to 
Comment = MAP_COMMANDER                             # Free text
```
### pyslobs.ini  
Connection information for your local Streamlaps installation.  
```config
[connection]
domain=localhost                                    # Domain to Streamlaps
port=59650                                          # Port tp Streamlaps API
token=*Your Streamlaps token*                       # API Token
```
Find you API token under `Settings - Remote Control - Show details - API Token**`

## Tested
Auto overlay was successfully tested with **Python 3.9.11** and **Streamlabs 1.13.3**


