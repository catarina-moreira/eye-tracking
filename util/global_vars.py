import os
from unittest.loader import VALID_MODULE_NAME

class GlobalVars:

    # class constructor
    def __init__(self, isColab, flag ):
        # Data structure where all the information per patient will be stored
        self.PATIENTS_DIC, self.IMG_TO_PATIENT, self.IMG_TO_DIAGNOSIS = {}, {}, {}

        # this flag is used to re-index the full dataset or not. Set it to False to load pre-indexed data
        self.FLAG = flag 

        # initialize other global variables
        self.TOTAL_EYEGAZE, self.TOTAL_REFLACX, self.TOTAL_BOTH = 0, 0,0 

        if not isColab:
            # path to github
            self.GDRIVE_MAIN = os.path.join( "C:", "Users", "cmore", "GitHub", "eye-tracking", "")
            self.EYE_GAZE_PATH = os.path.join( "D:", "EYE-GAZE", "")
            self.REFLACX_PATH = os.path.join("D:", "REFLACX", "" )
            self.REFLACX_XAMI_METADATA = os.path.join("D:","", "XAMI-MIMIC", "speadsheets", "REFLACX", "metadata.csv" )
            # MIMIC-XAMI full dataset path: update to your own dataset path
            self.MIMIC_PATH = os.path.join("D:", "XAMI-MIMIC","")
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

    # updates the path to GitHub
    def updateGDrive(self, new_path ):
        self.GDRIVE_MAIN = new_path

    def getREFLACX_XAMI_METADATA(self):
        return self.REFLACX_XAMI_METADATA

    # returns the total number of patients in the EYE GAZE dataset
    def getTOTAL_EYE_GAZE(self):
        return self.TOTAL_EYEGAZE
    
    def setTOTAL_EYE_GAZE(self, value):
        self.TOTAL_EYEGAZE = value

    # returns the total number of patients in the REFLACX dataset
    def getTOTAL_REFLACX(self):
        return self.TOTAL_REFLACX
    
    def setTOTAL_REFLACX(self, value):
        self.TOTAL_REFLACX = value

    # returns the total number of patients in both REFLACX and EYE GAZE
    def getTOTAL_BOTH(self):
        return self.TOTAL_BOTH
    
    def setTOTAL_BOTH(self, value):
        self.TOTAL_BOTH = value

    def getMIMIC_PATH(self):
        return self.MIMIC_PATH
    
    def getGDRIVE_MAIN(self):
        return self.GDRIVE_MAIN
    
    def getEYE_GAZE_PATH(self):
        return self.EYE_GAZE_PATH

    def getPATIENTS_DIC(self):
        return self.PATIENTS_DIC
    
    def setPATIENTS_DIC(self, new_dict):
        self.PATIENTS_DIC = new_dict
    
    def getFLAG(self):
        return self.FLAG

    def insertPatientIntoPATIENTS_DIC(self, new_patient ):
        self.PATIENTS_DIC[ new_patient.getPatient_key() ] = new_patient

    def insertDataIMG_TO_DIAGNOSIS(self, key, value ):
        self.IMG_TO_DIAGNOSIS[key] = value

    def insertDataIMG_TO_PATIENT(self, key, value ):
        self.IMG_TO_PATIENT[key] = value

    def getIMG_TO_DIAGNOSIS(self):
        return self.IMG_TO_DIAGNOSIS
    
    def setIMG_TO_DIAGNOSIS(self, new_dict):
        self.IMG_TO_DIAGNOSIS = new_dict
    
    def getIMG_TO_PATIENT(self):
        return self.IMG_TO_PATIENT
    
    def setIMG_TO_PATIENT(self, new_dict):
        self.IMG_TO_PATIENT = new_dict
    
    def getMIMICDictionaries(self):
        return self.PATIENTS_DIC, self.IMG_TO_DIAGNOSIS, self.IMG_TO_PATIENT




