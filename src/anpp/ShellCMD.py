import sys
import subprocess

def Shell(cmd):
    out = None

    if sys.platform.startswith('linux'):
        out = subprocess.Popen(["bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    elif sys.platform.startswith('win32'):
        pass
    elif sys.platform.startswith('darwin'):
        pass

    out.wait()

    if out != None:
        data = out.stdout.read()
        print(out.returncode)
        if data != None:
            return {"status": out.returncode, "output": data.decode('utf-8').strip()}
        else:
            return {"status": out.returncode, "output": ""}
    else:
        return {"status": 1, "output": ""}

if __name__ == "__main__" :
    print(Shell("adb devices"))
    print(Shell("adb root"))
    print(Shell("adb shell cat /proc/bootprof"))
