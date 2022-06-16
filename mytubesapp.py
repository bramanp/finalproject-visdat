#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource, DateRangeSlider
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral11, Turbo11, Set3_12
from bokeh.layouts import widgetbox, row, gridplot, column
from bokeh.models import Slider, Select


# In[26]:


# baca dataset
data = pd.read_csv("covid_19_indonesia_time_series_all.csv")
data.head()


# In[27]:


# memastikan kolom "Date" bertipe "datetime64"
data['Date'] = pd.to_datetime(data['Date'])  

# membuat kolom 'Date' menjadi index
data.set_index('Date', inplace=True)
data.head()


# In[28]:


# membuat list unique dari kolom 'Location'
location_list = pd.unique(data['Location']).tolist()
location_list


# In[29]:


# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=location_list, palette=Spectral11)


# In[30]:


# membuat ColumnDataSource
source = ColumnDataSource(data={
    'x' : data.index,
    'y' : data["New Cases"],
})


# In[31]:


# membuat figure plot
plot = figure(title='New Cases COVID-19', x_axis_label='Date', y_axis_label='New Cases',
           x_axis_type='datetime' ,plot_height=600, plot_width=1200)


# In[32]:


# membuat graph
plot.circle(x='x', y='y', source=source, fill_alpha=0.8)


# In[33]:


# fungsi update plot
def update_plot(attr, old, new):
    y = y_select.value
    y_kota = y_kota_select.value

    plot.yaxis.axis_label = y
    
    # new data
    if y_kota == "all":
        new_data = {
            'x'       : data.index,
            'y'       : data[y],    
        }
    else:
        data_kota = data.loc[(data["Location"] == y_kota)]
        new_data = {
            'x'       : data_kota.index,
            'y'       : data_kota[y],    
        }
    source.data = new_data


# In[34]:


# dropdown untuk y axis
# Kasus
y_select = Select(
    options=['New Cases', 'New Deaths', 'New Recovered', 'Total Cases', 'Total Recovered'],
    value='New Cases',
    title='Kasus list'
)

y_select.on_change('value', update_plot)

# pilih kota
location_list.insert(0, "all")
y_kota_select = Select(
    options= location_list,
    value='all',
    title='Kota list'
)

y_kota_select.on_change('value', update_plot)


# In[35]:


layout = row(column(y_kota_select, y_select), plot)
curdoc().add_root(layout)

