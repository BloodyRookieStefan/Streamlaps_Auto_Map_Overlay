############################################################################
# Main loop and entry point
# Date: 01.09.2023
############################################################################
import lib, time

class CController:

    def loop(self):
        # Set state machine to release
        lib.SM.moveNext(lib.Commands.RELEASE)
        # Init streamlabs
        lib.Log.info('Init streamlabs connection')
        lib.Streamlabs.removeOverlay()
        # Endless loop
        lib.Log.info('Joining endless loop')
        while True:
            contains, index = lib.ScreenCapture.doesContainSubImage()
            if contains and lib.SM.getCurrentState() == lib.States.RELEASED:
                comment = lib.Settings[f'RESOLUTION_{lib.Settings["GENERAL"]["ScreenResolution"]}_REF_{index}']['Comment']
                lib.Log.info(f'Set screen overlay - Detected {comment}')
                lib.SM.moveNext(lib.Commands.LOCK)
                lib.Streamlabs.setOverlay(index)
            elif not contains and lib.SM.getCurrentState() == lib.States.LOCKED:
                lib.Log.info('Remove screen overlay')
                lib.SM.moveNext(lib.Commands.RELEASE)
                lib.Streamlabs.removeOverlay()
            else:
                # Do nothing
                pass

            # Wait till next picture
            time.sleep(float(lib.Settings['GENERAL']['RefreshTime']))

if __name__ == '__main__':
    c = CController()
    c.loop()    
