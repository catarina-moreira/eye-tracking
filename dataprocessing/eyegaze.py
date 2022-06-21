import os
import pandas as pd
from dataprocessing.mimicdata import MIMICDataProcessor
from dataprocessing.patient import Patient
from util.global_vars import GlobalVars

class EyeGazeProcessor(MIMICDataProcessor):
    
    def __init__( self, global_vars : GlobalVars ):
        print("Loading EYE GAZE dataset at: ")
        super().__init__(global_vars)
        self.matersheet_path = os.path.join(self.global_vars.getEYE_GAZE_PATH(), "master_sheet.csv")
        print("\t" + os.path.join(self.global_vars.getEYE_GAZE_PATH(), "master_sheet.csv"))
    
    def processEYE_GAZE( self ):
        
        print("\t Processing EYE GAZE dataset...")
        metadata = pd.read_csv( self.getMastersheetPath() )
        global_vars = self.getGlobalVars()
        metadata.fillna(-100, inplace=True)

        # for each study in the metadata master sheet
        for indx in range(0,metadata.shape[0]):

            # extract all patient data from EYE GAZE and XAMI MIMIC datasets
            # get a dictionary with the study ID, patient ID and image ID
            patient_data = {}
            patient_data = self.extractIdentifiersEYEGAZE( metadata, indx )
            self.extractEYEGAZEDataFromXAMI( metadata, patient_data, indx )

            # create a new patient and add it to the patients dictionary
            new_patient = Patient( patient_data['PATIENT_KEY'], patient_data, "EYE GAZE")
            global_vars.insertPatientIntoPATIENTS_DIC( new_patient )
            
            global_vars.increment_EYE_GAZE()
    
    # general function that uses the Mastersheet from EYE GAZE dataset and 
    # extracts information in the form of a dictionary
    def extractEYEGAZEDataFromXAMI(self, metadata : pd.DataFrame, patient_data : dict, indx : int ):

        # saving XAMI MIMIC DATA paths
        self.extractMIMICPaths( patient_data ) 
        # extract patients data
        self.getPatientsAttributes(metadata, patient_data, indx)
        # add key conditions
        self.getKeyConditions_CheXpert( metadata, patient_data, indx )
        # add patients' symptoms
        self.getSymptoms(metadata, patient_data, indx)
        # add full diagnosis
        self.getOverallDiagnosis(metadata, patient_data, indx )
        # add image information
        self.getImageInformation(patient_data)
        # add audio information from radiologist's readings
        self. getAudioInformation( patient_data )
        # get fixation points data
        self.getEyeGazeData(patient_data)
        # extract bounding boxes
        self.getPatientsBoundingBoxes(patient_data)

    def getPatientsBoundingBoxes(self, patient_data : dict ):

        global_vars = self.getGlobalVars()
        patient_folder = "patient_" + patient_data['PATIENT_ID']
        bounding_boxes_df = pd.read_csv(os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "bounding_boxes.csv"))

        bb_dict = {}
        for indx in range(0, len(bounding_boxes_df)):
            region_name = bounding_boxes_df.iloc[indx]["bbox_name"].upper()
            xmin = bounding_boxes_df.iloc[indx]["x1"]
            xmax = bounding_boxes_df.iloc[indx]["x2"]
            ymin = bounding_boxes_df.iloc[indx]["y1"]
            ymax = bounding_boxes_df.iloc[indx]["y2"] 

            bb_dict['BOUNDING_BOXES_' + region_name] = [xmin, xmax, ymin, ymax]
        patient_data['BOUNDING_BOXES'] = bb_dict

    def generatePyGazePaths(self, patient_id : str, patient_folder : str, image_id : str, plot_type : str):
        
        global_vars = self.getGlobalVars()
        # create and store paths for pupil plots
        plot_dic = {}
        plot_dic['GENERAL'] = os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "EyeTrackingPlots", plot_type, plot_type[0]+"_" + patient_id + "_" + image_id + ".csv" )
        plot_dic['SILENT'] = os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "EyeTrackingPlots", plot_type, plot_type[0]+"_Silent_" + patient_id + "_" + image_id + ".csv" )
        plot_dic['TALKING'] = os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "EyeTrackingPlots", plot_type, plot_type[0]+"_Talking_" + patient_id + "_" + image_id + ".csv" )
        return plot_dic
    
    def getEyeGazeData(self, patient_data : dict ):

        global_vars = self.getGlobalVars()
        image_id = patient_data['IMAGE_ID']
        patient_id = patient_data['PATIENT_ID']
        patient_folder = "patient_" + patient_id

        # raw eye gaze data. If raw gaze file does not exist in XAMI dataset, add it
        existsGazeFile = os.path.exists(os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "gaze.csv" ))
        if not existsGazeFile:
            print("Creating gaze file for " + patient_folder)
            gaze_file_master = pd.read_csv( os.path.join(global_vars.EYE_GAZE_PATH, "eye_gaze.csv") )
            gaze_file_patient = gaze_file_master[gaze_file_master['DICOM_ID'] == patient_data['IMAGE_ID']]
            gaze_file_patient.to_csv(os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "gaze.csv"),  index=False)
    
        patient_data['GAZE'] = os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "gaze.csv")
        patient_data['FIXATIONS'] = os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "fixations.csv")

        # folders to save fixation / gaze heatmaps and masks
        existsDir = os.path.exists( os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "PyGazePlots", "" ))
        if not existsDir:
            os.makedirs(os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "PyGazePlots", "" ))
            os.makedirs(os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "PyGazePlots", "Pupils", "" ))
            os.makedirs(os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "PyGazePlots", "Fixations", "" ))
            os.makedirs(os.path.join(global_vars.MIMIC_PATH, patient_folder, "EyeGaze", "PyGazePlots", "Gaze", "" ))

        temp_dict = {}
        temp_dict['PUPILS'] = self.generatePyGazePaths(patient_id, patient_folder, image_id, "Pupils")
        temp_dict['FIXATIONS'] = self.generatePyGazePaths(patient_id,patient_folder, image_id, "Fixations")
        temp_dict['GAZE'] = self.generatePyGazePaths(patient_id,patient_folder, image_id, "Gaze")
        patient_data['PyGAZE_PLOTS'] = temp_dict


    def getAudioInformation(self, patient_data ):
        image_ID = patient_data['IMAGE_ID']
        audio_segmentation_folder =  os.path.join(patient_data['EYE_GAZE_PATH'], "audio_segmentation_transcripts", image_ID)
        audio_dic = {}
        audio_dic['MP3'] = os.path.join(audio_segmentation_folder, "audio.mp3")
        audio_dic['WAV'] = os.path.join(audio_segmentation_folder, "audio.wav")
        audio_dic['TRANSCRIPT'] = os.path.join(audio_segmentation_folder, "transcript.json")
        patient_data['AUDIO'] = audio_dic
    
    def getImageInformation(self, patient_data : dict):
        global_vars = self.getGlobalVars()
        patient_folder = "patient_" + patient_data["PATIENT_ID"] 
        image_ID = patient_data['IMAGE_ID']
        study_ID = patient_data['STUDY_ID']
        
        patient_data['CXR_JPG_PATH'] =  os.path.join(global_vars.getMIMIC_PATH(), patient_folder, "CXR-JPG", study_ID, image_ID + ".jpg")
        patient_data['CXR_DICOM_PATH'] = os.path.join(global_vars.getMIMIC_PATH(), patient_folder, "CXR-DICOM", study_ID, image_ID + ".dcm")

        # get segmentations
        # keeping a record of the paths for the masks for mediastinum, lungs and aorta
        audio_segmentation_folder =  os.path.join(patient_data['EYE_GAZE_PATH'], "audio_segmentation_transcripts", image_ID)
    
        segmentation_dic = {}
        segmentation_dic["MEDIASTINUM"] =  os.path.join(audio_segmentation_folder, "mediastanum.png")
        segmentation_dic["LUNG_RIGHT"] = os.path.join(audio_segmentation_folder, "right_lung.png")
        segmentation_dic["LUNG_LEFT"] = os.path.join(audio_segmentation_folder, "left_lung.png")
        segmentation_dic["AORTA"] =  os.path.join(audio_segmentation_folder, "aortic_knob.png")

        patient_data['SEGMENTATIONS'] = segmentation_dic

    def getPatientsAttributes(self, metadata : pd.DataFrame, patient_data : dict, indx : int ):

        patient_data['AGE'] = metadata['anchor_age'].values[indx]
        patient_data['GENDER'] = metadata['gender'].values[indx]
    
    def getSymptoms(self, metadata : pd.DataFrame, patient_data : dict, indx : int):

        symptoms_dic = {}
        for i in range(1, 9):
            medical_code = metadata["dx" + str(i) + "_icd"]
            medical_comment = metadata["dx" + str(i)]

            if( medical_comment.values[indx] == -100 ):
                continue
            else:
                symptoms_dic["dx" + str(i)] = medical_code.values[indx]
                symptoms_dic["dx" + str(i) + "_icd"] = medical_comment.values[indx]
        patient_data['SYMPTOMS'] = symptoms_dic

    def getOverallDiagnosis(self, metadata : pd.DataFrame, patient_data : dict, indx : int ):
        global_vars = self.getGlobalVars()
        CHF = metadata['CHF'].values[indx]
        pneumonia = metadata['pneumonia'].values[indx]
        normal = metadata['Normal'].values[indx]  

        if CHF == 1 : patient_data['DIAGNOSIS']['GLOBAL'] = "CHF"
        if pneumonia == 1 : patient_data['DIAGNOSIS']['GLOBAL'] = "Pneumonia"
        if normal == 1 : patient_data['DIAGNOSIS']['GLOBAL'] = "Normal"

        global_vars.insertDataIMG_TO_DIAGNOSIS( patient_data['IMAGE_ID'],  patient_data['DIAGNOSIS']['GLOBAL'] )
        global_vars.insertDataIMG_TO_PATIENT( patient_data['IMAGE_ID'],  patient_data['PATIENT_KEY'] )

    def getKeyConditions_CheXpert(self, metadata : pd.DataFrame, patient_data : dict, indx : int ):
        lst, lst_chexpert = [], []
    
        diagnosis_dic = {}
        # the metadata dataframe contains a series of columns with the key conditions
        # that were identified by ChestXpert
        # we extract the index of the first key condition of the dataframe to get
        # a list of all key conditions
        columns = metadata.columns.tolist()
        start_indx = columns.index("consolidation")
        key_conditions = metadata[columns[start_indx:-2]].iloc[indx]

        # add mimic ED medical comments
        diagnosis_dic['COMMENTS'] = metadata['cxr_exam_indication'].values[indx] 

        for condition in key_conditions.keys().tolist():
            # key conditions detected by CheXpert
            if "chx" in condition: # 
                if key_conditions[condition] == 1:
                    lst_chexpert.append(condition.replace("__chx", ""))
                    continue
            # key conditions predicted using NLP techniques on MIMIC CXR dataset reports
            if key_conditions[condition] == 1:
                condition = condition.replace("\n", "")
                lst.append( condition )

        # abnormalities detected using NLP techniques applied directly to MIMIC CXR dataset reports
        diagnosis_dic['KEY_CONDITIONS_NLP'] = lst  
        # abnormalities detected using CHEXPERT predictions
        diagnosis_dic['KEY_CONDITIONS_CHEXPERT_PRED'] = lst_chexpert
        # add information to patient data
        patient_data['DIAGNOSIS'] = diagnosis_dic

    def extractMIMICPaths(self, patient_data ):
        global_vars = self.getGlobalVars()
        patient_folder = "patient_" + patient_data["PATIENT_ID"] 
        mimic_path = global_vars.getMIMIC_PATH()

        # 1. patient's mastersheet file path
        patient_data['METADATA'] =  os.path.join(mimic_path, patient_folder, "EyeGaze", "master_sheet.csv")
        # 2. patient's MIMIC CORE path
        patient_data['CORE_PATH'] = os.path.join(mimic_path, patient_folder, "Core", "")
        # 3. patient's MIMIC ED path
        patient_data['ED'] = os.path.join(mimic_path, patient_folder, "ED", "")
        # 4. patient's EYE GAZE dataset path
        patient_data['EYE_GAZE_PATH'] = os.path.join(mimic_path, patient_folder, "EyeGaze", "")
    
    def extractIdentifiersEYEGAZE(self, metadata, indx ):
        global_vars = self.getGlobalVars()
        patient_data = {} # dictionary that will hold patients data
        patient_data['STUDY_ID'] =   "s" + str( metadata.loc[indx,'study_id'])
        patient_data['IMAGE_ID'] =   str( metadata.loc[indx,'dicom_id'])
        patient_data['PATIENT_ID'] = str( metadata.loc[indx,'patient_id'])


        # update the key of the patient if the patient has more than one medical study
        patient_key_base = str( metadata.loc[indx,'patient_id']) + "_IMG"
        for i in range(1, 10):
            patient_key = patient_key_base + str(i)
            if patient_key in global_vars.getPATIENTS_DIC().keys():
                continue
            else:
                patient_data['PATIENT_KEY'] = patient_key
                break
        return patient_data

    def getMastersheetPath(self):
        return self.matersheet_path
    
    def setMasterSheetPath(self, new_path):
        self.matersheet_path = new_path

