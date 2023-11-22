import sys
import subprocess

class Shell:

    def __init__(self) -> None:
        pass

    def start(self, cmd):
        self.process = None

        if sys.platform.startswith('linux'):
            self.process = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif sys.platform.startswith('win32'):
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif sys.platform.startswith('darwin'):
            self.process = subprocess.Popen(["zsh", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if self.process != None:
            self.process.wait()

            data = self.process.stdout.read()
            retCode = self.process.returncode

            self.process = None

            return {"status": retCode, "output": data.decode('utf-8').strip()}
        else:
            return {"status": 1, "output": ""}

    def terminate(self):
        if self.process != None:
            self.process.terminate()

if __name__ == "__main__" :
    print(Shell().start("adb devices"))
    print(Shell().start("adb root"))
    print(Shell().start("adb shell cat /proc/bootprof"))
