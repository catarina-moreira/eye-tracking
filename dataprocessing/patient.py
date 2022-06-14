class Patient:

    # class that describes what is a patient
    # a patient is an object with the following attributes
    # - patient_key: which corresponds to MIMIC's study ID
    # - patient_data: a dictionary with the patients' details extracted from MIMIC
    # - data_source: which dataset did the patient come from: REFLACX, EYE GAZE or BOTH
    def __init__( self, patient_key, patient_data, patient_source ):

        self.patient_key = patient_key
        self.patient_data = patient_data
        self.patient_source = patient_source
    
    

