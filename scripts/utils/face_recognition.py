import os
from typing import Tuple
from collections import deque

import numpy as np
import cv2

from video_buffer import Numpy_Buffer, Video_Reader


class Face_Detector:
    def __init__(self, 
                 haar_cascade_path: str,
                 scale_factor: float,
                 min_neighbors: int,
                 min_size: Tuple[int, int]
                 ) -> None:
        self.cascade = cv2.CascadeClassifier(haar_cascade_path)

        # scales
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size

    
    def frame_detect(self, img: np.ndarray, pad: int = 0) -> None:
        faces = self.cascade.detectMultiScale(
            image=img,     
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,     
            minSize=self.min_size
        )

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x - pad, y - pad), (x+w + pad,y+h + pad), (255,0,0), 2)
            roi_color = img[y:y+h, x:x+w]

        cv2.imshow('frame', img)

    
    def batch_detect(self, batch: np.ndarray, pad: int = 0) -> None:
        for i, img in enumerate(batch.copy()):
            img = img.astype(np.uint8)
            faces = self.cascade.detectMultiScale(
                image=img,     
                scaleFactor=self.scale_factor,
                minNeighbors=self.min_neighbors,     
                minSize=self.min_size
            )
            print(f'frame_{i}, Data Type: {img.dtype}')

            for (x,y,w,h) in faces:
                cv2.rectangle(img, 
                              (x - pad, y - pad), 
                              (x+w + pad,y+h + pad), 
                              (255, 0, 0), 2)
                # roi_color = img[y:y+h, x:x+w]

            # cv2.imshow(f'frame_{i}', img) # calling this as a GUI has issues with underlying QT library

            if cv2.waitKey(10) & 0xFF == ord('q'): 
                break


def main():
    height, width = 480, 640
    q = deque(maxlen=60)
    buff = Numpy_Buffer((height, width, 3), 30)
    vr = Video_Reader(buff)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_path = os.path.join(script_dir, 'Cascades/haarcascade_frontalface_default.xml')

    detector = Face_Detector(cascade_path,
                            1.2,
                            5,
                            (20, 20))
    
    
    vr.start_threads(q)

    while True:
        with vr.lock:
            try:
                batch = q[0]
                q.popleft()
                # print(f'{batch[0][0][0]}')

                detector.batch_detect(batch, 70)

            except Exception as e:
                # print(f"Error: {e}")
                pass
        
            if cv2.waitKey(10) & 0xFF == ord('q'): 
                    vr.stop_threads()
                    break
        
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()