# -*- coding: utf-8 -*-

import arcpy
from loadJSONtoArcGIS import loadJSONtoArcGIS


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Import New Orleans JSON data"
        self.description = ""

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

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

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

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
