import numpy as np
import tracker

tracking = tracker.Tracker(2.75)
tracking.run('emborrachado_SM_01.mp4')
print(f'cubo andou ::: {tracking.desloc} cm \nmarcardor tem tamanho ::: {tracking.marker_px} pixels e {tracking.marker_cm} cm')