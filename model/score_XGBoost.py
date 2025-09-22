import math
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

import settings

with open(Path(settings.pickle_path) / "XGBoost.pickle", "rb") as pickle_model:
    model = pd.read_pickle(pickle_model)

def score(LOAN, MORTDUE, VALUE, YOJ, DEROG, DELINQ, CLAGE, NINQ, CLNO, DEBTINC, REASON_HomeImp, JOB_Office, JOB_Other, JOB_ProfExe, JOB_Sales, JOB_Self):
    "Output: EM_CLASSIFICATION, EM_EVENTPROBABILITY"

    try:
        global model
    except NameError:
        with open(Path(settings.pickle_path) / "XGBoost.pickle", "rb") as pickle_model:
            model = pd.read_pickle(pickle_model)


    index=None
    if not isinstance(LOAN, pd.Series):
        index=[0]
    input_array = pd.DataFrame(
        {"LOAN": LOAN, "MORTDUE": MORTDUE, "VALUE": VALUE, "YOJ": YOJ, "DEROG": DEROG,
        "DELINQ": DELINQ, "CLAGE": CLAGE, "NINQ": NINQ, "CLNO": CLNO, "DEBTINC":
        DEBTINC, "REASON_HomeImp": REASON_HomeImp, "JOB_Office": JOB_Office,
        "JOB_Other": JOB_Other, "JOB_ProfExe": JOB_ProfExe, "JOB_Sales": JOB_Sales,
        "JOB_Self": JOB_Self}, index=index
    )
    input_array = impute_missing_values(input_array)
    prediction = model.predict_proba(input_array).tolist()

    # Check for numpy values and convert to a CAS readable representation
    if isinstance(prediction, np.ndarray):
        prediction = prediction.tolist()

    if input_array.shape[0] == 1:
        if prediction[0][1] > 0.5:
            EM_CLASSIFICATION = "1"
        else:
            EM_CLASSIFICATION = "0"
        return EM_CLASSIFICATION, prediction[0][1]
    else:
        df = pd.DataFrame(prediction)
        proba = df[1]
        classifications = np.where(df[1] > 0.5, '1', '0')
        return pd.DataFrame({'EM_CLASSIFICATION': classifications, 'EM_EVENTPROBABILITY': proba})

def impute_missing_values(data):
    impute_values = \
        {'MORTDUE': np.float64(73760.817199559), 'CLNO': np.float64(21.29609620076682),
        'NINQ': np.float64(1.1860550458715597), 'DEBTINC':
        np.float64(33.779915348721126), 'LOAN': np.float64(18607.96979865772), 'YOJ':
        np.float64(8.922268135904499), 'VALUE': np.float64(101776.04874145007), 'CLAGE':
        np.float64(179.76627518656605), 'DELINQ': np.float64(0.4494423791821561),
        'DEROG': np.float64(0.2545696877380046), 'REASON_HomeImp': np.int64(0),
        'JOB_Office': np.int64(0), 'JOB_Other': np.int64(0), 'JOB_ProfExe': np.int64(0),
        'JOB_Sales': np.int64(0), 'JOB_Self': np.int64(0)}
    return data.replace('           .', np.nan).fillna(impute_values).apply(pd.to_numeric, errors='ignore')
