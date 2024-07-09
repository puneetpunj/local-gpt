import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.start_script()

    def start_script(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(['python3', self.script])

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print(f'{self.script} changed, reloading...')
            self.start_script()

if __name__ == "__main__":
    script = 'main.py'
    event_handler = FileChangeHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
