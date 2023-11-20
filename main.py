import keyboard
import traceback
import csv
import time
from threading import Thread
import psutil

class KeysAndInfoLogger:
    checkDelay = 0.1
    def clearInfo(self):
        self.hotkeysUsingCount = 0
        self.timer = 0
    def __init__(self, filename, writeTime, hotKeys):
        self.clearInfo()
        self.filename = filename
        self.writeTime = writeTime
        self.hotkeys = hotKeys
        keyboardThread = Thread(name="KeyboardHandler", target=self.runKeyboardHandler, daemon=True)
        keyboardThread.start()
        print('Logger started successfully')
    def launchChecker(self): 
        while True:
            try:
                if self.timer >= self.writeTime:
                    self.writeToCsv()
                self.timer += self.checkDelay
                time.sleep(self.checkDelay)
            except Exception as msg:
                print('exeption! ', msg)
                self.writeError()
                break
    def writeToCsv(self):
        csvObject = csv.writer(open(self.filename, encoding='utf-8', mode="+a"), delimiter = ",", lineterminator="\r")
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S')
        print('write to CSV ', currentTime)
        csvObject.writerows([
            [currentTime, "HotKeysClicked", self.hotkeysUsingCount],
            [currentTime, "RAMUsing(%)", psutil.virtual_memory().percent],
            [currentTime, "ProccessorCPU(%)", psutil.cpu_percent()]
        ]);
        self.clearInfo()
    def writeError(self):
        csvObject = csv.writer(open('error.csv', encoding='utf-8', mode="+a"), delimiter = ",", lineterminator="\r")
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S')
        print('write error to CSV ', currentTime)
        csvObject.writerow([currentTime, "Error", traceback.format_exc()])
    def handleHotkey(self, *args, **kwargs):
        self.hotkeysUsingCount += 1
    def runKeyboardHandler(self):
        for hotkey in self.hotkeys:
            keyboard.add_hotkey(hotkey, self.handleHotkey)
        keyboard.wait()

def main():
    kandl = KeysAndInfoLogger('info.csv', 60, ["ctrl+z", "ctrl+a", "ctrl+c", "ctrl+v", "alt+tab"])
    kandl.launchChecker()
    print("Program closed or aborted.")

if __name__ == "__main__":
    main()