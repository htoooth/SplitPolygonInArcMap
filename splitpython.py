import arcpy

infc = arcpy.GetParameterAsText(0)

desc = arcpy.Describe(infc)
shapefieldname = desc.ShapeFieldName

rows = arcpy.SearchCursor(infc)

for row in rows:
    # Create the geometry object
    feat = row.getValue(shapefieldname)
    arcpy.AddMessage("{0}".format(feat))

