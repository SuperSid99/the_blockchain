import watchdog.events
import watchdog.observers
from blockchain_main import execute_camera_module_process
import time
from common import connect, chunks
from constants import MAIN_SERVER_IP, MAIN_SERVER_PORT

CAMERA_MODULE_IP = "IP TO BE Set"
FORMAT = "utf-8"


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.jpeg', '*.txt'],
                                                             ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        # print("Watchdog received created event - % s." % event.src_path)
        sttime=time.time()
        print(f"image added to folder at {sttime}\n")
        en_image = execute_camera_module_process(event.src_path, CAMERA_MODULE_IP)
        send_image_to_main_server(en_image)
        endtime=time.time()
        print(f"execution ended at {endtime}\n")
        print(f"total time taken = {endtime-sttime}\n")

    # Event is created, you can process it now

    def on_modified(self, event):
        print(f"Watchdog received modified event - {event.src_path}.")
        # execute_process(event.src_path)

    # Event is modified, you can process it now


def send_image_to_main_server(en_image):
    connection = connect((MAIN_SERVER_IP, MAIN_SERVER_PORT))
    i = 0
    connection.send("camera".encode(FORMAT))
    time.sleep(2)
    print("Sending data in Chunks")
    for chunk in chunks(en_image, 100):
        print(f"Sending chunk {i}")
        connection.send(chunk.encode(FORMAT))
        i += 1

    print("All Data sent")

    connection.close()

    time.sleep(2)


if __name__ == "__main__":
    # add the source path to your folder
    src_path = r'/Users/siddharthsharma/Desktop/the_blockchain'
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
