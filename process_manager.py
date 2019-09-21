from methods import *
from data_bridge import *




class Process_manager:

    def __init__(self, root):
        self.data_bridge = Singleton(Data_bridge)
        self.gui_root = root
        self.methods_dict = {'raw_video': Raw_video(self.gui_root),
                             'yolo_pd': YOLO_person_detection(self.gui_root)}


    def update_root(self):
        self.gui_root.update()

    def main_task(self):
        while True:
            while not self.data_bridge.start_process_manager:
                A = 0
                self.gui_root.update()
            self.methods_dict[self.data_bridge.methode_chosen_by_radio_butten].main_thread()
            self.gui_root.update()
