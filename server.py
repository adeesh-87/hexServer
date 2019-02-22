import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.options import define, options
import os
import time
import multiprocessing
import threading
import json
import maker
import re

clients = []
running = 0

statusUpdateIndicator = multiprocessing.Value('i',1)
generateRequestQueue = multiprocessing.Queue()

configOSettings = {
    "DEV_MAC_ID": "50DC000000000000",
    "DEV_EXT_PAN": "6000000000000000",
    "DEV_CHAN_MASK": "26"
}
generateRequest = {
    "confBase":configOSettings,
    "macStart": 1206,
    "macEnd": 1209,
    "devFolderPath": "../../BC3_3_SAMR21_Applications/Codebase/Applications/SZ_Dali_Master_Dev"
}

def getStatus():
    global statusUpdateIndicator
    print('statusUp: ',statusUpdateIndicator.value)    
    return statusUpdateIndicator.value


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class StaticFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('static/main.js')

class generate_files(multiprocessing.Process):
    def __init__(self, statusUpdateCtr):
        global running
        self.statusUpdateCtr = statusUpdateCtr
        multiprocessing.Process.__init__(self)
        running = 1
        return

    def close(self):
        running = 0
        return

    def run(self):
        global running
        while running:
            if not generateRequestQueue.empty():
                currentConfig = generateRequestQueue.get()
                maker.main(generateRequest, self.statusUpdateCtr)
            time.sleep(1)

        
class RequestHandler(tornado.web.RequestHandler):
    
    def get(self, endPoint):
        print("endPoint GET: ", endPoint)
        self.write(str(getStatus()))

    
    def post(self, endPoint):
        print("endPoint POST: ", endPoint)
        
        print("[*] Config form submitted")
        
        configForm = {}
        form_data = json.loads(self.request.body.decode("utf-8"))
        #form_data = json.loads(self.request.body.decode("utf-8"))
        form_data_temp = re.split('\&',form_data)
        for cf in form_data_temp:
            configForm[re.split('=',cf)[0]] = re.split('=',cf)[1]
        #form_data = re.split('=',form_data2)
        #print(configForm)
        generateRequest["macStart"]      = configForm["macStart"]
        generateRequest["macEnd"]        = configForm["macEnd"]
        #configOSettings["DEV_MAC_ID"]    = configForm["DEV_MAC_ID"]
        configOSettings["DEV_EXT_PAN"]   = configForm["DEV_EXT_PAN"]
        configOSettings["DEV_CHAN_MASK"] = configForm["DEV_CHAN_MASK"]
        for key in generateRequest:
            print(key, generateRequest[key])
	    
        #generateRequestQueue.put(generateRequest)
        

    def getDeviceConfig(self):
        return
    
def make_app():

    return tornado.web.Application([
        (r"/", MainHandler),
        #(r"/statusUpdate", status_update),
        (r"/api/([a-zA-Z]+)?", RequestHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path':  './static'}),
        
    ], debug=False)



if __name__ == "__main__":
    #global bablu
    
    gg = generate_files(statusUpdateIndicator)
    gg.daemon = True
    gg.start()
    app = make_app()
    app.listen(8888)
    print("Server started")
    tornado.ioloop.IOLoop.current().start()
    
