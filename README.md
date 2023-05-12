# Ontario-Fire-Hydrants
The project is to identify the nearest five fire hydrants in proximity to any given location within the Ontario Province.

Insurance companies can utilize the distance to a fire hydrant as a criterion in determining insurance premiums. Properties situated in close proximity to a fire hydrant may be deemed as lower risk for fire-related incidents, resulting in lower insurance premiums for such properties.

## Dataset
Data for the project is collected from various government websites for different cities.

## UI Interface
The user interface (UI) leverages Google Maps integrated within the Flask framework using Google Maps API. The UI enables users to input an address and visualize the nearest hydrants on the map. The UI logic transforms the location/address into coordinates on the earth's surface.

## Backend
The backend employs a MySQL database to store data, and the Python code interacts with the database through MySQL connector to retrieve the coordinates of nearby hydrants by calculating the Haversine distance between the points. Subsequently, these hydrant coordinates are communicated to an HTML page to be plotted on the map.
