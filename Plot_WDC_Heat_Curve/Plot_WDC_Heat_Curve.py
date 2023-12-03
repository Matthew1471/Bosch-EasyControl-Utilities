#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Bosch-EasyControl-Utilities <https://github.com/Matthew1471/Bosch-EasyControl-Utilities>
# Copyright (C) 2023 Matthew1471!
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Import our modules that we are using
import numpy
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.widgets import Slider, Button, RadioButtons

# Pre-defined Weather Dependent Control (WDC) default values.
heating_types = {
                 'Radiator': { 'default_start_point_curve': 20, 'default_end_point_curve':75, 'default_min_supply_temperature': 20, 'default_max_supply_temperature':90 },
                 'Convector': { 'default_start_point_curve': 20, 'default_end_point_curve':75, 'default_min_supply_temperature': 20, 'default_max_supply_temperature':90 },
                 'Underfloor': { 'default_start_point_curve': 20, 'default_end_point_curve':45, 'default_min_supply_temperature': 20, 'default_max_supply_temperature':45 }
                }

# Apply the Bosch EasyControl default values for a Radiator.
heating_type = heating_types['Radiator']

# Create the figure.
figure = plt.figure('Bosch EasyControl Weather Dependent Control (WDC) Simulator', figsize=(15,6))

# Allow some extra space for our widgets.
figure.subplots_adjust(left=0.15, bottom=0.25)

# The axes (or chart).
axes = figure.subplots()

# Annotate the axes.
axes.set_title('Bosch EasyControl Weather Dependent Control (WDC) Simulator')
axes.set_xlabel('Outside Temperature (oC)')
axes.set_ylabel('Flow Temperature (oC)')

# Default example temperature for summer setback.
default_example_summer_setback_threshold = 18

# Add the maximum, minimum flow temperature and summer setback lines.
line_minimum_flow_temperature = axes.axhline(y=heating_type['default_min_supply_temperature'], color='c', linestyle='dashed', label='_Minimum Flow Temperature')
line_maximum_flow_temperature = axes.axhline(y=heating_type['default_max_supply_temperature'], color='r', linestyle='dashed', label='_Maximum Flow Temperature')
line_summer_setback_threshold = axes.axvline(x=default_example_summer_setback_threshold, color='y', linestyle='dashed', label='_Summer Setback Threshold')

# Annotate the limit lines.
annotation_minimum_flow_temperature = axes.annotate('Minimum Flow Temperature', xy=(-10, heating_type['default_min_supply_temperature']), xytext=(-14.5, heating_type['default_min_supply_temperature'] + 1), color='c')
annotation_maximum_flow_temperature = axes.annotate('Maximum Flow Temperature', xy=(20, heating_type['default_max_supply_temperature']), xytext=(20, heating_type['default_max_supply_temperature'] + 1), color='r')
annotation_summer_setback_threshold = axes.annotate('Summer Setback Threshold', xy=(default_example_summer_setback_threshold, 0), xytext=(default_example_summer_setback_threshold - 0.5, 40), color='y', rotation=90)

# Create the vectors outside_temperatures (-10oC to 20oC) and basic_heat_curve (End Point Curve to Start Point Curve).
outside_temperatures = numpy.arange(-10, 20.01, 0.01)
basic_heat_curve = numpy.linspace(heating_type['default_end_point_curve'], heating_type['default_start_point_curve'], len(outside_temperatures))

# Plot the initial basic heat curve.
lines_basic_heat_curve, = axes.plot(outside_temperatures, basic_heat_curve, alpha=0.5, color='k', label='Basic', marker = 'D', markevery=[0,-1])

# Default example temperature for modelling by set point.
default_example_set_point = 20

# Calculate the initial adjusted by set point ( (Set Point – 20°C) x 3°C = Parallel Offset ) heat curve.
set_point_heat_curve = basic_heat_curve + ((default_example_set_point - 20) * 3)

# Apply the minimum and maximum flow temperature constraints to the initial adjusted by set point heat curve.
set_point_heat_curve = numpy.clip(set_point_heat_curve, heating_type['default_min_supply_temperature'], heating_type['default_max_supply_temperature'])

