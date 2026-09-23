import argparse
import yaml
import joblib
import pandas as pd
from sklearn.linear_model import Ridge

def train(dataset_path: str, model_path: str, model_configuration: dict[str, any]): # filname yaml
    print("model config:", model_configuration)
    df = pd.read_csv(dataset_path)
    features = ['rainfall', 'mean_temperature']
    X = df[features]
    Y = df['disease_cases']
    Y = Y.fillna(0)  # set NaNs to zero (not a good solution, just for the example to work)
    # chap eval writes an empty {} model_configuration_for_run.yaml when no
    # user_options are passed. Fall back to sklearn's Ridge default so the
    # model still runs in that case.
    print(model_configuration.get("user_option_values", {}).get("alpha", 1.0))
    alpha = float(model_configuration.get("user_option_values", {}).get("alpha", {}).get("values", 1.0))
    model = Ridge(alpha=alpha)
    model.fit(X, Y)
    print("Train - coefficients: ", list(zip(features, model.coef_)))
    joblib.dump(model, model_path) # can use MLflow to save info
    return model # not sure if needed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a minimalist forecasting model.')
    parser.add_argument('csv_fn', type=str, help='Path to the CSV file containing input data.') # order matters and required args
    parser.add_argument('model_fn', type=str, help='Path to save the trained model.')
    parser.add_argument('model_config', type=str, help='Path to model configuration yaml.')
    args = parser.parse_args()
    model_config = yaml.safe_load(open(args.model_config)) # should be a dict to train that's what chap does, discuss with GK and Knut again since they said pass yaml last time
    train(args.csv_fn, args.model_fn, model_config)