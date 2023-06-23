class Observable:
    def __init__(self):
        self.observers = list()

    def notify(self, dark_mode):
        for observer in self.observers:
            observer.update_(dark_mode)

    def attach(self, observer):
        self.observers.append(observer)


class Observer:
    def __init__(self):
        self.dark_mode = False

    def update_(self, dark_mode):
        if dark_mode:
            with open(f"scripts/settings/styles/dark/{self.__class__.__name__}.qss") as f:
                stylesheet = f.read()
        else:
            with open(f"scripts/settings/styles/light/{self.__class__.__name__}.qss") as f:
                stylesheet = f.read()

        self.dark_mode = dark_mode
        self.setStyleSheet(stylesheet)