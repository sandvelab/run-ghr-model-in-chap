import argparse
import joblib
import pandas as pd
from sklearn.metrics import root_mean_squared_error


def predict(model_fn: str, historic_data: str, future_data: str, out_file: str):
    df = pd.read_csv(future_data)
    X = df[['rainfall', 'mean_temperature']]
    model = joblib.load(model_fn)
    y_pred = model.predict(X)
    df['sample_0'] = y_pred
    df.to_csv(out_file, index=False)
    # When the future CSV carries the target (HPO mode via isolated_hpo_run.py
    # against a labelled validation/test split), return -RMSE so the HPO loop
    # can rank candidates. chap eval's future CSV has no target column - return
    # None in that case so the prediction call still succeeds.
    if 'disease_cases' in df.columns:
        return -root_mean_squared_error(df['disease_cases'], y_pred)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict using the trained model.')

    parser.add_argument('model_fn', type=str, help='Path to the trained model file.')
    parser.add_argument('historic_data_fn', type=str, help='Path to the CSV file historic data (here ignored).')
    parser.add_argument('future_climatedata_fn', type=str, help='Path to the CSV file containing future climate data.')
    parser.add_argument('predictions_fn', type=str, help='Path to save the predictions CSV file.')
    parser.add_argument('model_config', type=str, help='Path to model configuration yaml.') # not used not sure why needed

    args = parser.parse_args()
    predict(args.model_fn, args.historic_data_fn, args.future_climatedata_fn, args.predictions_fn)