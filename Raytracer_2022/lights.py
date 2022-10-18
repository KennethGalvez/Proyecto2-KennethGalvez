import mate as mt

DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2

def reflectVector(normal, direction):
    reflect = 2 * mt.productoV(normal, direction)
    reflect = mt.multiplicacionV(reflect, normal)
    reflect = mt.restaV(reflect, direction)
    reflect = mt.normalizarV(reflect)
    return reflect

def reflactVector(normal, direction, ior):
    #Snell´s Law
    cosi = max(-1, min(1, mt.productoV(direction, normal)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else: 
        etai, etat = etat, etai
        normal = normal * -1

    eta = etai / etat
    k = 1 - (eta**2) * (1-(cosi**2))

    if k < 0: #Total internal reflection
        return None
        
    j = eta * cosi - k **0.5
    R = mt.sumaV([mt.multiplicacionV(eta, direction)], [mt.multiplicacionV(j, normal)]) 
    return R
    

def fresnel(normal, direction, ior):
    #Snell´s Law  
    cosi = max(-1, min(1, mt.productoV(direction, normal)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai
    
    sint = etai / etat * (max(0, 1 - cosi**2) ** 0.5)

    if sint >= 1: #Total internal reflection
        return 1
    
    cost = max(0, 1 - sint**2) ** 0.5
    cosi = abs(cosi)

    Rs = ((etat * cosi) - (etai * cosi)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cosi)) / ((etai * cosi) + (etat * cost))

    return (Rs**2 + Rp**2)/2

class DirectionalLight(object):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = mt.normalizarV(direction)
        self.intensity = intensity
        self.color = color
        self.lightType = DIR_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = self.direction * -1
        intensity = mt.productoV(intersect.normal, light_dir) * self.intensity
        intensity = float(max(0, intensity))            
                                                        
        diffuseColor = [intensity * self.color[0],
                        intensity * self.color[1],
                        intensity * self.color[2]]

        return diffuseColor

    def getSpecColor(self, intersect, raytracer):
        light_dir = self.direction * -1
        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = mt.restaV( raytracer.camPosition, intersect.point)
        view_dir = mt.normalizarV(view_dir)

        spec_intensity = self.intensity * max(0,mt.productoV(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * self.color[0],
                    spec_intensity * self.color[1],
                    spec_intensity * self.color[2]]

        return specColor

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = self.direction * -1
        #light_dir = [x * -1 for x in self.direction]

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class PointLight(object):
    def __init__(self, point, constant = 1.0, linear = 0.1, quad = 0.05, color = (1,1,1)):
        self.point = point
        self.constant = constant
        self.linear = linear
        self.quad = quad
        self.color = color
        self.lightType = POINT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        light_dir = mt.restaV(self.point, intersect.point)
        light_dir = mt.normalizarV(light_dir)
        
        # att = 1 / (Kc + Kl * d + Kq * d * d)
        #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
        #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0
        intensity = mt.productoV(intersect.normal, light_dir) * attenuation
        intensity = float(max(0, intensity))            
                                                        
        diffuseColor = [intensity * self.color[0],
                        intensity * self.color[1],
                        intensity * self.color[2]]

        return diffuseColor

    def getSpecColor(self, intersect, raytracer):
        light_dir = mt.restaV(self.point, intersect.point)
        light_dir = mt.normalizarV(light_dir)

        reflect = reflectVector(intersect.normal, light_dir)

        view_dir = mt.restaV( raytracer.camPosition, intersect.point)
        view_dir = mt.normalizarV(view_dir)

        # att = 1 / (Kc + Kl * d + Kq * d * d)
        #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
        #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0

        spec_intensity = attenuation * max(0,mt.productoV(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = [spec_intensity * self.color[0],
                    spec_intensity * self.color[1],
                    spec_intensity * self.color[2]]

        return specColor

    def getShadowIntensity(self, intersect, raytracer):
        light_dir = mt.restaV(self.point, intersect.point)
        light_distance = mt.normalizarV(light_dir)
        light_dir = light_dir / light_distance

        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return shadow_intensity


class AmbientLight(object):
    def __init__(self, intensity = 0.1, color = (1,1,1)):
        self.intensity = intensity
        self.color = color
        self.lightType = AMBIENT_LIGHT

    def getDiffuseColor(self, intersect, raytracer):
        return mt.multiplicacionV(self.intensity, self.color)
        
    def getSpecColor(self, intersect, raytracer):
        return [0,0,0]

    def getShadowIntensity(self, intersect, raytracer):
        return 0
