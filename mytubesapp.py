#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource, DateRangeSlider
from bokeh.models import CategoricalColorMapper
from bokeh.layouts import widgetbox, row, gridplot, column
from bokeh.models import Slider, Select


# baca dataset, sumber:(https://www.kaggle.com/datasets/hendratno/covid19-indonesia)
data = pd.read_csv("covid_19_indonesia_time_series_all.csv")
data.head()

# memastikan kolom "Date" bertipe "datetime64"
data['Date'] = pd.to_datetime(data['Date'])  

# membuat kolom 'Date' menjadi index
data.set_index('Date', inplace=True)
data.head()

# membuat list unique dari kolom 'Location'
location_list = pd.unique(data['Location']).tolist()

# membuat ColumnDataSource
kota_awal = data.loc[(data["Location"] == "Indonesia")]
source = ColumnDataSource(data={
    'x' : kota_awal.index,
    'y' : kota_awal["New Cases"],
    'location' : kota_awal["Location"]
})

# membuat figure plot
plot = figure(title='Visualisasi Data COVID-19 Indonesia (3/1/2020 - 12/3/2021)', x_axis_label='Date', y_axis_label='New Cases',
           x_axis_type='datetime' ,plot_height=600, plot_width=1200)

# membuat graph
plot.line(x='x', y='y', source=source, line_alpha=0.8, legend='location')

# set legend
plot.legend.location = 'bottom_left'

# fungsi update plot
def update_plot(attr, old, new):
    y = y_select.value
    y_kota = y_kota_select.value

    plot.yaxis.axis_label = y
    
    # new data
    data_kota = data.loc[(data["Location"] == y_kota)]
    new_data = {
        'x'       : data_kota.index,
        'y'       : data_kota[y],
        'location': data_kota["Location"]
    }
    
    source.data = new_data

# dropdown untuk y axis
# Kasus
y_select = Select(
    options=['New Cases', 'New Deaths', 'New Recovered', 'Total Cases', 'Total Recovered'],
    value='New Cases',
    title='Kasus list'
)

y_select.on_change('value', update_plot)

# pilih kota
y_kota_select = Select(
    options= location_list,
    value='Indonesia',
    title='Kota list'
)

y_kota_select.on_change('value', update_plot)

layout = row(column(y_kota_select, y_select), plot)
curdoc().add_root(layout)
