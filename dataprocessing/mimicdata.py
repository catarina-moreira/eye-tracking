import os
from urllib.request import CacheFTPHandler
import pandas as pd
from util.global_vars import GlobalVars
from dataprocessing import patient
import numpy as np

class MIMICDataProcessor:

  def __init__( self, global_vars : GlobalVars ):
    self.global_vars = global_vars
  
  def getGlobalVars(self):
    return self.global_vars

  def findPatientsInBothDatasets(self):
    patients_both = []
    global_vars = self.getGlobalVars()
    PATIENTS_DIC = global_vars.getPATIENTS_DIC()

    # get the patients mastersheet
    df_reflacx = pd.read_csv( global_vars.getREFLACX_XAMI_METADATA() )

    for dicom_id in np.unique(df_reflacx['dicom_id'].values):
      for patient_key in PATIENTS_DIC.keys():
        
        patient = global_vars.getPATIENTS_DIC()[ patient_key]
        patient_data = patient.getPatient_data()
        if dicom_id !=patient_data['IMAGE_ID']:
          continue
        
        print("FOUND PATIENT: " + patient_key + " with DICOM " + dicom_id)
        self.global_vars.increment_BOTH()
        patients_both.append( patient_key )

        # get all studies performed over this X-Ray image
        radiologist = {}
        study_df = df_reflacx[ df_reflacx['dicom_id'] == dicom_id ]
        for indx in range(0, study_df.shape[0]):
          temp_res  = {}
          study_id = study_df.loc[indx,"id"]
          patient_folder = os.path.join(global_vars.getMIMIC_PATH(), "patient_" + patient_key.split("_")[0], "")
          temp_res['REFLACX_PATH_' + str(indx)] =  os.path.join( patient_folder, "REFLACX", study_id, "")
          
          temp_res['REFLACX_FIXATIONS_' + str(indx)] = os.path.join( temp_res['REFLACX_PATH_' + str(indx)], "fixations.csv"  )
          temp_res['REFLACX_GAZE_' + str(indx)] = os.path.join( temp_res['REFLACX_PATH_' + str(indx)], "gaze.csv"  )

          temp_res['REFLACX_ELLIPSES_' + str(indx)] = os.path.join( temp_res['REFLACX_PATH_' + str(indx)], "anomaly_location_ellipses.csv"  )
          temp_res['REFLACX_TRANSCRIPT_' + str(indx)] = os.path.join( temp_res['REFLACX_PATH_' + str(indx)], "transcription.txt")
          temp_res['REFLACX_TRANSCRIPT_TIMESTAMPS_' + str(indx)] = os.path.join( temp_res['REFLACX_PATH_' + str(indx)], "timestamps_transcription.CSV")

          radiologist['RADIOLOGIST_' + str(indx)] = temp_res
        
        patient_data['BOTH?'] = True
        patient_data['REFLACX'] = radiologist

        print("PATIENT: " + patient_key + "\tDICOM: " + dicom_id)
      else:
        patient_data['BOTH?'] = False

    return patients_both



  

