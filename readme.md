# Austin, Texas Traffic Predictions

I am predicting daily traffic in Austin based on  volumes at one intersection at Oltorf and S 1st street. 

## Model Documentation

I go into more detail on setting model parameters in [this PDF](https://github.com/Charlie-Henry/Traffic-Predict/blob/main/ATX%20Traffic%20Prediction.pdf)

### Files

- [ATX Traffic Prediction.ipynb](https://github.com/Charlie-Henry/Traffic-Predict/blob/main/ATX%20Traffic%20Prediction.ipynb) is where I find appropirate SARIMA model parameters.
- [traffic_notifications.py](https://github.com/Charlie-Henry/Traffic-Predict/blob/main/traffic_notifications.py) is where I take the best-fit model from above and tweet out the results along with a chart.

### Data source

This data is sourced from the Austin Open Data portal's [Camera Traffic Counts dataset.](https://data.austintexas.gov/Transportation-and-Mobility/Camera-Traffic-Counts/sh59-i6y9/data)

I've limited this analysis to the "OLTORF ST / 1ST ST" intersection as it has the most complete data.