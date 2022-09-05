from controller import Controller
from gui import Gui

def main():
    controller = Controller()
    Gui(controller).run()

if __name__ == "__main__":
    main()