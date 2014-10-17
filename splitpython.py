import arcpy
import math

infc = arcpy.GetParameterAsText(0)
area = float(arcpy.GetParameterAsText(1))
direction = int(arcpy.GetParameterAsText(2)) * math.pi / 180.0

vec = arcpy.Point(math.cos(direction),math.sin(direction),0.0)
z_vec = arcpy.Point(0.0,0.0,1.0)
rev_vec = vector_cross(vec,z_vec)

desc = arcpy.Describe(infc)
shapefieldname = desc.ShapeFieldName

rows = arcpy.SearchCursor(infc)


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

    mid_x = (ul.X + ur.X) / 2.0
    mid_y = (ul.Y + ll.Y) / 2.0

    # ax+b = y
    slp = direction.Y/direction.X
    b = mid_y - slp * mid_x
    
    # 求截点坐标
    start = arcpy.Point(0.0,b)
    end = arcpy.Point(-(b/slp),0.0)

    if vector_dot(start,end):
        return (start,end)
    else:
        return (end,start)

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
    return (geometries[0],geometries[1])

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
    feat = row.getValue(shapefieldname)
    split(feat,area,rev_vec)
    arcpy.AddMessage("{0},{1}".format(1,2))

# def symbol(num):
#     if num >= 0:
#         return 1
#     else:
#         return -1
# # y = ax + b
# def get_b(line):
#     start = line[0]
#     slope = slope(line)
#     b =  start.Y - slope * start.X

# def slope(line):
#     start = line[0]
#     end = line[1]
#     return (end.Y - start.Y) / (end.X - start.X)

# def not_touch(line1,line2):
#     start1 = line1[0]
#     end1   = line1[1]

#     start2 = line2[0]
#     slope2 = slope(line2)
#     b2 = slope2 * start2.X - start2.Y

#     func  = lambda x,y : slope2 * x + b2 -y

#     return symbol(func(start1.X,start1.Y)) == symbol(func(end1.X,end1.Y)))


# def intersect(line1,line2):
#     if not_touch(line1,line2): return None
#     a,b = line1[0],line1[1]
#     c,d = line2[0],line2[1]
#     denominator = (b.Y - a.Y)*(d.X - c.X) - (a.X - b.X)*(c.Y - d.Y)
#     x = ( (b.X - a.X) * (d.X - c.X) * (c.Y - a.Y)
#                 + (b.Y - a.Y) * (d.X - c.X) * a.X
#                 - (d.Y - c.Y) * (b.X - a.X) * c.X ) / denominator
#     y = -( (b.Y - a.Y) * (d.Y - c.Y) * (c.X - a.X)
#                 + (b.X - a.X) * (d.Y - c.Y) * a.Y
#                 - (d.X - c.X) * (b.Y - a.Y) * c.Y ) / denominator
#     return arcpy.Point(x,y)
