from tornado import web,ioloop
import time
import multiprocessing
import json
import maker
import configparser
import random

clients = []
running = 0

sessionIdGlobal = multiprocessing.Value('i', 0)
statusUpdateIndicator = multiprocessing.Value('i',1)
generateRequestQueue = multiprocessing.Queue()

codebaseConfig = configparser.ConfigParser()

'''
configOSettings = {
    "DEV_MAC_ID": "50DC000000000000",
    "DEV_EXT_PAN": "6000000000000000",
    "DEV_CHAN_MASK": "26"
}
generateRequest = {
    "sessionId": 0,
    "projName":"intel",
    "confBase":configOSettings,
    "macStart": 1206,
    "macEnd": 1209,
    "devFolderPath": "../../BC3_3_SAMR21_Applications/Codebase/Applications/SZ_Dali_Master_Dev"
}
'''
def getStatus():
    global statusUpdateIndicator
    print('statusUp: ',statusUpdateIndicator.value)    
    return statusUpdateIndicator.value


class MainHandler(web.RequestHandler):
    def get(self):
        self.render("login_page.html")

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class StaticFileHandler(web.RequestHandler):
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
                genReq = generateRequestQueue.get()
                maker.main(genReq, self.statusUpdateCtr)
            time.sleep(1)

        
class DeviceHandler(web.RequestHandler):
   
    def get(self, endPoint):
        #global configOsettings
        #global generateRequest
        print("endPoint GET: ", endPoint)
        if(endPoint == None):
            print(codebaseConfig["DEVICES"]["devicelist"])
            cfInit = {}
            cfInit["devicelist"] = codebaseConfig["DEVICES"]["devicelist"]
            cfInit["project_codes"] = {}
            for key in codebaseConfig['PROJECT_CODES']:
                cfInit["project_codes"][key] = codebaseConfig["PROJECT_CODES"][key]
            cfInit["GlobalConfigOptions"] = {}   
            for key in codebaseConfig["GlobalConfigOptions"]:
                cfInit["GlobalConfigOptions"][key] = codebaseConfig["GlobalConfigOptions"][key]
            self.write(json.dumps(cfInit))
        else:
            devDump = {}
            devDump["macbase"] = codebaseConfig[endPoint]["macbase"]
            devDump["versions"] = codebaseConfig[endPoint]["versions"]
            #configOsettings["devFolderPath"] = codebaseConfig[endPoint]["codepath"]
            self.write(json.dumps(devDump))
        #self.write(str(getStatus()))

    
    def post(self, endPoint):
        print("endPoint POST: ", endPoint)

class APIHandler(web.RequestHandler):
    fileName=""
    def get(self, endPoint):
        global fileName
        print("endPoint GET: ", endPoint)
        if endPoint == "statusUpdate":
            self.write(str(statusUpdateIndicator.value))

        elif endPoint == "fileName":
            self.write(fileName)
            #with open(fileName, 'rb') as f:
                #self.write(f)

    def post(self, endPoint):
        global fileName
        print("endPoint POST: ", endPoint)
        if endPoint == "generate":
            print("[*] Config form submitted")
            
            configForm = {}
            generateRequest = {}
            configOSettings = {}
            generateRequest["confBase"] = configOSettings
            configForm = json.loads(self.request.body.decode("utf-8"))
            proj = configForm["project"]
            if proj == None:
                proj = "0"
            configOSettings["DEV_MAC_ID"]    = codebaseConfig[configForm["deviceName"]]["macbase"] + proj.zfill(3)
            generateRequest["macStart"]      = int(configForm["macStart"])
            generateRequest["macEnd"]        = int(configForm["macEnd"])
            generateRequest["projName"]      = configForm["projName"]
            configOSettings["DEV_EXT_PAN"]   = configForm["DEV_EXT_PAN"]
            configOSettings["DEV_CHAN_MASK"] = configForm["DEV_CHAN_MASK"]
            deviceName                       = configForm["deviceName"]
            generateRequest["devFolderPath"] = codebaseConfig[deviceName]["codepath"]
            fileName = configOSettings["DEV_CHAN_MASK"]+"_"+configOSettings["DEV_EXT_PAN"]+".zip"
            for key in generateRequest:
                print(key, generateRequest[key])
            generateRequestQueue.put(generateRequest)
            
        elif endPoint == "sessionId":
            print(json.loads(self.request.body.decode("utf-8")))
            rr = random.randint(1000,9999)
            sessionIdGlobal.value = rr
            self.write(str(sessionIdGlobal.value))


def make_app():

    return web.Application([
        (r"/", IndexHandler),
        #(r"/statusUpdate", status_update),
        (r"/device/([a-zA-Z]+)?", DeviceHandler),
        (r"/api/([a-zA-Z]+)?", APIHandler),
        #(r"/device", DeviceHandler),
        (r"/static/(.*)", web.StaticFileHandler, {'path':  './static'}),
        (r"/download/(.*)", web.StaticFileHandler, {'path':  './download'}),
    ], debug=False)



if __name__ == "__main__":
    random.seed(a=None)
    #global bablu
    codebaseConfig.sections()
    codebaseConfig.read('../CIS/codebase_configuration.cfg')
    gg = generate_files(statusUpdateIndicator)
    gg.daemon = True
    gg.start()
    app = make_app()
    app.listen(8888)
    print("Server started")
    ioloop.IOLoop.current().start()
    
