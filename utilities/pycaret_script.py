import pandas as pd
from pycaret.regression import setup, models, compare_models, get_metrics, predict_model,save_model, load_model
from pycaret.regression import RegressionExperiment


from utilities.read_process_data_utility import ( 
    resample_and_aggregate, get_session_directory, ensure_session_id, )

session_dir = get_session_directory()  # Use session-specific directory


def run_pycaret_script(independent_col, dependent_col):
    filename = "data_for_pycaret.csv"
    file_path = session_dir / filename

    df = pd.read_csv(file_path)

    s = RegressionExperiment()
    s.setup(df, target = independent_col, session_id = 123)
    best = s.compare_models()

    print(best)

    new_df = df[independent_col]
    s.predict_model(best)
    predictions = s.predict_model(best, data=new_df)

    s.save_model(best, 'my_best_pipeline_two')
    loaded_model = s.load_model('my_best_pipeline')
    print(loaded_model)

    return predictions
