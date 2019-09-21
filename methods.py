from data_bridge import *
from cv2 import cv2
import os
import cv2
import coco
import model as modellib
import PersonFilter
from DenseColor import DenseNet
from DenseGender import DenseNet as densegender
from keras.optimizers import SGD
import config

# Root directory of the project
ROOT_DIR = os.getcwd()

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "mylogs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")


class Raw_video:
    def __init__(self, root):
        self.data_bridge = Singleton(Data_bridge)
        self.gui_root = root

    def main_thread(self):
        self.cap = cv2.VideoCapture(self.data_bridge.selected_video_file_path)
        while self.data_bridge.start_process_manager:
            ret, frame = self.cap.read()
            if ret==True:
                cv2.imshow('Video', frame)
                cv2.waitKey(100)
            else:
                self.data_bridge.start_process_manager = False
                break
            self.gui_root.update()
        cv2.destroyAllWindows()
        self.cap.release()


class YOLO_person_detection:
    def __init__(self, root):
        self.data_bridge = Singleton(Data_bridge)
        self.gui_root = root
        class InferenceConfig(coco.CocoConfig):
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
            NUM_CLASSES = 1 + 80

        inference_config = InferenceConfig()
        # Load Mask R-CNN Model (Object Detection)
        self.model = modellib.MaskRCNN(mode="inference", config=inference_config, model_dir=MODEL_DIR)
        # Get path to saved weights
        model_path = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
        assert model_path != "", "Provide path to trained weights"
        print("Loading weights from ", model_path)
        self.model.load_weights(model_path, by_name=True)
        print("-----------------------------Mask-RCNN Model Loaded-----------------------------")

        # Load Dense-Net Model for Color Classification
        ColorWeights_path = 'modalities/torso_color/color_model.h5'
        self.ColorModel = DenseNet(reduction=0.5, classes=12, weights_path=ColorWeights_path)
        sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        self.ColorModel.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
        print("-----------------------------Color Model Loaded-----------------------------")

        # Load Dense-Net Model for Gender Classification
        GenderWeights_path = 'modalities/gender/gender_model.h5'
        self.GenderModel = densegender(reduction=0.5, classes=2, weights_path=GenderWeights_path)
        sgd = SGD(lr=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
        self.GenderModel.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])
        print("-----------------------------Gender Model Loaded-----------------------------")

    def main_thread(self):

        # Classes
        class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                       'bus', 'train', 'truck', 'boat', 'traffic light',
                       'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                       'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                       'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                       'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                       'kite', 'baseball bat', 'baseball glove', 'skateboard',
                       'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                       'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                       'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                       'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                       'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                       'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                       'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                       'teddy bear', 'hair drier', 'toothbru    sh']

        # Attributes
        output_storage_path = "output/"

        capture = cv2.VideoCapture(self.data_bridge.selected_video_file_path)
        frame_name = 0
        while self.data_bridge.start_process_manager:
            try:
                ret, frame = capture.read()
                '''
                The following module detects the person in the surveillance frame. It also
                gives the semantic segmentation within the person's bounding box.
                '''
                text_file = open(output_storage_path + "/person_coordinates.txt", 'a')
                results = self.model.person_detection([frame], verbose=1)
                r = results[0]
                rois = r['rois']
                mask = r['masks']
                class_ids = r["class_ids"]
                scores = r["scores"]
                PersonFilter.person_identification(frame_name, frame, rois, mask, class_ids, scores, class_names, color_model=self.ColorModel, gender_model=self.GenderModel, text_file=text_file, output_storage_path=output_storage_path)
                frame_name = frame_name + 1
                text_file.close()
            except:
                break
            self.gui_root.update()
