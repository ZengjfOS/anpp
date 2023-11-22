import sys
import subprocess

class Shell:

    def __init__(self, log: list) -> None:
        self.log = log
        self.currentCmdLog = []

    def start(self, cmd):
        self.process = None
        self.currentCmdLog = []

        if sys.platform.startswith('linux'):
            self.process = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif sys.platform.startswith('win32'):
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif sys.platform.startswith('darwin'):
            self.process = subprocess.Popen(["zsh", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if self.process != None:
            while True:
                line = self.process.stdout.readline()
                if line.decode('utf-8') == '' and self.process.poll() is not None:
                    break

                if line:
                    # print(line.decode('utf-8'))
                    self.log.append(line.decode('utf-8'))
                    self.currentCmdLog.append(line.decode('utf-8'))

            retCode = self.process.returncode
            self.process = None

            return {"status": retCode, "output": "".join(self.currentCmdLog)}
        else:
            return {"status": 1, "output": ""}

    def terminate(self):
        if self.process != None:
            self.process.terminate()

if __name__ == "__main__" :
    print(Shell().start("adb devices"))
    print(Shell().start("adb root"))
    print(Shell().start("adb shell cat /proc/bootprof"))
