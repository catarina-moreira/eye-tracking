import os

class GlobalVars:

    # class constructor
    def __init__(self, isColab ):
        # Data structure where all the information per patient will be stored
        self.PATIENTS_DIC, self.IMG_TO_PATIENT, self.IMG_TO_DIAGNOSIS = {}, {}, {}

        # this flag is used to re-index the full dataset or not. Set it to False to load pre-indexed data
        self.FLAG = False 

        # initialize other global variables
        self.TOTAL_EYEGAZE, self.TOTAL_REFLACX, self.TOTAL_BOTH = 0, 0,0 

        if not isColab:
            # path to github
            self.GDRIVE_MAIN = os.path.join( "C:", "Users", "cmore", "GitHub", "eye-tracking", "")
            
            # MIMIC-XAMI full dataset path: update to your own dataset path
            self.MIMIC_PATH = os.path.join("D", "GoogleDrive", "Datasets", "XAMI-MIMIC", "XAMI-MIMIC","")
        else:
            self.GDRIVE_MAIN = "/content/drive/MyDrive/"
            self.MIMIC_PATH = self.GDRIVE_MAIN + "Datasets/XAMI-MIMIC/XAMI-MIMIC/"

    # setters 
    # increments the counter of patients who are in the EYE GAZE dataset
    def increment_EYE_GAZE(self):
        self.TOTAL_EYEGAZE = self.TOTAL_EYEGAZE + 1
    
    # increments the counter of patients who are in the REFLACX dataset
    def increment_REFLACX(self):
        self.TOTAL_REFLACX = self.TOTAL_REFLACX + 1

    # increments the counter of the patients who are both in
    # REFLACX and EYE GAZE datasets
    def increment_BOTH(self):
        self.TOTAL_BOTH = self.TOTAL_BOTH + 1

    # updates the path to the MIMIC dataset
    def updateMIMIC_PATH(self, new_path ):
        self.MIMIC_PATH = new_path
    

