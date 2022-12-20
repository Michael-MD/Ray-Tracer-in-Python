from sys import path
path.append("../linear_algebra")

from linear_algebra import *

def reflect(v_in,normal):
	return v_in - normal * 2 * dot(v_in,normal)