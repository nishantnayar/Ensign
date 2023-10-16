from datetime import date, datetime, timedelta
import pytz
import pandas as pd
import os
import matplotlib.pyplot as plt





from pandas import DataFrame




# load_dotenv()

def datetoday():
    # Get the latest date
    # helps to only load the delta records and not the entire history
    return date.today()


def datetoday1():
    if date.today().weekday() == 0:
        return date.today() - timedelta(3)
    elif date.today().weekday() == 6:
        return date.today() - timedelta(2)
    else:
        return date.today() - timedelta(1)


def start_date(df):
    return (df.index.max() + timedelta(1)).date()







# MACD calculation
# Moving Average Convergence Divergence
# https://www.investopedia.com/terms/m/macd.asp
# https://medium.com/python-in-plain-english/plot-stock-chart-using-mplfinance-in-python-9286fc69689

# Add MACD as subplot
def macd_fn(df, window_slow, window_fast, window_signal):
    macd: DataFrame = pd.DataFrame()
    macd['ema_slow'] = df['Close'].ewm(span=window_slow).mean()
    macd['ema_fast'] = df['Close'].ewm(span=window_fast).mean()
    macd['macd'] = macd['ema_slow'] - macd['ema_fast']
    macd['signal'] = macd['macd'].ewm(span=window_signal).mean()
    macd['diff'] = macd['macd'] - macd['signal']
    macd['bar_positive'] = macd['diff'].map(lambda x: x if x > 0 else 0)
    macd['bar_negative'] = macd['diff'].map(lambda x: x if x < 0 else 0)
    return macd


# stochastic oscillator Indicator
# https://www.investopedia.com/terms/s/stochasticoscillator.asp

def stochastic_fn(df, window, smooth_window):
    stochastic = pd.DataFrame()
    stochastic['%K'] = ((df['Close'] - df['Low'].rolling(window).min())
                        / (df['High'].rolling(window).max() - df['Low'].rolling(window).min())) * 100
    stochastic['%D'] = stochastic['%K'].rolling(smooth_window).mean()
    stochastic['%SD'] = stochastic['%D'].rolling(smooth_window).mean()
    stochastic['UL'] = 80
    stochastic['DL'] = 20
    return stochastic


# Saving Figures
# Where to save the figures
PROJECT_ROOT_DIR = "."
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images")
os.makedirs(IMAGES_PATH, exist_ok=True)


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    # logging.info('Saving figure %s', fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution, transparent=True)


def pred_color(c):
    enmax_palette = ["#800000", "#767676", "#D6D6CE", "#350E20",
                     "#FFA319", "#C16622", "#8F3931", "#8A9045",
                     "#58593F", "#155F83", "#000000"]
    color_codes_wanted = ['maroon', 'darkgray', 'lightgray', 'violet',
                          'yellow', 'orange', 'red', 'lightgreen',
                          'darkgreen', 'blue', 'black']

    return enmax_palette[color_codes_wanted.index(c)]


# This is common function to calcuate the Interquartile range
def outlier_lower_iqr(col_name, th1=0.25, th3=0.75):
    quartile1 = X[col_name].quantile(th1)
    quartile3 = X[col_name].quantile(th3)
    iqr = quartile3 - quartile1
    lower_limit = quartile1 - 1.5 * iqr
    return lower_limit


def outlier_upper_iqr(col_name, th1=0.25, th3=0.75):
    quartile1 = X[col_name].quantile(th1)
    quartile3 = X[col_name].quantile(th3)
    iqr = quartile3 - quartile1
    upper_limit = quartile3 + 1.5 * iqr
    return upper_limit



