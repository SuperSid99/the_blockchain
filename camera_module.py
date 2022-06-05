import watchdog.events
import watchdog.observers
import logging
from blockchain_main import execute_camera_module_process
import time
from common import connect, chunks, get_key_by_addr
from constants import MAIN_SERVER_IP, MAIN_SERVER_PORT, CAMERA_MODULES_IPS

CAMERA_MODULE_IP = "100.81.249.49"
FORMAT = "utf-8"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('')


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.png', '*.jpeg', '*.txt'],
                                                             ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        try:
            st_time = time.time()
            log.info("Execution Started.")
            log.info(f"[STEP 1] Image added to folder at {sttime}\n")
            key = get_key_by_addr(CAMERA_MODULE_IP, CAMERA_MODULES_IPS)
            log.info("[STEP 2] Encrypting the Received Image")
            en_image = execute_camera_module_process(event.src_path, key)
            log.info("Encrypted Image received")
            log.info("[STEP 3] Sending Data to Main Server")
            send_image_to_main_server(en_image)
            end_time = time.time()
            log.info(f"Execution ended at {end_time}\n")
            log.info(f"total time taken = {end_time - st_time}\n")
        except Exception as e:

            log.error("En error Occurred while Processing.")
            log.info(f"Error >> {e}")

    # Event is created, you can process it now

    def on_modified(self, event):
        log.info(f"Watchdog received modified event - {event.src_path}.")

    # Event is modified, you can process it now


def send_image_to_main_server(en_image):
    connection = connect((MAIN_SERVER_IP, MAIN_SERVER_PORT))
    log.info("Connected To Main Server")
    i = 0
    connection.send("camera".encode(FORMAT))
    # time.sleep(4)
    var = connection.recv(512).decode()
    if var == "OK":
        log.info("Sending data in Chunks")
        for chunk in chunks(en_image, 100):
            connection.send(chunk.encode(FORMAT))
            i += 1
        log.info("All Data sent")

    connection.close()

    time.sleep(2)


if __name__ == "__main__":
    # add the source path to your folder
    src_path = r'/home/vishwajeet/Travclan/BLK/the_blockchain/images/'
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    log.info(f"Listening to Path ====> {src_path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
