
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import pygmt
import xarray as xr

class DrawVectorService:
    @staticmethod
    def draw_vector(date: str):
        """
        Controller for the draw vector
        """
        
        folder = "tethysapp/my_contour_map/public/data/output"
        vector_name = "Vector_" + date + ".d"
        tideland_name = "tideland_" + date + ".d"
        
        vector_path = os.path.join(folder, vector_name)
        tideland_path = os.path.join(folder, tideland_name)
        
        print(vector_path)
        print(tideland_path)
        
        if not (os.path.exists(vector_path)):
            return ''
        
        if not (os.path.exists(tideland_path)):
            return ''
        
        print("Exists")
        
        with open(vector_path, "r") as file:
            vector_data = file.read()
        
        vector_lines = vector_data.strip().split("\n")
        vector_coordinates = [list(map(float, line.split())) for line in vector_lines if line != ""]
        
        with open(tideland_path, "r") as file:
            tideland_data = file.read()
            
        tideland_lines = tideland_data.strip().split("\n")
        tideland_coordinates = [list(map(float, line.split())) for line in tideland_lines if line != ""]
        
        # Extract the range for x and y values from tideland_coordinates
        x_min, x_max = np.min(tideland_coordinates, axis=0)[0], np.max(tideland_coordinates, axis=0)[0]
        y_min, y_max = np.min(tideland_coordinates, axis=0)[1], np.max(tideland_coordinates, axis=0)[1]
        
        # Include vector coordinates in the range calculation
        x_min = min(x_min, np.min(vector_coordinates, axis=0)[0])
        x_max = max(x_max, np.max(vector_coordinates, axis=0)[2])
        y_min = min(y_min, np.min(vector_coordinates, axis=0)[1])
        y_max = max(y_max, np.max(vector_coordinates, axis=0)[3])

        print(x_min, x_max, y_min, y_max)

        # Vector plot
        fig, ax = plt.subplots()
        for x1, y1, x2, y2 in vector_coordinates:
            dx = x2 - x1
            dy = y2 - y1
            ax.arrow(x1, y1, dx, dy, head_width=15, head_length=25, fc='red', ec='red')

        # Tideland plot
        for x, y in tideland_coordinates:
            ax.plot(x, y, marker='o', linestyle='-', color='black')
            
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        
        image_path = "tethysapp/my_contour_map/public/images/vector_" + date + ".png"
        
        plt.savefig(image_path, dpi=400)
        
        return image_path
    
    
    @staticmethod
    def draw_contour(date: str):
        fig = pygmt.Figure()

        # HARD CODE VIETNAM REGION
        region = [102, 110.1, 8, 17.8]

        ## SET UP lat, long variables
        lat_min, lat_max = 8, 17.8
        lon_min, lon_max = 102, 110.1

        lat = np.arange(lat_min, lat_max, 0.2)
        lon = np.arange(lon_min, lon_max, 0.2)

        # Load Data File
        folder = "tethysapp/my_contour_map/public/data/output"
        salinity_name = "salinity_" + date + ".d"
        salinity_path = os.path.join(folder, salinity_name)
        
        if not (os.path.exists(salinity_path)):
            return ''
        
        with open(salinity_path, "r") as file:
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
        fig.colorbar(frame=["x+lSalinity DATA", "y+lm"])
        
        image_path = "tethysapp/my_contour_map/public/images/contour_map_" + date + ".png"
        
        fig.savefig(image_path, dpi=300, show=False)
        
        return image_path