# Apply summer setback to the initial adjusted by set point heat curve.
set_point_heat_curve[outside_temperatures >= default_example_summer_setback_threshold] = 0

# Plot the initial adjusted by set point heat curve with flow limits applied.
lines_set_point_heat_curve, = axes.plot(outside_temperatures, set_point_heat_curve, color='b', label='Adjusted by Set Point', marker = 'D', markevery=[0,-1])

# Default room influence factor and example actual room temperature for modelling by room temperature.
default_room_influence_factor = 3
default_example_actual_room_temperature = 16

# Calculate the initial adjusted by room temperature ( (Set Point – Actual Room Temperature) x Room Influence Factor = Parallel Offset ) heat curve.
room_temperature_heat_curve = basic_heat_curve + ((default_example_set_point - default_example_actual_room_temperature) * default_room_influence_factor)

# Apply the minimum and maximum flow temperature constraints to the initial adjusted by room temperature heat curve.
room_temperature_heat_curve = numpy.clip(room_temperature_heat_curve, heating_type['default_min_supply_temperature'], heating_type['default_max_supply_temperature'])

# Apply summer setback to the initial adjusted by room temperature heat curve.
room_temperature_heat_curve[outside_temperatures >= default_example_summer_setback_threshold] = 0

# Plot the initial adjusted by room temperature heat curve with flow limits applied.
lines_room_temperature_heat_curve, = axes.plot(outside_temperatures, room_temperature_heat_curve, color='g', label='Adjusted by Room Temperature', marker = 'D', markevery=[0,-1])

# Annotate the plot.
annotation_basic_heat_curve_start_point = axes.annotate('Start\nPoint', xy=(outside_temperatures[-1], basic_heat_curve[-1]), xytext=(-10, -25), textcoords='offset points')
annotation_basic_heat_curve_end_point = axes.annotate('End\nPoint', xy=(outside_temperatures[0], basic_heat_curve[0]), xytext=(-10, -25), textcoords='offset points')

# Set the axes display to match the documentation.
axes.set_xlim(-15, 30)
plt.setp(axes.get_xticklabels()[0], visible=False)
plt.setp(axes.get_xticklabels()[-1], visible=False)

axes.set_ylim(0, 90)
plt.setp(axes.get_yticklabels()[0], visible=False)
plt.setp(axes.get_yticklabels()[-1], visible=False)

# Add a grid.
axes.grid(linestyle='dashed', alpha=0.4)

# Add a Legend.
legend = axes.legend(title='Heat Curve Legend:', title_fontproperties=font_manager.FontProperties(weight='bold'))

# This dictionary of room influence factors is used to map the string back to a value.
room_influence_factor_dictionary = {'None (0)':0, 'Low (1)':1, 'Medium (2)':2, 'High (3)':3}

# Create the radio room influence factor buttons (Rect = Left, Bottom, Width, Height).
radio_influence_left = 0.03
radio_influence_bottom = 0.7
radio_influence_width = 0.08
radio_influence_height = 0.15

axes_radio_room_influence_factor = figure.add_axes(rect=[radio_influence_left, radio_influence_bottom, radio_influence_width, radio_influence_height], facecolor='lightgoldenrodyellow')
radio_room_influence_factor = RadioButtons(ax=axes_radio_room_influence_factor, labels=list(room_influence_factor_dictionary.keys()), active=default_room_influence_factor, activecolor='g')
figure.text(radio_influence_left - 0.005, radio_influence_bottom + radio_influence_height + 0.01, 'Room Influence Factor')

# Create the horizontal sliders (Rect = Left, Bottom, Width, Height).
horizontal_slider_left = 0.25
horizontal_slider_width = 0.65
horizontal_slider_height = 0.03

axes_slider_start_point_curve = figure.add_axes(rect=[horizontal_slider_left, 0.15, horizontal_slider_width, horizontal_slider_height])
slider_start_point = Slider(ax=axes_slider_start_point_curve, label='Start Point Curve', valmin=20, valmax=45, valinit=heating_type['default_start_point_curve'], valstep=0.5, color='k', initcolor='none')

