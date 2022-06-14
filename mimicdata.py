import os
import pandas as pd
from util.global_vars import GlobalVars
from dataprocessing import patient

class MIMICDataProcessor:

  def __init__( self ):
    print("MIMICDataProcessor")

  def processEYE_GAZE(self, global_vars):
    print("Loading EYE GAZE original dataset...")
    metadata = pd.read_csv( os.path.join(global_vars.getEYE_GAZE_PATH(), "master_sheet.csv"))

    # for each study in the metadata master sheet
    for indx in range(metadata.shape[0]):

      # a patient can have more than one image in a study. 
      token = 1 # We will need to differentiate these patients

      # extract all patient data from EYE GAZE and XAMI MIMIC datasets
      # get a dictionary with the study ID, patient ID and image ID
      patient_data = self.extractIdentifiersEYEGAZE( metadata, indx, token, global_vars )
      self.extractEYEGAZEDataFromXAMI( patient_data, global_vars )

      # create a new patient and add it to the patients dictionary
      new_patient = patient.Patient( patient_data['PATIENT_KEY'], patient_data, "EYE GAZE")
      global_vars.insertPatientIntoPATIENTS_DIC( new_patient )


  def extractEYEGAZEDataFromXAMI(self, patient_data, global_vars : GlobalVars ):
    
    # keeping track of patients unique identifiers
    patient_folder = "patient_" + patient_data["PATIENT_ID"] 
    mimic_path = global_vars.getMIMIC_PATH()

    # saving XAMI MIMIC DATA PATHS:
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
    patient_data['STUDY_ID'] = "s" + str( metadata.loc[indx,'study_id'])
    patient_data['IMAGE_ID'] = "s" + str( metadata.loc[indx,'dicom_id'])
    patient_data['PATIENT_ID'] = "s" + str( metadata.loc[indx,'patient_id'])

    # update the key of the patient if the patient has more than one medical study
    patient_data['PATIENT_KEY'] =str( metadata.loc[indx,'patient_id']) + "_IMG" + str(token)
    if patient_data['PATIENT_KEY'] in global_vars.getPATIENTS_DIC().keys():
      token = token + 1
      patient_data['PATIENT_KEY'] = str(metadata.loc[indx,'patient_id']) + "_IMG" + str(token)
    
    return patient_data

  



      





      





    
    