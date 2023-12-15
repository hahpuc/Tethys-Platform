from datetime import date
from django.shortcuts import render
from tethys_sdk.routing import controller
from tethys_sdk.gizmos import Button

from tethys_sdk.gizmos import (
    SelectInput
)

import pygmt
import numpy as np
import xarray as xr

from .services.draw_vector import DrawVectorService

@controller
def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='save',
        style='success',
        attributes={
            'data-bs-toggle':'tooltip',
            'data-bs-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='pen',
        style='warning',
        attributes={
            'data-bs-toggle':'tooltip',
            'data-bs-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='trash',
        style='danger',
        attributes={
            'data-bs-toggle':'tooltip',
            'data-bs-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-bs-toggle':'tooltip',
            'data-bs-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-bs-toggle':'tooltip',
            'data-bs-placement':'top',
            'title':'Next'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'my_contour_map/home.html', context)

@controller(url='my-contour-map/contour-view')
def contour_view(request):
    
    image_path = ""
    
    if (request.POST and 'visualize-button' in request.POST):
        dates_input = request.POST.get('dates-input')
        
        print('Visualize Salinity Data for: ', dates_input)
        
        DrawVectorService.draw_contour(dates_input)
        
        image_path = "contour_map_" + dates_input + ".png"
        
    
    dates_input = SelectInput(
        display_text='Dates',
        name='dates-input',
        multiple=False,
        options=[(date, date) for date in ['201001021300', '201001021500', '201001022000', '201001022400',  '201001030300']],
        error=None,
    )
    
    
    visualize_button = Button(
        display_text='Visualize',
        name='visualize-button',
        style='success',
        submit=True,
        attributes={
            'form': 'load-data-form'
        }
    )
    
    context = {
        'dates_input': dates_input,
        'visualize_button': visualize_button,
        "image_path": image_path
    }
    
    return render(request, 'my_contour_map/contour_map.html', context)


@controller(url='my-contour-map/hydrodynamic-vector')
def hydrodynamic_vector_view(request):
    
    result_path = ""
    
    if (request.POST and 'visualize-button' in request.POST):
        dates_input = request.POST.get('dates-input')
        
        print('Visualize Vector Data for: ', dates_input)
        
        DrawVectorService.draw_vector(dates_input)
        
        result_path = "vector_" + dates_input + ".png"
        
    
    dates_input = SelectInput(
        display_text='Dates',
        name='dates-input',
        multiple=False,
        options=[(date, date) for date in ['201001021300', '201001021400', '201001022000', '201001022400',  '201001030300']],
        error=None,
    )
    
    
    visualize_button = Button(
        display_text='Visualize',
        name='visualize-button',
        style='success',
        submit=True,
        attributes={
            'form': 'load-data-form'
        }
    )
    
    context = {
        'dates_input': dates_input,
        'visualize_button': visualize_button,
        'result_path': result_path
    }
    
    return render(request, 'my_contour_map/hydrodynamic_vector.html', context)