axes_slider_end_point_curve = figure.add_axes(rect=[horizontal_slider_left, 0.10, horizontal_slider_width, horizontal_slider_height])
slider_end_point = Slider(ax=axes_slider_end_point_curve, label='End Point Curve', valmin=40, valmax=90, valinit=heating_type['default_end_point_curve'], valstep=0.5, color='k', initcolor='none')

# Create the left vertical sliders (Rect = Left, Bottom, Width, Height).
vertical_slider_bottom = 0.25
vertical_slider_width = 0.02
vertical_slider_height = 0.35

axes_slider_example_set_point = figure.add_axes(rect=[0.03, vertical_slider_bottom, vertical_slider_width, vertical_slider_height])
slider_example_set_point = Slider(ax=axes_slider_example_set_point, label='Set Point', valmin=5, valmax=30, valinit=default_example_set_point, valstep=0.5, orientation='vertical', color='b', initcolor='none')

axes_slider_example_actual_room_temperature = figure.add_axes(rect=[0.08, vertical_slider_bottom, vertical_slider_width, vertical_slider_height])
slider_example_actual_room_temperature = Slider(ax=axes_slider_example_actual_room_temperature, label='Room Temp', valmin=5, valmax=30, valinit=default_example_actual_room_temperature, valstep=0.5, orientation='vertical', color='g', initcolor='none')

# Create the right vertical sliders (Rect = Left, Bottom, Width, Height).
axes_slider_minimum_flow_temperature = figure.add_axes(rect=[0.915, vertical_slider_bottom, vertical_slider_width, vertical_slider_height])
slider_minimum_flow_temperature = Slider(ax=axes_slider_minimum_flow_temperature, label='Min Temp', valmin=10, valmax=50, valinit=heating_type['default_min_supply_temperature'], valstep=0.5, orientation='vertical', color='c', initcolor='none')

axes_slider_maximum_flow_temperature = figure.add_axes(rect=[0.965, vertical_slider_bottom, vertical_slider_width, vertical_slider_height])
slider_maximum_flow_temperature = Slider(ax=axes_slider_maximum_flow_temperature, label='Max Temp', valmin=25, valmax=90, valinit=heating_type['default_max_supply_temperature'], valstep=0.5, orientation='vertical', color='r', initcolor='none')

axes_slider_summer_setback_threshold = figure.add_axes(rect=[0.94, radio_influence_bottom - 0.03, vertical_slider_width, vertical_slider_height / 2])
slider_summer_setback_threshold = Slider(ax=axes_slider_summer_setback_threshold, label='Summer Setback Temp', valmin=10, valmax=30, valinit=default_example_summer_setback_threshold, valstep=0.5, orientation='vertical', color='y', initcolor='none')

