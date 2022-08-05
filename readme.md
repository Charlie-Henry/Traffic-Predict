# Austin, Texas Traffic Predictions

I am predicting daily traffic in Austin based on  volumes at one intersection at Oltorf and S 1st street. 

## Model Documentation

I go into more detail on setting model parameters in [this PDF](https://github.com/Charlie-Henry/Traffic-Predict/blob/main/ATX%20Traffic%20Prediction.pdf)

### Files

- [ATX Traffic Prediction.ipynb](https://github.com/Charlie-Henry/Traffic-Predict/blob/main/ATX%20Traffic%20Prediction.ipynb) is where I find appropirate SARIMA model parameters.
- [traffic_notifications.py](https://github.com/Charlie-Henry/Traffic-Predict/blob/main/traffic_notifications.py) is where I take the best-fit model from above and tweet out the results along with a chart.