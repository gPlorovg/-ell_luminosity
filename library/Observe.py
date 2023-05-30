class Observable:
    def __init__(self):
        self.observers = list()

    def notify(self, dark_mode):
        for observer in self.observers:
            observer.update_(dark_mode)

    def attach(self, observer):
        self.observers.append(observer)


class Observer:
    def update_(self, dark_mode):
        self.setSyleSheet()