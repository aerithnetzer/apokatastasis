from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import build
from pathlib import Path

WATCH_DIRS = [
    Path("content"),
    Path("templates"),
    Path("static"),
]

WATCH_EXTS = {".md", ".html", ".css", ".js"}

class RebuildHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)

        if path.suffix not in WATCH_EXTS:
            return

        print(f"Change detected in {path}, rebuilding…")
        build.build_site()

def watch():
    observer = Observer()
    for d in WATCH_DIRS:
        observer.schedule(RebuildHandler(), str(d), recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
