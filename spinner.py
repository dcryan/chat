import threading
import itertools
import time
import sys

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        spinner = itertools.cycle(['-', '/', '|', '\\'])
        while True:
            yield next(spinner)

    def __init__(self, delay=None):
        self.delay = delay or self.delay

    def start(self):
        self.busy = True
        spinner_generator = self.spinning_cursor()
        def spinning():
            while self.busy:
                sys.stdout.write(next(spinner_generator))
                sys.stdout.flush()
                time.sleep(self.delay)
                sys.stdout.write('\b')
                sys.stdout.flush()
        self.thread = threading.Thread(target=spinning)
        self.thread.start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)
        self.thread.join()
        sys.stdout.write('\r')
        sys.stdout.flush()
