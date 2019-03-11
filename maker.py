import sys
import subprocess
import re
import fileinput
import asyncio
import os

def editConfigFile(basePath, configSettings):
    configFile = basePath + '/SZ_config.h'
    cFile = ''
    with open(configFile, 'rU') as pConfigFile:
        for line in pConfigFile:
            xx = re.split(' ', line)
            if xx[0] == '#define':
                cFile = cFile + xx[0] + " " + xx[1] + " "
                if(xx[1] == "DEV_CHAN_MASK"):
                    cFile = cFile + "(1ul<<"
                if((xx[1] == "DEV_MAC_ID") or (xx[1] == "DEV_EXT_PAN")):
                    cFile = cFile + "0x"
                cFile = cFile + configSettings[xx[1]] 
                if((xx[1] == "DEV_MAC_ID") or (xx[1] == "DEV_EXT_PAN")):
                    cFile = cFile + "ull"
                if(xx[1] == "DEV_CHAN_MASK"):
                    cFile = cFile + ")"
                cFile = cFile + "\n"
                #print("conf: ", xx[1],"from ", xx[2], ' -> ', config_settings[xx[1]] )
        pConfigFile.close()
    with open(configFile, 'w') as pConfigFile:
        pConfigFile.write(cFile)

def compileProc(basePath, configSettings, AppName, folderName):
    AppNameHex = AppName + ".hex"
    print(AppNameHex)
    with open('logout.txt','w') as outfile, open('logerr.txt','w') as errfile:
        compileCommand = ['make', 'clean', 'all']
        compileSubProc = subprocess.Popen(compileCommand, cwd = basePath, stdout = outfile, stderr = errfile)
        compileSubProc.wait()

        destFile = folderName + "/" + configSettings["DEV_MAC_ID"] + ".hex"
        command = ['mv', AppNameHex, destFile]
        renaming = subprocess.Popen(command, cwd = basePath, stdout = outfile, stderr = errfile)
        renaming.wait()
        #        print ("finished for 5003" + str(ID).zfill(12) + '.hex')
        

def worker(configSettings, basePath, folder):
    AppName = ''
    MakefileFile = basePath + '/Makefile'
    with open(MakefileFile, 'rU') as mf:
        for line in mf:
            xx = re.split(' |\n', line)
            if xx[0] == "APP_NAME":
                AppName = xx[2]
        mf.close()

    editConfigFile(basePath, configSettings)
    compileProc(basePath, configSettings, AppName, folder)

    #await t1
    #await futures

def main(generateRequest, statusUpdateCounter):
    
    statUp = statusUpdateCounter
    configSettingsBase = generateRequest["confBase"]
    macStart = generateRequest["macStart"]
    macEnd = generateRequest["macEnd"]
    deviceFolderPathBase = generateRequest["devFolderPath"]
    devMacBase = configSettingsBase["DEV_MAC_ID"][0:7]
    hexFileDestinationFolder = "executables/" + configSettingsBase["DEV_CHAN_MASK"] + "_" + configSettingsBase["DEV_EXT_PAN"]
    for key in generateRequest:
        print(generateRequest[key])
    with open('logout.txt','w') as outfile, open('logerr.txt','w') as errfile:
        command = ['mkdir', hexFileDestinationFolder]
        cmdSubProc = subprocess.Popen(command, cwd = deviceFolderPathBase, stdout = outfile, stderr = errfile)
        cmdSubProc.wait()

    counter = 1
    for i in range(macStart, macEnd):
        macExt = str(i).zfill(10)
        configSettingsBase["DEV_MAC_ID"] = devMacBase + macExt
        print("compiling for: ", configSettingsBase["DEV_MAC_ID"]) 
        worker(configSettingsBase, deviceFolderPathBase, hexFileDestinationFolder)
        delta = macEnd - macStart
        statUp.value = round((counter*100)/delta)
        counter = counter + 1

    # Compress generated files
    zippableFolderName = configSettingsBase["DEV_CHAN_MASK"] + "_" + configSettingsBase["DEV_EXT_PAN"]
    zippedFileName = zippableFolderName + ".zip"
    zippableFolderLocation = deviceFolderPathBase + "/executables/"
    with open('logout.txt','w') as outfile, open('logerr.txt','w') as errfile:
        command = ['zip', '-r', zippedFileName, zippableFolderName]
        cmdSubProc = subprocess.Popen(command, cwd = zippableFolderLocation, stdout = outfile, stderr = errfile)
        cmdSubProc.wait()
        print("zipped")
    with open('logout.txt','w') as outfile, open('logerr.txt','w') as errfile:
        command = ['mv', zippedFileName, "../../../../CIS/hexServer/download/"]
        cmdSubProc = subprocess.Popen(command, cwd = zippableFolderLocation, stdout = outfile, stderr = errfile)
        cmdSubProc.wait()
        print("zipped")
