from predict import predict
from train import train
import yaml


config = yaml.safe_load(open("config_hpo.yaml"))
best_score = -float("inf")
best_model = None
for alpha in config["alpha"]["values"]:
    model_config = config.copy()
    model_config["alpha"] = alpha
    model_config = {"user_option_values": model_config}
    # model_file = f"output/model_{alpha}.bin"
    model_file = "output/model.bin"
    train("input/train.csv", model_file, model_config)
    rmse_score = predict(model_file, "input/train.csv", "input/validation.csv", "output/predictions.csv")
    print("rmse:", rmse_score)
    if rmse_score > best_score:
        best_score = rmse_score
        best_model = model_file
print("best score", best_score)

#final prediction..
rmse_score = predict(best_model, "input/train.csv", "input/test.csv", "output/predictions.csv")
print("final test score:", rmse_score)