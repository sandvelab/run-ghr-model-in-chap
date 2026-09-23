import yaml
from predict import predict
from train import train

model_config = yaml.safe_load(open("config.yaml"))
# model_config["alpha"] = model_config["alpha"]["values"][0]
train("input/train.csv", "output/model.bin", model_config)
# train("input/train.csv", "output/model.bin")
predict("output/model.bin", "input/train.csv", "input/test.csv", "output/predictions.csv")