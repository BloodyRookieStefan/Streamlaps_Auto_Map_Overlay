############################################################################
# Streamlaps controller
# Date: 01.09.2023
############################################################################

import asyncio, time
from pyslobs import SlobsConnection, ScenesService, config_from_ini
from threading import Thread
from .logger import Log
from .settings import Settings

class CSlobs:

    Run = True
    Started = False
    OverlayControl = -1
    OverlayActive = -1

    # Start async operation
    def main(self):
        asyncio.run(self._connect())

    # Set overlay visible to TURE
    def setOverlay(self, index):
        #Log.info('Set streamlabs overlay')   
        self.OverlayControl = index

    # Set all overlays visible to False
    def removeOverlay(self):
        #Log.info('Remove streamlabs overlay')   
        self.OverlayControl = 0

    # Is any overlay currently active?
    def isOverlayActive(self):
        return self.OverlayActive

    # Connect to streamlaps
    async def _connect(self):
        connection = SlobsConnection(config_from_ini())
        sService = ScenesService(connection)
        await asyncio.gather(connection.background_processing(), self._loop(connection, sService))

    # Main loop for streamlaps operations
    async def _loop(self, connection, sService):
        # All relevant names of stream overlay sources
        targetNamesContainer = [Settings['GENERAL'][f'SlobsOverlayName_REF1'], Settings['GENERAL'][f'SlobsOverlayName_REF2'], Settings['GENERAL'][f'SlobsOverlayName_REF3']]
        # Endless loop
        while self.Run:
            # Get active scene
            ssActive = await sService.active_scene()
            # Get scene items
            ssItems = await ssActive.get_items()
            # Control overlay
            if self.OverlayControl > -1:
                if self.OverlayControl == 0:
                    targetNames = targetNamesContainer
                else:
                    # Select overlay image
                    targetNames = [Settings['GENERAL'][f'SlobsOverlayName_REF{self.OverlayControl}']]
                # Search for screen item by name
                for i in ssItems:
                    if i.name in targetNames:
                        # Set setting visible
                        await i.set_settings({'visible': self.OverlayControl})
                self.OverlayControl = -1
            # Update is overlay active
            for i in ssItems:
                if i.name in targetNamesContainer:
                    self.OverlayActive = i._visible
                    # At least one reference is active
                    if self.OverlayActive:
                        break
            # Loop was run at least once
            self.Started = True
        # Close connection
        connection.close()
        Log.info('Streamlabs connection closed')   

Streamlabs = CSlobs()

Log.info('Establish streamlabs connection...')
# Create new thread
T = Thread(target=Streamlabs.main)
T.start()
# Wait till steamlabs connection is established
while not Streamlabs.Started and T.is_alive():
    pass
# Check if something went wrong
if not T.is_alive():
    Log.error('Could not establish streamlabs connection')
    exit(-1)
# All good
Log.info('Streamlabs connection establised')


# ---- Testing -----
#for i in range(0, 5):
#    if Streamlabs.isOverlayActive():
#        Streamlabs.removeOverlay()
#    else:
#        Streamlabs.setOverlay()
#    time.sleep(3)
#Streamlabs.Run = False
#time.sleep(1)
#print('Done')
# -----------------