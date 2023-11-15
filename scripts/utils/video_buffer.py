from typing import Any, Tuple, Optional
import threading
import time
from collections import deque
from abc import ABC, abstractmethod

import numpy as np
import cv2


class Buffer(ABC):
    @abstractmethod
    def __init__(self,
                 img_shape: Tuple[int, int, int],
                 batch_size: int,
                 max_size: int,
                 ) -> None:
        self.start = 0
        self.end = 0
        self.batch_size = batch_size
        self.img_shape = img_shape

    @abstractmethod
    def read(self, img) -> None: pass

    @abstractmethod
    def write(self, queue: deque, lock: threading.Lock) -> None: pass


class Numpy_Buffer(Buffer):
    def __init__(self, 
                 img_shape: Tuple[int, int, int], 
                 batch_size: int, 
                 max_size: Optional[int] = 120
                 ) -> None:
        super().__init__(img_shape, 
                         batch_size, 
                         max_size)
        self.max_size = max_size
        self.buff = np.ndarray(shape=(self.max_size, *self.img_shape), dtype=np.int8)
        self.flag = False
        self.lock = threading.Lock()
        
    
    def read(self, img) -> None:
        self.buff[self.end] = img
        self.end = (self.end + 1) % self.max_size

        if self.end < self.start: self.flag = True


    def write(self, queue: deque, lock: threading.Lock) -> None:
        with lock:
            if not self.flag and (self.end - self.start) > self.batch_size:
                queue.append(self.buff[self.start:self.start+self.batch_size+1])
                self.start += self.batch_size + 1

            elif self.flag and (self.max_size - self.start) + (self.end) + 1 > self.batch_size:
                if (self.max_size - self.start) > self.batch_size:
                    queue.append(self.buff[self.start:self.start+self.batch_size+1])
                    self.start += self.batch_size + 1
                    
                else:
                    bs = self.batch_size - (self.max_size - self.start)
                    b1 = self.buff[self.start:]
                    b2 = self.buff[:bs+1]
                    queue.append(np.concatenate((b1, b2), axis=0))
                    self.start = bs+1
            
            else: queue.append(None)



class Video_Reader:
    def __init__(self, buffer: Buffer, src: str = 0) -> None:
        self.buffer = buffer
        self.stop_event = threading.Event()
        self.src = src
        self.lock = threading.Lock()


    def read(self):
        self.cap = cv2.VideoCapture(self.src)

        while not self.stop_event.is_set():
            success, frame = self.cap.read()

            if not success:
                print('All frames have been read or frame error')
                self.stop_event.set() 
                break

            if cv2.waitKey(10) & 0xFF == ord('q'): 
                self.stop_event.set() 
                break

            self.buffer.read(frame)
        self.cap.release()


    def write(self,
              queue: deque, 
              lock: threading.Lock,
              func: Optional[callable] = None
              ) -> None:        
        while not self.stop_event.is_set():
            if func is None:
                self.buffer.write(queue, lock)

            else:
                func(self.buffer.write, queue, lock)
    

    def start_threads(self, 
                      queue: deque, 
                      func: Optional[callable] = None
                      ) -> None:
        rt = threading.Thread(target=self.read)
        wt = threading.Thread(target=self.write, kwargs={
            'queue': queue,
            'func': func,
            'lock': (self.lock)
        })

        rt.start()
        wt.start()


    def stop_threads(self) -> None: self.stop_event.set()


def main():
    q = deque(maxlen=60)
    np_buff = Numpy_Buffer((480, 640, 3), 30)
    
    vr = Video_Reader(np_buff)
    vr.start_threads(q)

    while True:
        with vr.lock:
            try:
                batch = q[0]
                q.popleft()
                print(batch[0][0][0])
            except: pass

    vr.stop_threads()


if __name__ == '__main__':
    main()










