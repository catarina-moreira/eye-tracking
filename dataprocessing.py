

def get_global_disease( patient_Key, metadata ):
  chf = metadata['CHF'].values[0]
  pneumonia = metadata['pneumonia'].values[0]
  normal = metadata['Normal'].values[0]   

  PATIENTS_DIC[patient_Key]['DIAGNOSIS_GLOBAL'] = "Normal"
  if chf == 1:
    PATIENTS_DIC[patient_Key]['DIAGNOSIS_GLOBAL'] = "CHF"
  if pneumonia == 1:
    PATIENTS_DIC[patient_Key]['DIAGNOSIS_GLOBAL'] = "Pneumonia"

