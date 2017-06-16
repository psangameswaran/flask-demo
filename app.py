from flask import Flask, render_template, request
import pandas as pd
from bokeh.charts import Histogram
from bokeh.embed import components
import requests
import simplejson as json
import numpy as np
from bokeh.io import push_notebook, show, output_file,output_notebook,reset_output,save
from bokeh.plotting import figure
from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput, Dropdown
import datetime as dt
from bokeh.models import DatetimeTickFormatter


app = Flask(__name__)

# Load the Stock Data Set
#quandl.ApiConfig.api_key = 'J3DvHz2kKB97tvnzutbs'
r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=J3DvHz2kKB97tvnzutbs&date.gte=2017-06-13')
prepredata = r.json()
cols = ["ticker", "date", "open", "high", "low", "close", "volume", "ex-dividend", "split_ratio", "adj_open", "adj_high", "adj_low$

predata=pd.DataFrame(prepredata['datatable']['data'], columns = cols)
#predata = quandl.get_table('WIKI/PRICES', date = { 'gte': '2017-06-13' })
stock_names = [x for x in predata['ticker'].unique()]

# Create the main plot
def create_figure(stock):
        query = "%s%s" %("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=J3DvHz2kKB97tvnzutbs&date.gte=2017-05-$
        r = requests.get(query)
        prepdata=r.json()
        data=pd.DataFrame(prepdata['datatable']['data'],columns=cols)
        #data = quandl.get_table('WIKI/PRICES', ticker=stock, date = { 'gte': '2017-05-15' })
        data['date'] = data['date'].astype('datetime64[ns]')
        today = dt.date.today()
        monthago=today - pd.offsets.Day(29)
        data2=data[data['date']>monthago]
        x=data2['date'].dt.date
        y=data2['close']
        p = figure(title="Stock Ticker Price", plot_height=300, plot_width=600)
        r = p.line(x, y, color="#2222aa", line_width=3)
        p.xaxis.formatter=DatetimeTickFormatter(days=["%m/%d"])

        # Set the x axis label
        p.xaxis.axis_label = "Date"

        # Set the y axis label
        p.yaxis.axis_label = 'Closing Price'
        return p

# Index page
@app.route('/')
def index():
        # Determine the selected feature
        current_stock_name = request.args.get("s")
        if current_stock_name == None:
                current_stock_name = "A"

        # Create the plot
        plot = create_figure(current_stock_name)

        # Embed plot into HTML via Flask Render
        script, div = components(plot)
        return render_template("index.html", script=script, div=div,
                stock_names=stock_names,  current_stock_name=current_stock_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
        app.run(host='0.0.0.0')                         
       
