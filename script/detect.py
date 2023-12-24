import sys
import subprocess

def detect_devices():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if "List of devices attached" in result.stdout:
            return len(result.stdout.splitlines()) - 2
        else :
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)  # Exit with an error code

if __name__ == "__main__":
    if detect_devices():
        print("[INFO] {} deviced detected".format(detect_devices()))
    else:
        print("[ERROR] No device detected. Please check your connection.")
        sys.exit(2)
