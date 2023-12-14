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
    fig = pygmt.Figure()

    # HARD CODE VIETNAM REGION
    region = [102, 110.1, 8, 17.8]

    ## SET UP lat, long variables
    lat_min, lat_max = 8, 17.8
    lon_min, lon_max = 102, 110.1

    lat = np.arange(lat_min, lat_max, 0.2)
    lon = np.arange(lon_min, lon_max, 0.2)

    # Load Data File
    file_data = "tethysapp/my_contour_map/public/data_sample/data.d"
    with open(file_data, "r") as file:
        dataFile = [[float(num) for num in line.split()] for line in file]

    data = np.array(dataFile)
    # data = np.random.uniform(-5, 5, size=(len(lat), len(lon)))

    grid = xr.DataArray(
        data=data,
        dims=["lat", "lon"],
        coords={
            "lon": lon,
            "lat": lat,
        },
    )
    
    print(grid)

    ## SHOW DATA Contour
    fig.grdimage(
        grid=grid,
        cmap="viridis",
        projection="M12c",
    )
    fig.grdcontour(
        interval=250,
        grid=grid,
        limit=[-4000, -2000],
    )

    ## Show map line
    fig.coast(
        region=region,
        projection="M12c",
        borders="1/0.5p",
        shorelines="1/0.5p",
        frame="ag",
    )

    # Set color bar bottom
    fig.colorbar(frame=["x+lContour DATA", "y+lm"])
    
    image_path = "tethysapp/my_contour_map/public/images/contour_map.png"
    
    fig.savefig(image_path, dpi=300, show=False)
    
    context = {
        "image_path": image_path
    }
    
    return render(request, 'my_contour_map/contour_map.html', context)


@controller(url='my-contour-map/hydrodynamic-vector')
def hydrodynamic_vector_view(request):
    
    result_path = ""
    
    if (request.POST and 'visualize-button' in request.POST):
        dates_input = request.POST.get('dates-input')
        
        print('Visualize Data for: ', dates_input)
        
        result_path = DrawVectorService.draw_vector(dates_input)
    
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