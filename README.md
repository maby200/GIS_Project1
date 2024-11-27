# Project 1

In this project, the 2018 Land Value for New Orleans data is downloaded in JSON-format. The JSON to Features tool offered by ArcGIS by default is no useful to convert this data to shapefile format. Because of that, a specific tool should be created.

## Methods
### Materials
1. The JSON-formatted Land Value for New Orleans.
2. Jupyter notebook, to explore the data structure.
3. Packages: Arcpy, json, os

> These steps are splitted in two main parts: The `loadJSONtoArcGIS` function creation, and the Python toolbox creation.

### Developing `loadJSONtoArcGIS`
1. The json data is opened using `with` statement.The JSON data structure is as follows:
```json
{
  "meta" : { 
    "view" : {
    "..." : "...",
    "columns" : [ {
        "id" : -1,
        "name" : "sid",
        "dataTypeName" : "meta_data",
        "fieldName" : ":sid",
        "position" : 0,
        "renderTypeName" : "meta_data",
        "format" : { },
        "flags" : [ "hidden" ]
      }, {
        "..." : "...",
      }
    }
  },
  "data" : [ 
    [ "row-69eh-dt2h-vwz3", "00000000-0000-0000-A344-B176ECD7FE9B", 0, 1628101573, null, 1628101573, null, "{ }", "MULTIPOLYGON (((-90.092842237961 29.9693768329, ... ))),"101", "220710050002", "C", "3085170.5967876972", "7251.2480743083825"],
    [...]
  ]
}  
```
- After reviewing the JSON structure it is clear that the column names (fields) can be found following the path: `meta`->`view`->`columns`. Also, the values are in the `data` section inside the JSON.
- The aim is to create a shapefile with all the polygons. For that we should append the polygon that belongs to each row.
2. Using the `arcpy.FromWKT()` function the new Polygon is appended at the end of each row inside `data`.
3. A new empty shapefile is created using the `arcpy.management.CreateFeatureClass` function.
Given that the default fields in a shapefile created using the previous function are FID, Shape, and Id, some changes need to be done in the JSON field names:
    - Both of them are `ID` and `id`, they will be change to `uid` and `uid2`.
    - It is worth noting that some fields has space inside their names.
    - Also the maximum length of a fieldname is 10, condition that is not met here.
4. After making those corrections, all the fields are inserted in the empty shapefile.
5. Using the `arcpy.da.InsertCursor` functio is used to insert data in the shapefile.

### Python Toolbox
- To create a Toolbox, right click on the Project Toolboxes, then click on new Python Toolbox.
  ![](/img/createPyToolbox.png)
  > It is important that this toolbox have to be created inside the same folder where the previous python script is.
  
- Then, the code editor will open and the following changes have to be done:
  - Import the developed function:
  ```python
  from loadJSONtoArcGIS import loadJSONtoArcGIS
  ```
  - Modify the `getParameterInfo` function:
  ```python
  def getParameterInfo(self):
        """Define the tool parameters."""
        param_ws = arcpy.Parameter(
            name='worspace',
            displayName='Workspace',
            direction='Input',
            datatype='DEWorkspace',
            parameterType='Required'
        )
        param_json = arcpy.Parameter(
            name='jsonPath',
            displayName='JSON Path',
            direction='Input',
            datatype='DEFile',
            parameterType='Required'
        )
        param_out = arcpy.Parameter(
            name='output',
            displayName='Output Shapefile',
            direction='Output',
            datatype='GPString',
            parameterType='Required'
        )
        param_subfolder = arcpy.Parameter(
            name='output_subfolder',
            displayName='Output subfolder',
            direction='Input',
            datatype='GPString',
            parameterType='Optional'
        )
        params = [param_ws,param_json,param_subfolder,param_out]
        return params
  ```
  - Also, the default `excecute` method need to be modified:
  ```python
   def execute(self, parameters, messages):
        """The source code of the tool."""
        workspace = parameters[0].valueAsText
        json_file = parameters[1].valueAsText
        subfolder = parameters[2].valueAsText
        output_path = parameters[3].valueAsText
        
        loadJSONtoArcGIS(workspace=workspace,
                         json_path=json_file,
                         fc_name=output_path,
                         output_shp_folder=subfolder
                         )
        return
  ```
This is how the python toolbox should be seen:
![](/img/finalGUI.png)