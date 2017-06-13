from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)

import quandl
quandl.ApiConfig.api_key = 'J3DvHz2kKB97tvnzutbs'
data = quandl.get_table('WIKI/PRICES', date = { 'gte': '2017-05-15' })

import simplejson as json
import pandas as pd

from ipywidgets import interact
import numpy as np

from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure
from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput
output_notebook()

data['date'] = data['date'].astype('datetime64[ns]')
import datetime as dt     
today = dt.date.today()
monthago=today - pd.offsets.Day(29)
data2=data[data['date']>monthago]
x=data2['date'].dt.date
a=data2['close']
y=a[data2['ticker']=='A']

p = figure(title="Stock Ticker Price", plot_height=300, plot_width=600)
r = p.line(x, y, color="#2222aa", line_width=3)
from bokeh.models import DatetimeTickFormatter
p.xaxis.formatter=DatetimeTickFormatter(days=["%m/%d"])

def update(Ticker):
    new_y=a[data2['ticker']==Ticker]
    r.data_source.data['y']=new_y
    push_notebook()

show(p,notebook_handle=True)

interact(update,Ticker=[x for x in data2['ticker'].unique()])
