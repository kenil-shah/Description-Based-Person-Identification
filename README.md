# Description_Based_Person_Identification

![Alt Text](https://github.com/Kenils/Description_Based_Person_Identification/blob/master/readme_images/Person_Retrieval.jpeg)

**Locating a particular  person in a given surveillance video using a set of soft-biometric queries such as height,color and gender.**

## Installation

1) Clone this repository.

2) In the repository, execute `pip install -r requirements.txt` to install all the necessary libraries.
	
3) Three deep learning models are used inorder to filter out the desired person.
	1) *Mask_RCNN:- Used to determine the coordinates of the person and fetch the pixelwise segmentation of the person*
	2) *gender_model:- Used to determine gender of the person*
	3) *color_model:- Used to determine torso color of the person*
4)Download the pretrained weights.
	1) Mask_RCNN[pretrained weights](https://drive.google.com/open?id=1g8hvgQ199VmevOuoTJtaR9yo0CPheqxt) and save it in root directory
	2) gender_model[pretrained weights](https://drive.google.com/open?id=1ZB67dCOY_mSGBFtDL6EteKb_uOTodN9J) and save it in /modalities/gender/ 
	3) color_model[pretrained weight](https://drive.google.com/open?id=13EpN25wSwI5gcoEs8wgJ8OmFx4Y6-YfW) and save it in /modalities/torso_color/ 

