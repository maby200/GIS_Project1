import arcpy
import json
import os

def loadJSONtoArcGIS(workspace = r'C:\Users\mgavil3\Box\CursosLSU\GISProgramming4057\Projects\P1',
                     json_path = "data/no_tax.json",
                     fc_name = 'no_tax_fc.shp',
                     output_shp_folder = 'output'
                     ):
    with open(json_path, "r") as json_data:
        study_area = json.load(json_data)
        
    for row in study_area['data']:
        arcgis_geom = arcpy.FromWKT(row[8])
        row.append(arcgis_geom)
        
    workspace = workspace
    fc_name = fc_name
    output_folder = os.path.join(workspace, output_shp_folder)
    fc_full_name = os.path.join(output_folder, fc_name)
    if arcpy.Exists(fc_full_name):
        arcpy.management.Delete(fc_full_name)
    arcpy.management.CreateFeatureclass(
                                        out_name = fc_name,
                                        out_path = output_folder,
                                        geometry_type = 'POLYGON',
                                        spatial_reference = 4326
                                        )

    fields = study_area["meta"]["view"]["columns"]
    fields = [field['name'] for field in fields if field['name'] != 'the_geom']
    field_type = ['TEXT','TEXT','LONG','LONG','TEXT','LONG','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT']# not including 'the_geom' field nor the ARGIS Polygon]
    # changing field names because are the same as the defaults when Feature Class is created
    fields[1] = 'uid'
    fields[9] = 'uid2'
    fields = [field.replace(' ','_') for field in fields]
    fields = [field.replace('.','_') for field in fields]
    fields = [field[:10] if len(field)>10 else field for field in fields]

    for idx, field in enumerate( fields):
        # print(field_name)
        arcpy.management.AddField(in_table = fc_full_name, field_name = field, field_type = field_type[idx])
        
    fields.append('SHAPE@')
        
    with arcpy.da.InsertCursor(fc_full_name,field_names=fields) as cursor:

        for row in study_area['data']:
            inserting_row = []
            for idx, value in enumerate(row):
                if idx == 8:
                    continue
                if value == None:
                    value = ""
                inserting_row.append(value)
            cursor.insertRow(inserting_row)
            
def main():
    import sys
    fc_name = sys.argv[1]
    loadJSONtoArcGIS(fc_name=fc_name)

if __name__ == "__main__":
    loadJSONtoArcGIS()