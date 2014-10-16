import arcpy

infc = arcpy.GetParameterAsText(0)

desc = arcpy.Describe(infc)
shapefieldname = desc.ShapeFieldName

rows = arcpy.SearchCursor(infc)

for row in rows:
    # Create the geometry object
    feat = row.getValue(shapefieldname)
    area = feat.area
    extent = feat.extent
    ul = extent.upperLeft
    lr = extent.lowerRight
    # get x,y ul.X ,ul.Y
    # new = feat.clip(extent)
    arcpy.AddMessage("{0},{1}".format(ul.X,ul.Y))


# array = arcpy.Array()

# List of coordinates.
#
# coordList = ['1.0;1.0','1.0;10.0','10.0;10.0','10.0;1.0']

# For each coordinate set, create a point object and add the x- and 
#   y-coordinates to the point object, then add the point object 
#   to the array object.
#
# for coordPair in coordList:
#     x, y = coordPair.split(";")
#     pnt = arcpy.Point(x,y)
#     array.add(pnt)

# Add in the first point of the array again to close the polygon boundary
#
# array.add(array.getObject(0))

# Create a polygon geometry object using the array object
#
# boundaryPolygon = arcpy.Polygon(array)

# Use the geometry to clip an input feature class
#
# arcpy.Clip_analysis("c:/data/rivers.shp", boundaryPolygon, "c:/data/rivers_clipped.shp")