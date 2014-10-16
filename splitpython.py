import arcpy

infc = arcpy.GetParameterAsText(0)

desc = arcpy.Describe(infc)
shapefieldname = desc.ShapeFieldName

rows = arcpy.SearchCursor(infc)

def generate_vector(ul,ur,ll,lr,direction):
    pass

def generate(extent,direction):
    ur = extent.upperRight
    ul = extent.upperLeft
    ll = extent.lowerLeft
    lr = extent.lowerRight

    start,end = generate_vector(ul,ur,ll,lr,direction)
    array = arcpy.Array()
    array.add(start)
    array.add(end)
    return arcpy.Polyline(array)

def half(geometry,direction):
    extent = geometry.extent
    line = generate(extent,direction)
    geometries = geometry.cut(line)
    return geometries[0],geometries[1]

def good_enough(guess,area):
    return abs(guess - area) < 0.001

def split(geometry,area,direction):
    if good_enough(geometry,area):
        return geometry

    left,right = half(geometry,direction)

    if(right.area > area):
        return this(right,area,direction)
    else:
        area = area -right.area
        return right.union(split(geometry,area,direction))


for row in rows:
    # Create the geometry object
    feat = row.getValue(shapefieldname)
    area = feat.area
    extent = feat.extent

    ur = extent.upperRight
    ul = extent.upperLeft

    ll = extent.lowerLeft
    lr = extent.lowerRight

    # get x,y ul.X ,ul.Y
    # new = feat.clip(extent)
    # new = feat.union(geometry)
    # cut = feat.cut(PolyLine)
    # cut[0] cut[1]
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