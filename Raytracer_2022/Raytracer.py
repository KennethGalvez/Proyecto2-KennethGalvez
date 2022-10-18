from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 1000
height = 1000

# Materiales

steve = Material(texture = Texture("steve.bmp"))
tela = Material(texture = Texture("tela_roja.bmp"))
creeper = Material(texture = Texture("creper.bmp"))

stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
madera = Material(diffuse = (0.93, 0.81, 0.61), spec = 64)
azul = Material(diffuse = (0, 0, 1), spec = 64)
verde = Material(diffuse = (0, 1, 0), spec = 64)
cafe = Material(diffuse = (0.63, 0.50, 0.38), spec = 32)

sun = Material(diffuse = (0.6, 1, 1), spec = 64, matType = REFLECTIVE)
nubes = Material(diffuse = (0.70, 0.79, 0.85), spec = 64, ior = 1.5, matType = REFLECTIVE)

rtx = Raytracer(width, height)

rtx.envMap = Texture("fondos.bmp")

rtx.lights.append( AmbientLight(intensity = 0.4 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))
#rtx.lights.append( PointLight(point = (0,0,0)))

#rtx.scene.append( Sphere(V3(3,-3,-10), 1, steve))

rtx.scene.append( AABB(position = (-6,-6,-12), size = (2,2,2), material = stone))
rtx.scene.append( AABB(position = (-4,-6,-12), size = (2,2,2), material = stone))
rtx.scene.append( AABB(position = (-2,-5,-12), size = (2,2,2), material = stone))
rtx.scene.append( AABB(position = (0,-5,-12), size = (2,2,2), material = stone))
rtx.scene.append( AABB(position = (-6,-4,-13), size = (2,2,2), material = stone))
rtx.scene.append( AABB(position = (-4,-4,-13), size = (2,2,2), material = stone))


rtx.scene.append( AABB(position = (1,-5,-12), size = (2,2,2), material = madera))
rtx.scene.append( AABB(position = (1,-4,-13), size = (2,2,2), material = madera))
rtx.scene.append( AABB(position = (0,-4,-13   ), size = (2,2,2), material = madera))
rtx.scene.append( AABB(position = (-2,-4,-13), size = (2,2,2), material = madera))
rtx.scene.append( AABB(position = (-2,-2,-14), size = (3,3,3), material = madera))
rtx.scene.append( AABB(position = (-4,-2,-14), size = (3,3,3), material = madera))
rtx.scene.append( AABB(position = (-4,0,-14), size = (3,3,3), material = madera))
rtx.scene.append( AABB(position = (-4,2,-14), size = (3,3,3), material = madera))
rtx.scene.append( AABB(position = (-4,4,-14), size = (3,3,3), material = madera))
rtx.scene.append( AABB(position = (-4,6,-14), size = (3,3,3), material = madera))
rtx.scene.append( AABB(position = (-8,-2,-15), size = (3,3,3), material = madera))
rtx.scene.append( AABB(position = (-8,0,-16), size = (2,2,2), material = madera))
rtx.scene.append( AABB(position = (-8,2,-16), size = (2,2,2), material = madera))
rtx.scene.append( AABB(position = (-8,4,-16), size = (2,2,2), material = madera))
rtx.scene.append( AABB(position = (-8,6,-16), size = (2,2,2), material = madera))
rtx.scene.append( AABB(position = (-8,8,-15), size = (2,2,2), material = madera))

rtx.scene.append( Disk(position = (7,7,-14), radius = 1.2, normal = (1,0,0), material = sun ))
rtx.scene.append( Sphere(V3(7,7,-13), 1, sun))

rtx.scene.append( Sphere(V3(1,5,-13), 0.5, nubes))
rtx.scene.append( Sphere(V3(2,5,-13), 0.5, nubes))
rtx.scene.append( Sphere(V3(1.5,5.5,-13), 0.5, nubes))

rtx.scene.append( Sphere(V3(4,5,-13), 0.5, nubes))
rtx.scene.append( Sphere(V3(5,5,-13), 0.5, nubes))
rtx.scene.append( Sphere(V3(4.5,5.5,-13), 0.5, nubes))

rtx.scene.append( AABB(position = (-1,-3,-11), size = (1.2,3,1.2), material = azul))
rtx.scene.append( AABB(position = (-2.5,-3,-11), size = (1.2,3,1.2), material = verde))
#Cabezas
rtx.scene.append( AABB(position = (-1,-1,-11), size = (1,1,1), material = steve))
rtx.scene.append( AABB(position = (-2.5,-1,-11), size = (1.2,1.2,1.2), material = creeper))


rtx.glRender()


rtx.glFinish("output.bmp")