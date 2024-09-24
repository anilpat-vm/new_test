import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pypandoc

# Path to your Word document and README.md file
DOCX_PATH = ".github/workflows/Code Review.docx"
README_PATH = ".github/workflows/readme.md"
REPO_PATH = ".github/workflows"

class WordDocHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == DOCX_PATH:
            print(f"{DOCX_PATH} has been modified. Updating README.md...")
            # Convert the .docx to .md
            try:
                pypandoc.convert_file(DOCX_PATH, 'md', outputfile=README_PATH)
                print("README.md updated successfully.")
                
                # Commit and push to GitHub
                self.push_to_github()
            except Exception as e:
                print(f"Error during conversion: {e}")

    def push_to_github(self):
        try:
            os.chdir(REPO_PATH)
            subprocess.run(["git", "add", README_PATH])
            subprocess.run(["git", "commit", "-m", "Update README.md from Word document"])
            subprocess.run(["git", "push"])
            print("Changes pushed to GitHub.")
        except Exception as e:
            print(f"Error during git operations: {e}")

if __name__ == "__main__":
    event_handler = WordDocHandler()
    observer = Observer()
    observer.schedule(event_handler, path=DOCX_PATH, recursive=False)

    print(f"Watching {DOCX_PATH} for changes...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
