from dataprocessing.eyegaze import EyeGazeProcessor
from util.global_vars import GlobalVars
import pickle
import os

def load_XAMI_MIMIC_Dictionaries( gv :GlobalVars ):
    print("Loading dictionaries...")
    PATIENTS_DIC = load_dictionary( os.path.join(gv.getMIMIC_PATH(), "PATIENTS_DIC_EYEGAZE.pkl" ))
    gv.setPATIENTS_DIC( PATIENTS_DIC )

    IMG_TO_DIAGNOSIS = load_dictionary(  os.path.join(gv.getMIMIC_PATH(), "IMG_DIAGNOSIS_EYEGAZE.pkl")  )
    gv.setIMG_TO_DIAGNOSIS( IMG_TO_DIAGNOSIS )

    IMG_TO_PATIENT = load_dictionary(  os.path.join(gv.getMIMIC_PATH(), "IMG_PATIENT_EYEGAZE.pkl" ))
    gv.setIMG_TO_PATIENT(IMG_TO_PATIENT)

    stats_dict = load_dictionary(  os.path.join( gv.getMIMIC_PATH(), "GLOBAL_VARS.pkl" ))
    gv.setTOTAL_EYE_GAZE( stats_dict['TOTAL_EYE_GAZE'] )
    gv.setTOTAL_EYE_GAZE( stats_dict['TOTAL_EYE_GAZE'] )
    gv.setTOTAL_EYE_GAZE( stats_dict['TOTAL_EYE_GAZE'] )

def create_XAMI_MIMIC_Dictionaries(gv : GlobalVars):
    stats_dict = {}
    process = EyeGazeProcessor( gv )
    process.processEYE_GAZE( )

    # save processed patients
    save_dictionary( os.path.join(gv.getMIMIC_PATH(), "PATIENTS_DIC_EYEGAZE.pkl") , gv.getPATIENTS_DIC())
    save_dictionary( os.path.join(gv.getMIMIC_PATH(), "IMG_DIAGNOSIS_EYEGAZE.pkl"), gv.getIMG_TO_DIAGNOSIS())
    save_dictionary( os.path.join(gv.getMIMIC_PATH(), "IMG_PATIENT_EYEGAZE.pkl"), gv.getIMG_TO_PATIENT())
    
    # save global variables
    stats_dict['TOTAL_EYE_GAZE'] = gv.getTOTAL_EYE_GAZE()
    stats_dict['TOTAL_REFLACX'] = gv.getTOTAL_REFLACX()
    stats_dict['TOTAL_BOTH'] = gv.getTOTAL_BOTH()
    save_dictionary( os.path.join(gv.getMIMIC_PATH(), "GLOBAL_VARS.pkl") , stats_dict)

def getPatientInfo(patient_key : str, condition : str, global_vars : GlobalVars ):
    patient = global_vars.getPATIENTS_DIC()[ patient_key]
    patient_data = patient.getPatient_data()
    return patient_data[condition]

def save_dictionary( path, dictionary):
  dic_file = open( path, "wb")
  pickle.dump(dictionary, dic_file)
  dic_file.close()

def load_dictionary( path ):
  dic_file = open( path, "rb" )
  PATIENTS_DIC = pickle.load(dic_file)
  return PATIENTS_DIC