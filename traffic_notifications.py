from datetime import date
import os

from dotenv import load_dotenv
import statsmodels.api as sm
import pandas as pd
import tweepy
import plotly.graph_objects as go

load_dotenv("twitter.env")

TW_API_KEY = os.getenv("TW_API_KEY")
TW_API_Key_Secret = os.getenv("TW_API_Key_Secret")
TW_ACCESS_TOKEN = os.getenv("TW_ACCESS_TOKEN")
TW_ACCESS_TOKEN_SECRET = os.getenv("TW_ACCESS_TOKEN_SECRET")

DATA_URL = "https://data.austintexas.gov/resource/sh59-i6y9.csv?$select=sum(volume),date_trunc_ymd(read_date)%20as%20date&atd_device_id=7341&$group=date&$order=date%20DESC&$limit=10000"
ARMA_PARAMS = (0,1,2)
SEASONAL_PARAMS = (0,2,2,7)

def clean_data(df):
	df.index = pd.DatetimeIndex(df.index)
	all_days = pd.date_range(df.index.min(), df.index.max(), freq='D')
	df = df.reindex(all_days)
	y = df[['sum_volume']]
	y['sum_volume'] = y['sum_volume'].fillna(0)

	return y

def traffic_model(y):

	mod = sm.tsa.statespace.SARIMAX(y,order=ARMA_PARAMS,seasonal_order=SEASONAL_PARAMS,enforce_stationarity=False,enforce_invertibility=False)
	results = mod.fit(disp=0)
	fcast = results.get_forecast(steps=21).summary_frame()
	today_cast = fcast.loc[date.strftime(date.today(),format="%Y-%m-%d")]

	return today_cast



def twitter_connection():
	twitter_auth_keys = {
		"consumer_key"        : TW_API_KEY,
		"consumer_secret"     : TW_API_Key_Secret,
		"access_token"        : TW_ACCESS_TOKEN,
		"access_token_secret" : TW_ACCESS_TOKEN_SECRET
	}

	auth = tweepy.OAuthHandler(
		twitter_auth_keys['consumer_key'],
		twitter_auth_keys['consumer_secret']
		)
	auth.set_access_token(
		twitter_auth_keys['access_token'],
		twitter_auth_keys['access_token_secret']
		)
	api = tweepy.API(auth)
	
	return api

def forecast_plot(today_val,y):
	lowest = y["sum_volume"].median()-(2*y["sum_volume"].std())
	highest = y["sum_volume"].median()+(2*y["sum_volume"].std())

	v_low =  y["sum_volume"].median()-(1*y["sum_volume"].std())
	v_high =  y["sum_volume"].median()+(1*y["sum_volume"].std())

	low =  y["sum_volume"].median()-(.5*y["sum_volume"].std())
	high =  y["sum_volume"].median()+(.5*y["sum_volume"].std())

	if today_val <=  v_low:
	    title_text = "Very low traffic expected today"
	    tweet = "Austin's traffic is expected to be very low today."

	elif today_val <=  low:
	    title_text = "Relatively low traffic expected today"
	    tweet = "Austin's traffic is expected to be relatively low today."

	elif (today_val >  low and today_val <= high):
	    title_text = "Relatively normal traffic expected today"
	    tweet = "Austin's traffic is expected to be normal today."
	    
	elif today_val > high:
	    title_text = "Relatively busy traffic expected today"
	    tweet = "Austin's traffic is expected to be relatively busy today."
	    
	elif today_val > high:
	    title_text = "Very busy traffic expected today"
	    tweet = "Austin's traffic is expected to be very busy today."

	fig = go.Figure(go.Indicator(
	    mode = "gauge",
	    value = today_val,
	    domain = {'x': [0, 1], 'y': [0, 1]},
	    title = {'text': title_text},
	    gauge={
	        'axis': {'range':[lowest,highest],'visible': False},
	        'bar': {'color': "black"},
	        'steps': [
	            {'range':[lowest,v_low], 'color':'#1a9641'},
	            {'range':[v_low,low], 'color':'#a6d96a'},
	            {'range':[low,high], 'color':'#ffffbf'},
	            {'range':[high,v_high], 'color':'#fdae61'},
	            {'range':[v_high,highest], 'color':'#d7191c'},
	        ],
    }))
	fig.write_image("traffic_plot.png")

	return tweet



def main():
	tw_api = twitter_connection()

	df = pd.read_csv(DATA_URL,index_col=1)
	y = clean_data(df)
	today_cast = traffic_model(y)

	tweet = forecast_plot(today_cast['mean'],y)

	media = tw_api.media_upload("traffic_plot.png")
	post_result = tw_api.update_status(status=tweet, media_ids=[media.media_id])


if __name__ == "__main__":
	main()





