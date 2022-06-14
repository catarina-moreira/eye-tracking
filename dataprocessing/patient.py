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

    # getters 
    def getPatient_key(self):
        return self.patient_key
    
    def getPatient_data(self):
        return self.patient_data
    
    def getPatient_source(self):
        return self.getPatient_source
    
    # setters
    def setPatient_key(self, newKey ):
        self.patient_key = newKey
    
    def setPatient_data(self, newData):
        self.patient_data = newData
    
    def setPatient_source(self, newSource):
        self.patient_source
    


    


    

    


