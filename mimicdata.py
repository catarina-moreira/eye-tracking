import os
from urllib.request import CacheFTPHandler
import pandas as pd
from util.global_vars import GlobalVars
from dataprocessing import patient

class MIMICDataProcessor:

  def __init__( self ):
    print("MIMICDataProcessor")

  def processEYE_GAZE(self, global_vars):
    print("Loading EYE GAZE original dataset...")
    metadata = pd.read_csv( os.path.join(global_vars.getEYE_GAZE_PATH(), "master_sheet.csv"))
    metadata.fillna(-100, inplace=True)

    # for each study in the metadata master sheet
    for indx in range(3): #range(metadata.shape[0]):

      # a patient can have more than one image in a study. 
      token = 1 # We will need to differentiate these patients

      # extract all patient data from EYE GAZE and XAMI MIMIC datasets
      # get a dictionary with the study ID, patient ID and image ID
      patient_data = {}
      patient_data = self.extractIdentifiersEYEGAZE( metadata, indx, token, global_vars )
      self.extractEYEGAZEDataFromXAMI( metadata, patient_data, indx, global_vars )

      # create a new patient and add it to the patients dictionary
      new_patient = patient.Patient( patient_data['PATIENT_KEY'], patient_data, "EYE GAZE")
      global_vars.insertPatientIntoPATIENTS_DIC( new_patient )


  def extractEYEGAZEDataFromXAMI(self, metadata : pd.DataFrame, patient_data : dict, indx : int, global_vars : GlobalVars ):

    # keeping track of patients unique identifiers
    patient_folder = "patient_" + patient_data["PATIENT_ID"] 
    mimic_path = global_vars.getMIMIC_PATH()
    
    # saving XAMI MIMIC DATA paths
    self.extractMIMICPaths( patient_data, global_vars ) 
    # add key conditions
    self.getKeyConditions_CheXpert( metadata, patient_data, indx, global_vars )
    # add full diagnosis
    self.getOverallDiagnosis(metadata, patient_data, indx, global_vars )

    


  def getOverallDiagnosis(self, metadata : pd.DataFrame, patient_data : dict, indx : int, global_vars : GlobalVars ):

    CHF = metadata['CHF'].values[indx]
    pneumonia = metadata['pneumonia'].values[indx]
    normal = metadata['Normal'].values[indx]  

    if CHF == 1 : patient_data['DIAGNOSIS']['GLOBAL'] = "CHF"
    if pneumonia == 1 : patient_data['DIAGNOSIS']['GLOBAL'] = "Pneumonia"
    if normal == 1 : patient_data['DIAGNOSIS']['GLOBAL'] = "Normal"

    global_vars.insertDataIMG_TO_DIAGNOSIS( patient_data['IMAGE_ID'],  patient_data['DIAGNOSIS']['GLOBAL'] )
    global_vars.insertDataIMG_TO_PATIENT( patient_data['IMAGE_ID'],  patient_data['PATIENT_KEY'] )


  def getKeyConditions_CheXpert(self, metadata : pd.DataFrame, patient_data : dict, indx : int, global_vars : GlobalVars ):
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
  

  def extractMIMICPaths(self, patient_data, global_vars ):
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

  def extractIdentifiersEYEGAZE(self, metadata, indx, token, global_vars ):

    patient_data = {} # dictionary that will hold patients data
    patient_data['STUDY_ID'] =   "s" + str( metadata.loc[indx,'study_id'])
    patient_data['IMAGE_ID'] =   str( metadata.loc[indx,'dicom_id'])
    patient_data['PATIENT_ID'] = str( metadata.loc[indx,'patient_id'])

    # update the key of the patient if the patient has more than one medical study
    patient_data['PATIENT_KEY'] =str( metadata.loc[indx,'patient_id']) + "_IMG" + str(token)
    if patient_data['PATIENT_KEY'] in global_vars.getPATIENTS_DIC().keys():
      token = token + 1
      patient_data['PATIENT_KEY'] = str(metadata.loc[indx,'patient_id']) + "_IMG" + str(token)
    
    return patient_data
  


    
    