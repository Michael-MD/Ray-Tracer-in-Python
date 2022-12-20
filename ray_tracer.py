from sys import path

path.append("linear_algebra")
path.append("ray_casting")
path.append("primitives")
path.append("cameras")
path.append("ppm_file")
path.append("render")
path.append("materials")
path.append("lights")

from material import *
from point_light import *
from ray import ray
from primitives import *
from linear_algebra import *
from cameras import *
from render_scene import *
from world import *
