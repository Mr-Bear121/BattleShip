import threading
import time

lstThreads = {}
pause = threading.Event()

def threadStart():
    
    if pause.is_set():
        break

if __name__ == '__main__':
    
    listThreads['1'] = threading.Thread(target=threadStart)
    listThreads['2'] = threading.Thread(target=threadStart)