def update_heat_curves(val):
    # The minimum and maximum temperatures cannot overlap.
    if slider_start_point.val > slider_end_point.val:
        slider_end_point.eventson = False
        slider_end_point.set_val(slider_start_point.val)
        slider_end_point.eventson = True

    # The minimum and maximum flow temperatures cannot overlap.
    if slider_minimum_flow_temperature.val > slider_maximum_flow_temperature.val:
        slider_maximum_flow_temperature.eventson = False
        slider_maximum_flow_temperature.set_val(slider_minimum_flow_temperature.val)
        slider_maximum_flow_temperature.eventson = True

    # Calculate the basic (flow temperature) heat curve from the start point and end point sliders.
    basic_heat_curve = numpy.linspace(slider_end_point.val, slider_start_point.val, len(outside_temperatures))

    # Set the Y data range (flow temperature) for the basic heat curve.
    lines_basic_heat_curve.set_ydata(basic_heat_curve)

    # Move the minimum, maximum and summer setback lines.
    line_minimum_flow_temperature.set_ydata([slider_minimum_flow_temperature.val])
    line_maximum_flow_temperature.set_ydata([slider_maximum_flow_temperature.val])
    line_summer_setback_threshold.set_xdata([slider_summer_setback_threshold.val])

    # Move the minimum, maximum and summer setback line annotations.
    annotation_minimum_flow_temperature.set_y(slider_minimum_flow_temperature.val + 1)
    annotation_maximum_flow_temperature.set_y(slider_maximum_flow_temperature.val + 1)
    annotation_summer_setback_threshold.set_x(slider_summer_setback_threshold.val - 0.5)

    # Calculate the adjusted by set point ( (Set Point – 20°C) x 3°C = Parallel Offset ) heat curve.
    set_point_heat_curve = basic_heat_curve + ((slider_example_set_point.val - 20) * 3)

    # Apply the minimum and maximum flow temperature constraints to the set point heat curve.
    set_point_heat_curve = numpy.clip(set_point_heat_curve, slider_minimum_flow_temperature.val, slider_maximum_flow_temperature.val)

    # Apply summer setback to the adjusted by set point heat curve.
    set_point_heat_curve[outside_temperatures >= slider_summer_setback_threshold.val] = 0

    # Set the Y data range (flow temperature) for the adjusted by set point heat curve with flow limits applied.
    lines_set_point_heat_curve.set_ydata(set_point_heat_curve)

    # Update the basic heat curve annotations.
    annotation_basic_heat_curve_start_point.xy = (outside_temperatures[-1], slider_start_point.val)
    annotation_basic_heat_curve_end_point.xy = (outside_temperatures[0], slider_end_point.val)

    # Lookup the selected room_influence_factor from the currently selected ratio label.
    room_influence_factor = room_influence_factor_dictionary[radio_room_influence_factor.value_selected]

    # Is the selected room influence factor not "None (0)"?
    if room_influence_factor != 0:
        # Calculate the adjusted by room temperature ( (Set Point – Actual Room Temperature) x Room Influence Factor = Parallel Offset ) heat curve.
        room_temperature_heat_curve = basic_heat_curve + ((slider_example_set_point.val - slider_example_actual_room_temperature.val) * room_influence_factor)

        # Apply the minimum and maximum flow temperature constraints to the room temperature heat curve.
        room_temperature_heat_curve = numpy.clip(room_temperature_heat_curve, slider_minimum_flow_temperature.val, slider_maximum_flow_temperature.val)

        # Apply summer setback to the adjusted by room temperature heat curve.
        room_temperature_heat_curve[outside_temperatures >= slider_summer_setback_threshold.val] = 0

        # Set the Y data range (flow temperature) for the adjusted by room temperature heat curve with flow limits applied.
        lines_room_temperature_heat_curve.set_ydata(room_temperature_heat_curve)

        # Show the Example Actual Room Temperature slider.
        axes_slider_example_actual_room_temperature.set_visible(True)

        # Show the room temperature adjusted heat curve.
        lines_room_temperature_heat_curve.set_visible(True)
    else:
        # Hide the Example Actual Room Temperature slider as not applicable.
        axes_slider_example_actual_room_temperature.set_visible(False)

        # Hide the room temperature adjusted heat curve as not applicable.
        lines_room_temperature_heat_curve.set_visible(False)

    # Update the figure.
    figure.canvas.draw_idle()

# Set listeners on the widgets.
slider_start_point.on_changed(update_heat_curves)
slider_end_point.on_changed(update_heat_curves)
slider_minimum_flow_temperature.on_changed(update_heat_curves)
slider_maximum_flow_temperature.on_changed(update_heat_curves)
slider_summer_setback_threshold.on_changed(update_heat_curves)
slider_example_set_point.on_changed(update_heat_curves)
slider_example_actual_room_temperature.on_changed(update_heat_curves)
radio_room_influence_factor.on_clicked(update_heat_curves)

# Add a button to reset the variables.
axes_button_reset = figure.add_axes(rect=[0.8, 0.035, 0.1, 0.04])
button = Button(ax=axes_button_reset, label='Reset', hovercolor='0.975')

def reset(event):
    # Reset the sliders and radios back to their initial values.
    slider_start_point.reset()
    slider_end_point.reset()
    slider_example_set_point.reset()
    slider_example_actual_room_temperature.reset()
    slider_minimum_flow_temperature.reset()
    slider_maximum_flow_temperature.reset()
    slider_summer_setback_threshold.reset()
    radio_room_influence_factor.set_active(default_room_influence_factor)

# Set a listener on the button.
button.on_clicked(reset)

# Show the plot.
plt.show()