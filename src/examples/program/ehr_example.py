""" Synthea Synthetic Electronic Health Record. """

def run(data_folder, **kwargs):

    # Load the libraries.
    pd = kwargs.get('pandas')

    # Load the data / policies
    patients = pd.read_csv(data_folder + "patients/data.csv")
    conditions = pd.read_csv(data_folder + "conditions/data.csv")

    # Merge
    ehr = pd.merge(patients, conditions, left_on="ID", right_on="ID")
    print('Merged policy: ' + str(ehr.policy))

    # Filter
    ehr = ehr[ehr.CONSENT == 'Y']
    ehr = ehr[ehr.DESCRIPTION == 'ViralSinusitisDisorder']
    ehr = ehr[ehr.GENDER == 'M']
    ehr = ehr[ehr.AGE >= 18]

    # Aggregate
    return ehr.groupby(by="RACE").count()
