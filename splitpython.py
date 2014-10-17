import arcpy

infc = arcpy.GetParameterAsText(0)

desc = arcpy.Describe(infc)
shapefieldname = desc.ShapeFieldName

rows = arcpy.SearchCursor(infc)

def symbol(num):
    if num >= 0:
        return 1
    else:
        return -1
# y = ax + b
def get_b(line):
    start = line[0]
    slope = slope(line)
    b = slope * start.X - start.Y

def slope(line):
    start = line[0]
    end = line[1]
    return (end.Y - start.Y) / (end.X - start.X)

def touch(line1,line2):
    start1 = line1[0]
    end1   = line1[1]

    start2 = line2[0]
    slope2 = slope(line2)
    b2 = slope2 * start2.X - start2.Y

    func  = lambda x,y : slope2 * x + b2 -y

    return symbol(func(start1.X,start1.Y)) == symbol(func(end1.X,end1.Y)))


def intersect(line1,line2):
    if touch(line1,line2): return None
    a,b = line1[0],line1[1]
    c,d = line2[0],line2[1]
    denominator = (b.Y - a.Y)*(d.X - c.X) - (a.X - b.X)*(c.Y - d.Y)
    x = ( (b.X - a.X) * (d.X - c.X) * (c.Y - a.Y)
                + (b.Y - a.Y) * (d.X - c.X) * a.X
                - (d.Y - c.Y) * (b.X - a.X) * c.X ) / denominator
    y = -( (b.Y - a.Y) * (d.Y - c.Y) * (c.X - a.X)
                + (b.X - a.X) * (d.Y - c.Y) * a.Y
                - (d.X - c.X) * (b.Y - a.Y) * c.Y ) / denominator
    return arcpy.Point(x,y)

def vector_cross(vector1,vector2):
    return (vector1.Y * vector2.Z - vector1.Z * vector2.Y,
            vector1.Z * vector2.X - vector1.X * vector2.Z,
            vector1.X * vector2.Y - vector1.Y * vector2.X)

def vector_dot(vector1,vector2):
    return vector1.X * vector2.X + vector1.Y + vector2.Y

def start_end(extent,direction):
    ul = extent.upperLeft
    ur = extent.upperRight
    lr = extent.lowerRight
    ll = extent.lowerLeft
    start_pnts = [ul,ur,lr,ll]
    end_pnts  = [ur,lr,ll,ul]
    lines = zip(start,end)

def generate(extent,direction):
    start,end = start_end(extent,direction)
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