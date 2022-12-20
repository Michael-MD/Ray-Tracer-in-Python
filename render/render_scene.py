from sys import path
path.append("../ppm_file")
path.append("../ray_casting")
path.append("../linear_algebra")
path.append("../lights")

from linear_algebra import *
from ppm_file import *
from cast_ray_to_canvas import *
from ray_intersection import *
from world import *
from group_transform import *
from reflect import reflect


def render(cam, w):
	image = ppmFile(cam.hsize, cam.vsize)
	for y in range( 0, cam.vsize ):
		print(y)
		for x in range( 0, cam.hsize ):
			r = ray_for_pixel(cam, x, y)
			c = color_at(w, r)
			image.write_pixel(x, y, c)
	return image


def is_shadowed(w,p):
	v = w.light.position - p
	distance = mag(v)
	direction = normalize(v)
	r = ray(p,direction)
	intersections = intersect_world(w,r)
	h= hit(intersections)
	if h != None and h.t < distance:
		return True
	else:
		return False


class prepare_computations:
	def __init__(self,i, r, xs = []):
		self.t = i.t
		self.object = i.object
		self.p = position_calc(r, self.t)
		self.eyev = -r.direction
		self.normalv = normal_at(self.object, self.p)
		self.reflectv = reflect(r.direction,self.normalv)

		if dot(self.normalv, self.eyev) < 0:
			self.inside = True
			self.normalv = -self.normalv
		else:
			self.inside = False

		self.over_point = self.p+self.normalv*EPSILON
		self.under_point = self.p-self.normalv*EPSILON

		containers = []
		for x in xs:
			if i is x:
				if len(containers) == 0:
					self.n1 = 1.0
				else:
					self.n1 = containers[-1].mat.refractive_index

			if x.object in containers:
				containers.remove(x.object)
			else:
				containers.append(x.object)

			if i is x:
				if len(containers) == 0:
					self.n2 = 1.0
				else:
					self.n2 = containers[-1].mat.refractive_index


def normal_at(s,world_point):
	object_point = world_to_object(s,world_point)
	object_normal = s.local_normal_at(object_point)
	world_normal = normal_to_world(s,object_normal)
	world_normal[-1] = 0
	return normalize(world_normal)


def schlick(comps):
	cos = dot( comps.eyev, comps.normalv )
	if comps.n1 > comps.n2:
		n = comps.n1 / comps.n2
		sin2_t = n**2 * (1.0 - cos**2)
		if sin2_t > 1.0:
			return 1.0

		cos_t = np.sqrt(1.0 - sin2_t)
		cos = cos_t

	r0 = ((comps.n1 - comps.n2) / (comps.n1 + comps.n2))**2
	return r0 + (1 - r0) * (1 - cos)**5

def shade_hit(w,comps, remaining):
	shadowed = is_shadowed(w,comps.over_point)
	surface = lighting(comps.object,w.light,comps.p, comps.eyev, comps.normalv, shadowed)
	reflected = reflected_color( w,comps,remaining )
	refracted = refracted_color( w,comps,remaining )

	m = comps.object.mat
	if m.reflective > 0 and m.transparency > 0:
		reflectance  = schlick(comps)
		c =  surface + reflected*reflectance + refracted*(1-reflectance)
	else:
		c =  surface + reflected + refracted
	return np.minimum( c, color(1,1,1) )



def color_at(w,r,remaining = 5):
	xs = intersect_world(w,r)
	x = hit(xs)
	if x == None: return color(0,0,0)
	comps = prepare_computations(x,r,xs)
	return shade_hit(w,comps,remaining)

def lighting(object, light,p,eyev,normalv,in_shadow = False):
	mat = object.mat
	effective_color = mat.pat.pattern_at_object(object,p) * light.intensity
	lightv = normalize( light.position - p )
	ambient = effective_color * mat.ambient
	light_dot_normal = dot(lightv,normalv)
	if light_dot_normal < 0 or in_shadow:
		specular = diffuse = color(0,0,0)
	else:
		diffuse = effective_color * mat.diffuse * light_dot_normal
		reflectv = reflect(-lightv,normalv)
		reflect_dot_eye = dot(reflectv,eyev)

		if reflect_dot_eye <= 0:
			specular = color(0,0,0)
		else:
			factor =  reflect_dot_eye ** mat.shininess 
			specular = light.intensity * mat.specular * factor

	return ambient + diffuse + specular



def reflected_color(w,comps,remaining):
	if comps.object.mat.reflective < EPSILON: return color(0,0,0)
	reflect_ray = ray(comps.over_point,comps.reflectv)
	if remaining<=0: c = color(0,0,0)
	else: c = color_at( w,reflect_ray,remaining-1 )
	return c * comps.object.mat.reflective


def refracted_color(w,comps,remaining):
	if comps.object.mat.transparency == 0 or remaining <= 0:
		return color(0,0,0)

	n_ratio = comps.n1 / comps.n2
	cos_i = dot(comps.eyev, comps.normalv)
	sin2_t = n_ratio**2 * (1 - cos_i**2)

	if sin2_t > 1:
		return color(0,0,0)

	cos_t = np.sqrt(1.0 - sin2_t)
	direction = comps.normalv * (n_ratio * cos_i - cos_t) - comps.eyev * n_ratio
	refract_ray = ray(comps.under_point, direction)
	c = color_at(w, refract_ray, remaining - 1)
	return c * comps.object.mat.transparency