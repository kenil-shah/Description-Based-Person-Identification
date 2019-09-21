from data_bridge import *
from gui_creator import GUI_Creator_temp
from process_manager import Process_manager
import threading


class App:
    """
    This is app class which will be called when running our UI. Everything other will be called inside this class.
    """

    def __init__(self):
        self.data_bridge = Singleton(Data_bridge)
        self.gui_creator = GUI_Creator_temp()
        self.gui_creator.defining_whole_ui()
        self.process_manager = Process_manager(self.gui_creator.root)

    def gui_thread(self):
        self.gui_creator.root.after(0, self.process_task)
        self.gui_creator.root.mainloop()

    def process_task(self):
        self.process_manager.main_task()

app = App()
app.gui_thread()
