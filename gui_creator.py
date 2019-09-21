from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from data_bridge import *



class GUI_Creator_temp:
    def __init__(self):
        self.data_bridge = Singleton(Data_bridge)
        self.root = Tk()
        self.root.title("Description Based Person Identification")
        self.content = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        self.chosen_method = StringVar()

        self.color = StringVar()
        self.color.set('Red')
        self.color_choices = ['Black', 'Blue', 'Brown', 'Green','Grey', 'Orange','Pink','Purple','Red','White','Yellow','Skin']

        self.hgt_range = StringVar()
        self.hgt_range.set('130-160')
        self.hgt_choices = ['130-160', '150-170', '160-180', '170-190', '180-210']

        self.gender = StringVar()
        self.gender.set('Male')
        self.gender_choices=['Male','Female']

        self.camera = StringVar()
        self.camera.set('1')
        self.camera_choices = ['1', '2', '3', '4', '5', '6']

    def defining_labels(self):

        # Title label
        self.title_label = ttk.Label(self.content, text="Input queries screen")
        self.title_label.config(font=("Courier", 20,'bold'))

        #Modalities title
        self.height_label = ttk.Label(self.content, text="Height Range")
        self.height_label.config(font=("Courier", 8))
        self.color_label = ttk.Label(self.content, text="Gender")
        self.color_label.config(font=("Courier", 8))
        self.gender_label = ttk.Label(self.content, text="Torso color")
        self.gender_label.config(font=("Courier", 8))
        self.camera_label = ttk.Label(self.content, text="Camera No.")
        self.camera_label.config(font=("Courier", 8))

        # Video select label
        self.video_select_label = ttk.Label(self.content, text="Modalities")
        self.video_select_label.config(font=("Courier", 14,'bold'))
        self.methods_label = ttk.Label(self.content, text="Methods")
        self.methods_label.config(font=("Courier", 12,'bold'))

    def defining_buttons(self):

        # video select button
        self.video_select_button = ttk.Button(self.content, text="Select Video", command=self.select_video_file)

        # process video button
        self.process_video_button = ttk.Button(self.content, text="Process frame", command=self.process_video_method)

        # stop video processing video button
        self.stop_video_processing_button = ttk.Button(self.content, text="Stop processing", command=self.stop_processing_video)
    
        #Drop down menus
        self.hgt_option = OptionMenu(self.content, self.hgt_range, *self.hgt_choices)
        self.color_option = OptionMenu(self.content, self.color, *self.color_choices)
        self.gender_option = OptionMenu(self.content, self.gender, *self.gender_choices)
        self.camera_option = OptionMenu(self.content, self.camera, *self.camera_choices)

    def select_video_file(self):
        self.selected_video_file_path = filedialog.askopenfilename()
        self.video_select_label["text"] = self.selected_video_file_path
        self.data_bridge.selected_video_file_path = self.selected_video_file_path

    def define_radio_buttons_for_method_select(self):
        self.raw_video = ttk.Radiobutton(self.content, text='Raw Video', variable=self.chosen_method, value='raw_video')
        self.yolo_pd = ttk.Radiobutton(self.content, text='Sequential model', variable=self.chosen_method, value='yolo_pd')

    def process_video_method(self):
        self.data_bridge.camera_entered = self.camera.get()
        self.data_bridge.color_entered = self.color.get()
        self.data_bridge.hgt_entered = self.hgt_range.get()
        self.data_bridge.gender_entered = self.gender.get()
        self.data_bridge.methode_chosen_by_radio_butten = self.chosen_method.get()
        self.data_bridge.start_process_manager = True
        pass

    def stop_processing_video(self):
        self.data_bridge.start_process_manager = False
        pass

    def defining_geometry_grid(self):
        self.content.grid(column=0, row=0, sticky=(N, S, E, W))
        self.title_label.grid(column=1, row=0, columnspan=2, sticky=(N, W), padx=5)

        #Modalities

        self.height_label.grid(column=2,row=4,sticky=(E))
        self.gender_label.grid(column=2,row=5,sticky=(E))
        self.color_label.grid(column=2,row=6,sticky=(E))
        self.camera_label.grid(column=2,row=7,sticky=(E))

        self.gender_option.grid(column=3,row=6,sticky=(N))
        self.hgt_option.grid(column=3,row=4,sticky=(N))
        self.color_option.grid(column=3,row=5,sticky=(N))
        self.camera_option.grid(column=3,row=7,sticky=(N))

        self.video_select_label.grid(column=3, row=2, columnspan=2, sticky=(N, W))
        self.raw_video.grid(column=0, row=6)
        self.yolo_pd.grid(column=0, row=7)
        self.process_video_button.grid(column=0, row=8)
        self.stop_video_processing_button.grid(column=0, row=9)
        self.video_select_button.grid(column=0, row=2)
        self.methods_label.grid(column = 0, row = 5,sticky=(N))

    def defining_whole_ui(self):
        self.defining_labels()
        self.defining_buttons()
        self.define_radio_buttons_for_method_select()
        self.defining_geometry_grid()

    def update(self):
        print("The text is", self.newname.get())
        self.root.mainloop()
