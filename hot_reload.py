import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main import create_app

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, create_app_callback):
        self.create_app_callback = create_app_callback
        super().__init__()

    def on_modified(self, event):
        print("Code change detected. Reloading...")
        # Restart your PyQt application here
        app, window = self.create_app_callback()
        app.quit()
        time.sleep(1)  # Ensure the application is closed
        window.close()
        main()

def run_with_hot_reload(create_app_callback):
    event_handler = CodeChangeHandler(create_app_callback)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    main()

def main():
    while True:
        try:
            app, _ = create_app()
            sys.exit(app.exec_())
        except SystemExit:
            pass

if __name__ == "__main__":
    run_with_hot_reload(create_app)
