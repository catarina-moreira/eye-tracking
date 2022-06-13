import os

class MyGlobalVars:

    FLAG = False # this flag is used to re-index the full dataset or not. Set it to False to load pre-indexed data

    # path to github
    GDRIVE_MAIN = os.path.join( "C:", "Users", "cmore", "GitHub", "eye-tracking", "")

    # MIMIC-XAMI full dataset path: update to your own dataset path
    MIMIC_PATH = os.path.join("D", "GoogleDrive", "Datasets", "XAMI-MIMIC", "XAMI-MIMIC","")

    # EYE GAZE full dataset path
    EYE_GAZE_PATH = os.path.join(GDRIVE_MAIN, "Datasets", "Eye-Gaze", "")

    # Data structure where all the information per patient will be stored
    PATIENTS_DIC = {}

    IMG_TO_PATIENT = {}
    IMG_TO_DIAGNOSIS = {}

    # initialize other global variables
    TOTAL_EYEGAZE = 0
    TOTAL_REFLACX = 0
    TOTAL_BOTH = 0

def setup_global_vars_Colab( ):
    global TOTAL_EYEGAZE, TOTAL_REFLACX, TOTAL_BOTH, FLAG, PATIENTS_DIC, GDRIVE_MAIN, MIMIC_PATH, COLAB_MODE
    global EYEGAZE_HEALTHY_CXR_HEATMAP_PATH, EYEGAZE_CHF_CXR_HEATMAP_PATH, EYEGAZE_PNEUMONIA_CXR_HEATMAP_PATH
    global STATISTICS_EYEGAZE, EYE_GAZE_PATH, IMG_TO_PATIENT, IMG_TO_DIAGNOSIS

    FLAG = False 
    GDRIVE_MAIN = "/content/drive/MyDrive/"
   
    # MIMIC-XAMI full dataset path
    MIMIC_PATH = os.path.join(GDRIVE_MAIN, "Datasets", "XAMI-MIMIC", "XAMI-MIMIC","")

    # EYE GAZE full dataset path
    EYE_GAZE_PATH = os.path.join(GDRIVE_MAIN, "Datasets", "Eye-Gaze", "")

    # PYGAZE HEATMAPS PATHS
    EYEGAZE_HEALTHY_CXR_HEATMAP_PATH = os.path.join(GDRIVE_MAIN, "Colab Notebooks", "Eye Tracking", "outputs", "pygaze", "eye_gaze_dataset", "healthy", "")
    EYEGAZE_CHF_CXR_HEATMAP_PATH = os.path.join(GDRIVE_MAIN, "Colab Notebooks", "Eye Tracking", "outputs", "pygaze", "eye_gaze_dataset", "chf", "")
    EYEGAZE_PNEUMONIA_CXR_HEATMAP_PATH = os.path.join(GDRIVE_MAIN, "Colab Notebooks", "Eye Tracking", "outputs", "pygaze", "eye_gaze_dataset", "pneumonia", "")

    STATISTICS_EYEGAZE = os.path.join(GDRIVE_MAIN, "Colab Notebooks", "Eye Tracking", "outputs", "statistics", "eyegaze", "")
    # Data structure where all the information per patient will be stored
    PATIENTS_DIC = {}

    IMG_TO_PATIENT = {}
    IMG_TO_DIAGNOSIS = {}

    # initialize other global variables
    TOTAL_EYEGAZE = 0
    TOTAL_REFLACX = 0
    TOTAL_BOTH = 0

