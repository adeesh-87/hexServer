import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
import os
import time
import multiprocessing
import threading
import json
import struct as stroo

class generate_files(multiprocessing.Process):
    #bablu = "1"
    def __init__(self):
        global running
        self.bablu = 0
        multiprocessing.Process.__init__(self)

        running = 1
        return

    def close(self):
        running = 0
        return

    def getStatus(self):
        return self.bablu
    
    def incr(self):
        global running
        
        if running:
            bbb = int(self.bablu)
            #print(self.bablu)
            bbb = bbb + 1
            self.bablu = str(bbb)
            print(self.bablu)
            time.sleep(5)

    def run(self):
        thr1 = threading.Thread(target=self.incr)
        thr1.start()
        thr1.join()
