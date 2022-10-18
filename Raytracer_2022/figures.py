from locale import normalize
from math import pi, sqrt
import mate as mt
import numpy as np

WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, texcoords, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.sceneObj = sceneObj

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0, matType = OPAQUE, texture = None):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.matType = matType
        self.texture = texture


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = mt.restaV(self.center, orig)
        tca = mt.productoV(L, dir)
        e = mt.normalizarV2(L) ** 2 - tca ** 2 
        if e <0: return None
        d = sqrt(e)

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # P = O + t0 * D
        P = mt.sumaV(orig, [t0 * x for x in dir])
        normal = mt.restaV(P, self.center)
        normal = mt.normalizarV(normal)

        u = np.arctan2(normal[2], normal[0]) / (2 * pi) + 0.5
        v = np.arccos(-normal[1]) / pi

        uvs = (u,v)

        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         texcoords = uvs,
                         sceneObj = self)

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = mt.normalizarV(normal)
        self.material = material

    def ray_intersect(self, orig, dir):
        denom = mt.productoV(dir, self.normal)

        # Distancia = (( planePos - origRayo) o normal) / ( direccionRayo o normal)

        if abs(denom) > 0.001:
            num = mt.productoV( mt.restaV(self.position, orig), self.normal)
            t = num / denom

            if t > 0:
                #P = 0 + t*D
                P = mt.sumaV(orig, [t*d for d in dir])
                return Intersect(distance = t,
                         point = P,
                         normal = self.normal,
                         texcoords = None,
                         sceneObj = self)
        return None

class AABB(object):
    #Axis aligned Bounding Box
    def __init__(self, size, position, material): 
        self.position = position
        self.size = size
        self.material = material

        self.planes = []

        halfSizes = [0,0,0]

        halfSizes[0] = size[0] / 2
        halfSizes[1] = size[1] / 2
        halfSizes[2] = size[2] / 2

        #Sides
        self.planes.append(Plane(mt.sumaV(position, (halfSizes[0],0,0)), (1,0,0), material))
        self.planes.append(Plane(mt.sumaV(position, (-halfSizes[0],0,0)), (-1,0,0), material))
        #Up and down
        self.planes.append(Plane(mt.sumaV(position, (0,halfSizes[1],0)), (0,1,0), material))
        self.planes.append(Plane(mt.sumaV(position, (0,-halfSizes[1],0)), (0,-1,0), material))
        #Front and Back
        self.planes.append(Plane(mt.sumaV(position, (0,0,halfSizes[2])), (0,0,1), material))
        self.planes.append(Plane(mt.sumaV(position, (0,0,-halfSizes[2])), (0,0,-1), material))

        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + halfSizes[i])
            self.boundsMax[i] = self.position[i] + (epsilon + halfSizes[i])
            
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter is not None:
                
                planePoint = planeInter.point
                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter
                                #Tex Cords

                                u, v = 0, 0 

                                #Las uvs de las caras de los lados
                                if abs(plane.normal[0]) > 0:
                                    #Mapear uvs para el eje x, usando las coordenadas de Y y Z
                                    u = (planeInter.point[1] - self.boundsMin[1]) / (self.size[1])
                                    v = (planeInter.point[2] - self.boundsMin[2]) / (self.size[2])
                                
                                elif abs(plane.normal[1] > 0):
                                    #Mapear uvs para el eje x, usando las coordenadas de Y y Z
                                    u = (planeInter.point[0] - self.boundsMin[0]) / (self.size[0])
                                    v = (planeInter.point[2] - self.boundsMin[2]) / (self.size[2])

                                elif abs(plane.normal[2] > 0):
                                    #Mapear uvs para el eje x, usando las coordenadas de Y y Z
                                    u = (planeInter.point[0] - self.boundsMin[0]) / (self.size[0])
                                    v = (planeInter.point[1] - self.boundsMin[1]) / (self.size[1])

        if intersect is None:
            return None

        return Intersect(distance = t,
                         point = intersect.point,
                         normal = intersect.normal,
                         texcoords = (u,v),
                         sceneObj = self)            

class Disk (object):
    def __init__(self, position, radius, normal, material):
        self.plane = Plane(position, normal, material)
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        intersect = self.plane.ray_intersect(orig, dir)
        if intersect is None:
            return None
        contact = mt.restaV(intersect.point,self.plane.position)
        contact = mt.normalizarV2(contact)

        if contact > self.radius:
            return None
        
        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = self.plane.normal,
                         texcoords = None,
                         sceneObj = self)            

