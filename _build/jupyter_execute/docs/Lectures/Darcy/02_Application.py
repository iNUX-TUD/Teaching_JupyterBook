#!/usr/bin/env python
# coding: utf-8

# # Application of Darcy's Law
# 
# ## 1. Application to a column of porous media
# Watch the video about how Darcy's Law can describe the flow in porous media.

# In[1]:


get_ipython().run_cell_magic('HTML', '', '<iframe width="560" height="315" src="https://www.youtube.com/embed/KPmklXGd-18" allowfullscreen></iframe>\n')


# Now it is your turn to do the same experiment! Play around with the parameters to understand their role in Darcy's law. Also consider that you can change the composition of the porous medium. In the next section you will be asked questions to test your knowledge.

# In[9]:


# Import necessary packages

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import numpy as np
import json
from ipywidgets import *
from IPython.display import display,clear_output
import urllib.request


# In[10]:


# Define the language in the plot

# being supported are "english" or "german"
language = "english"


# In[11]:


# Import language
with urllib.request.urlopen("https://www.dropbox.com/s/citzs2zds2bihlh/test.txt?dl=1") as url:
    lang_dict = json.load(url)

if language=="english":
    ylabel = lang_dict["Druckpotential"] + " (m)"
elif language=="german":
    ylabel = "Druckpotential" + " (m)"
else:
    raise Exception(f"{language} is currently not a supported language!")


# In[6]:


# Define variables needed

material_dict= {
        "Sand":{
            "color":"gold",
            "k":1E-4
        },
        "Gravel":{
            "color":"gray",
            "k":1E-2
        },
        "Clay":{
            "color":"peru",
            "k":1E-6
        }
    }


# In[7]:


# Define functions needed

def plot_triangle(x, y, ax, stretch):
    """
    Plot a water triangle
    
    Keyword Arguments:
    x -- x postion of triangle tip (water table)
    y -- y position of triangle tip
    ax -- axes to plot on
    stetch -- height and half the base length of the symmetric triangle
    """
    tgl = [[x, y],[x - stretch, y + stretch],[x + stretch, y + stretch]]
    ax.add_patch(Polygon(tgl))
    ax.hlines(y, x - stretch, x + stretch)
    ax.hlines(y - stretch * 0.5, x - stretch * 0.66, x + stretch * 0.66)
    ax.hlines(y - stretch, x - stretch * 0.33, x + stretch * 0.33)
    

def plot_darcy_column(h1, h2, material):
    """
    Plot a Darcy column
    
    Keyword Arguments:
    h1 -- head inside column, m
    h2 -- head of outlet, m
    material -- material inside column. Defined by material_dict
    
    TODO: Avoid globaliszing variables to speak to observation plot
    """
    
    global q, h1_out, h2_out
    h1_out = h1
    h2_out = h2
    
    # Prepare plot
    fig = plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.get_xaxis().set_visible(False)
    ax.set_aspect("equal")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_ylabel(ylabel, fontsize=13)
    
    # Define lenghts in m
    column_height = 15
    column_width = 5
    sediment_height = 5
    distance_gauge_column = gauge_width = 0.9
    overlap_left = 0.5
    arrow_length_max = 2.
    arrow_width_max = .3
    
    # Define verticies
    p1 = (0, column_height)
    p2 = (column_width, column_height)
    p3 = (column_width, gauge_width)
    p4 = (column_width + distance_gauge_column, gauge_width)
    p5 = (column_width + distance_gauge_column, gauge_width + h2)
    p6 = (column_width + distance_gauge_column + gauge_width + overlap_left, gauge_width + h2)
    p7 = (column_width + distance_gauge_column + gauge_width + overlap_left, h2)
    p8 = (column_width + distance_gauge_column + gauge_width, h2)
    p9 = (column_width + distance_gauge_column + gauge_width, 0)
    p10 = (0,0)
    p11 = (column_width,0)
    
    # Plot material
    ax.add_patch(Rectangle((0,0), sediment_height, column_width,
                 color = material_dict[material]["color"]))
    
    # Plot water column
    ax.add_patch(Rectangle((0,sediment_height), column_width, h1 - sediment_height,
                 color = "skyblue", alpha=0.8))
    
    # Plot lengths
    shape = [p2, p3, p4, p5, p6, p7, p8, p9, p10, p1]
    x, y = zip(*shape)
    plt.plot(x, y, c="black")
    
    # add triangle
    stretch = column_width * 0.05
    x_dist = column_width / 2
    plot_triangle(x_dist, h1, ax, stretch)
    
    
    if h1 > h2:
        # Calculate discharge after Darcy
        q = material_dict[material]["k"] * (h1 - h2)
        q_max = material_dict[material]["k"] * column_height
        # Plot arrow for discharge
        arrow_length = arrow_length_max * q / q_max
        arrow_width = arrow_width_max * q / q_max
        plt.arrow(p6[0],
                 h2 + 0.5 * gauge_width, arrow_length, 0,
                 length_includes_head = True,
                 width = arrow_width)
        txt = "Q = " + str(round(q, 6)) + r" $\frac{m^3}{s}$"
        plt.text(p6[0] + arrow_length,p6[1], txt, fontsize=13)
        gauge = [p3, p4, p5, p6, p7, p8, p9, p11]
    else:
        p12 = (column_width+distance_gauge_column,h1)
        p13 = (column_width+distance_gauge_column+gauge_width,h1)
        plt.hlines(p12[1], p12[0],p13[0])
        x_dist = column_width + distance_gauge_column + gauge_width / 2
        plot_triangle(x_dist, h1, ax, stretch)
        gauge = [p3, p4,p12, p13,p9, p11]
    ax.add_patch(Polygon(gauge, color="skyblue", alpha=0.8))
    


# In[8]:


# Run interactive plot

interact(plot_darcy_column,
         h1 = widgets.BoundedFloatText(value=11, min=5, max=15, step=1, description='H1', disabled=False),
         h2 = widgets.BoundedFloatText(value=0, min=0, max=15, step=1, description='H2:', disabled=False),
         material = widgets.Dropdown(options=material_dict.keys(),value="Sand", description="Material"))


# In[ ]:




