
from typing import Any, Tuple
from collections import deque
import threading
import time

import cv2
import numpy as np

class Config:
    def __init__(self, 
                 max_buffer_size,
                 batch_size,
                 image_dim: Tuple[int, int, int], # cwh
                 ) -> None:
        self.MAX_BUFFER_SIZE = max_buffer_size
        self.batch = np.ndarray((batch_size, *image_dim), dtype=np.int8)

    def capture_init(self, cap: cv2.VideoCapture)-> None:
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))


class Dequeue_Buffer:
    def __init__(self, config: Config) -> None:
        self.q = deque(maxlen=config.MAX_BUFFER_SIZE)
        self.size = 0
        self.config = config

        self.batched = threading.Condition()
        self.batch_size = self.config.batch.shape[0]
    

    def enqueue(self, x)-> None:
        with self.batched:
            self.q.append(x)
            self.size += 1

            self.batched.notify()

    def dequeue(self) -> None:
        with self.batched:
            # if it not batched, wait
            while not self.q or self.size < self.batch_size:
                self.batched.wait()
            
            # if it is batched pass it to the batch
            for i in range(self.batch_size):
                self.config.batch[i] = self.q[0]
                self.q.popleft()

            self.size -= self.batch_size
            self.batched.notify()
    

class Frame_Buffer:
    def __init__(self, 
                 config: Config,
                 src: str = 0,
                 buffer = Dequeue_Buffer) -> None:
        self.config = config
        self.buffer = buffer(config=self.config)

        self.cap = cv2.VideoCapture(src)
        self.config.capture_init(self.cap)
        self.frame_cntr = 0
        

    def read_frames(self) -> None:
        while True:
            success, frame = self.cap.read()
            # print(f'Read frame #{self.frame_cntr}')
            
            if not success:
                print('All frames have been read or frame error')
                break

            if cv2.waitKey(10) & 0xFF == ord('q'): break

            # if frame exists
            self.buffer.enqueue(frame)
            self.frame_cntr +=1

        # destroy capture
        self.cap.release()


    def write_frames(self):
        while True: 
            self.buffer.dequeue()
            print(f'BATCH shape: {self.config.batch.shape}')
            print(f'BATCH value: {self.config.batch[0]}')
    

    def start_threads(self) -> None:
        self.read_thread = threading.Thread(target=self.read_frames)
        time.sleep(1)
        self.write_thread = threading.Thread(target=self.write_frames)

        self.read_thread.start()
        self.write_thread.start()


    def stop_threads(self):
        self.read_thread.join()
        self.write_thread.join()

    
def main():
    config = Config(max_buffer_size=512,
                    batch_size=30,
                    image_dim=(480, 640, 3))
                    # image_dim=(3, 1280, 720))
    
    buff = Frame_Buffer(config=config)
    buff.start_threads()
    buff.stop_threads()

    # threading
    
if __name__ == '__main__':
    main()

