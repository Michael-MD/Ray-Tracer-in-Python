from sys import path
path.append("../linear_algebra")
path.append("../ray_casting")

from linear_algebra import *
from reflect import *

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