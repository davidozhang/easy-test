# -*- coding: utf-8 -*-
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == self.path:
            self.easy_test._test()

    def set_path(self, path):
        self.path = path

    def set_easy_test(self, easy_test):
        self.easy_test = easy_test

class EasyTestMonitor():
    def __init__(self, **kwargs):
        event_handler = FileModifiedHandler()
        event_handler.set_path(kwargs['path'])
        event_handler.set_easy_test(kwargs['object'])
        self.observer = Observer()
        self.observer.schedule(
            event_handler,
            path=kwargs['directory'],
            recursive=False,
        )

    def _start(self):
        self.observer.start()

    def _stop(self):
        self.observer.stop()
        self.observer.join()
