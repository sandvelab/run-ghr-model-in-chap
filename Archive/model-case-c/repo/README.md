# Minimal model template example 
This document demonstrates a minimal example of how to write a CHAP-compatible forecasting model template. The example is written in Python, uses few variables without any lag and uses Scikit-learn's Ridge Regression with tunable hyperparameter alpha. It simply learns a linear regression from rain and temperature to disease cases, without considering any previous disease or climate data. It also assumes and works only with a single region. The model is not meant to accurately capture any interesting relations - the purpose is just to show how CHAP integration works in a simplest possible setting and how data flows when hpo is activated. This example supports running evaluate with or without hyperparameter optimization.

## Running the model without CHAP integration
Before getting a new model to work as part of CHAP, it can be useful to develop and debug it while running it directly a small dataset from file.

The example can be run in isolation (e.g. from the command line) without hpo using the file isolated_run.py:

```bash
uv run isolated_run.py
```
This file imitates how data is parsed in chap and sends the formated configuration data (from a file configuration.yaml) to "train", which trains a tuned model from an input file "train.csv" and stores the trained model in a file "model.bin". Then a call to "predict" uses the stored model to forecast future disease cases (to a file "predictions.csv") based on input data on future climate predictions (from a file test.csv). Note: The "historic_data" argument to predict can be any placeholder since it's never used by the linear model.     

The example can be run in isolation with hpo activated using the file isolated_hpo_run.py:
```bash 
uv run isolated_hpo_run.py
```
This file imitates how the hpo loop is done in chap. Here we send a list of configrations (from a file configuration_hpo.yaml) to "train" and in each loop one configration is picked. The tuned model is trained from an input file "train.csv" and evaluated on "validation.csv", and after the loop the model with the best rmse score is saved in the file "model.bin". Then a call to "predict" uses the stored model to forecast future disease cases (to a file "predictions.csv") based on input data on future climate predictions (from a file test.csv).

## Running the minimalist model as part of CHAP
To run the minimalist model in CHAP, we first define the model interface in an MLFlow-based yaml specification (in the file "MLproject", which defines:
```yaml
name: min_template_py_ex

entry_points:
  train:
    command: python train.py {train_data} {model} {model_config}
    parameters:
      train_data: str
      model: str
      model_config: str
  predict:
    command: python predict.py {model} {historic_data} {future_data} {out_file} {model_config}
    parameters:
      model: str
      historic_data: str
      future_data: str
      out_file: str
      model_config: str
uv_env: pyproject.toml
```
A pyproject.toml should be included in the model directory to specify the python version and dependencies. CHAP runs the entry point commands through `uv run`, which resolves and installs the environment on first use.

After you have installed chap-core (see here for installation instructions: https://github.com/dhis2-chap/chap-core), you can run this minimal template through CHAP as follows (remember to replace '/path/to/your/model/directory' and '/path/to/your/config/yaml/file' with your local path):
```bash
chap eval --model-name /path/to/your/model/directory --dataset-csv https://raw.githubusercontent.com/dhis2/climate-health-data/refs/heads/main/lao/chap_LAO_admin1_monthly.csv --output-file eval.nc --plot --model-configuration-yaml /path/to/your/config/yaml/file --run-config.ignore-environment --run-config.debug
```
