# Ray-Tracer-in-Python
Ray Tracer in Python based on Jamis Buck's Ray Tracing Challenge. As a courtesy, I would appreciate it if you email me first at mdei0001@student.monash.edu before using this code.

## 1. Setup
### 1.1. Install Python
Obviously a version of python 3 is required. The code has been tested on version 3.9.13. You can check you're version of python by running
```
python --version
```

### 1.2. Downloading Source Code
This can be done by cloing the repo using
```
git clone https://github.com/Michael-MD/Ray-Tracer-in-Python.git
```
or simply zipping and download directly from github.

## 2. Usage
### 2.1. Creating World
All the necessary parts of the ray-tracer are imported into a single file called ray_tracer.py in the root directory. Ensure that you're project has access to the ray-tracer root directory and import it using
```
from ray_tracer import *
```
This imports all patterns, shapes, lights etc.

The render is written using oop so multiple instances of the render can be defined in a single file. To render a scene instantiate the world() class
```
w = world()
```
Shapes can be added to w using
```
s = sphere()
w.objects.append(s)
```
### 2.2. Inserting Primitives/shapes
Now you are free to import objects into your scene. To import a primitive, for example a plane:
```
floor = plane()
```
The other primitives as of writing this document are:
<ul>
  <li>cone</li>
  <li>cube</li>
  <li>cylinder</li>
  <li>double_nabbed_cone</li>
  <li>group</li>
  <li>plane</li>
  <li>sphere</li>
  <li>triangle</li>
  <li>obj_model</li>
</ul>
The triangle primitive expects three points during initilization for the three vertices. For example

```
triangle(point(0,0,0),point(1,1,1),point(-1,0,1))
```
obj_model expects an obj file. The class which reads the obj file is buggy so it should be replaced with a proper class but the one here does the job.
Additional notes:
 - trangles are mostly useful only for models.
 - cylinder by default by default is capped and extends infinitly in both directions, this can be set by setting the min and max attributes. Removing caps from the cylinder is controlled using the isclosed boolean attribute.
 - the cone has these same properties as the cylinder
 - every shape is placed at the origin with default dimensions. Everything is usually set to unity e.g. unit radius, unit length etc. A shape can be deformed using the transform attribute by assigning transformation matrices. Simple transformations can ofcourse be chained together using numpy's @ operator. The full list of transformation matrices is given in the next subsection.

### 2.3. Transformation matrices
Transformation matrices can be used for any object with a transform attribute. Depending on the object the transformation depends on the object under consideration.
<ul>
  <li>translation</li>
  <li>scaling</li>
  <li>rotation_x</li>
  <li>rotation_y</li>
  <li>rotation_z</li>
  <li>shearing</li>
</ul>
These all take 4x1 numpy arrays except shearing which has function handle given by
```
def shearing(xy,xz,yx,yz,zx,zy)
```

### 2.4. Groups
If an scene contains many items, use groups. It is easier to write and makes the ray-tracer more efficient. To see why why the render is more efficient, jump to "Bounding Boxes".
A group contains a group of shapes which transform together. For example, one may define a group of three sphere's and then move them whereever they want in the scene rather than moving each sphere individually.
Here is an example of using a group containing 3 spheres. For simplicity, they are all the same.
```
s1 = sphere()
s2 = sphere()
s3 = sphere()
g = group()
g.add_child(s1)
g.add_child(s2)
g.add_child(s3)
```
The group needs to then be added to the world class instance.

### 2.5. Materials
#### 2.5.1
By default all shapes have a white solid color i.e. rgb = (255,255,255). This can be changed by asigning a new solid_color class to the pat atrribute of the mat attribute of the shape for example, here is a red sphere:
```
s = sphere()
s.mat.pat = solid_color( color(1,0,0) )
```
Observe all colors are in the range [0,1].
For a more interesting pattern, here are some choices:
<ul>
  <li> stripe_pattern </li>
  <li> solid_pattern </li>
  <li> gradient_pattern </li>
  <li> ring_pattern </li>
  <li> checkered_pattern </li>
  <li> radial_gradient_pattern </li>
</ul>
stripe_pattern, gradient_pattern, ring_pattern, checkered_pattern and radial_gradient_pattern expect two colors as input.
Every object also has a material with attributes:
<ul>
  <li> ambient = .1 </li>
  <li> diffuse = .9 </li>
  <li> specular = .9 </li>
  <li> shininess = 200. </li>
  <li> reflective = 0. </li>
  <li> transparency = 0. </li>
  <li> refractive_index = 1. </li>
</ul>
All values must be >= 0. All values must be <= 1 except refractive_index and shininess.

### 2.6. Lighting
Currently the only light available is a point light.
#### 2.6.1 Point Light
This is a light source which radiates in all directions. To assign a point light
```
w.light = point_light( position, intensity )
```
position: where the light is located
intensity: The color of the source e.g. bright white light is color(1,1,1).

### 2.7. Camera
Finally, we need to add a camera to our scene.
#### 2.7.1 Pinhole Camera
We assign a camera to our world as follows:
```
cam = camera( canvas_width, canvas_height, field_of_view )
```
canvas_width: width of rendered image in pixels
canvas_height: height of rendered image in pixels
field_of_view: field of view of camera, takes some angle in radians.


To set the location of the camera
```
cam.transform = view_transform( from, to, up ) 
```
from: where the camera is located
to: where the camera is pointing
up: which direction is up, for example, if you want to take a picture with camera tilted or even upside-down!

### 2.8. Render Image
To render the image simply include these two lines
```
image = render(cam, w)
image.to_ppm(filename)
```

# 3. Extra Content
## 3.1 Bounding Boxes
To be more efficient, before calculating ray intersections with entire groups, the renderer will check if the ray intersects a axis-aligned-bounding box.

# 4. Showcase
Here is an example of a file:
(images/sample_render.jpg)
The code to generate is as follows:

```
from ray_tracer import *
import numpy as np

tau = 2*np.pi

w = world()

# -----------------   room walls  -----------------
room_walls = group()

floor = plane()
floor.mat.reflective = .5
floor.diffuse = .6
floor.mat.pat = stripe_pattern(color(16/255, 227/255, 97/255),color(227/255, 16/255, 86/255))
floor.mat.pat.transform = scaling(vector(.5,.5,.5))@rotation_y(tau/4)

left_wall = plane()
left_wall.transform = translation(vector(0,0,-10))@rotation_x(tau/4)

right_wall = plane()
right_wall.transform = translation(vector(0,0,5))@rotation_x(tau/4)

back_wall = plane()
back_wall.transform = translation(vector(-5,0,0))@rotation_z(tau/4)

ceiling = plane()
ceiling.transform = translation(vector(0,6,0))


room_walls.add_child(floor)
room_walls.add_child(left_wall)
room_walls.add_child(right_wall)
room_walls.add_child(back_wall)
room_walls.add_child(ceiling)

w.objects.append( room_walls )


# -----------------   cylinder on cube  -----------------
c_on_c = group()

cu = cube()
cu.transform = rotation_y(0.2*tau)@translation(vector(0,1,0))
cu.mat.pat = solid_pattern(color(227/255, 16/255, 86/255))
cu.mat.diffuse = .1
cu.mat.transparency = .8
cu.mat.specular = .1
cu.mat.reflective = .6
cu.mat.shininess = 50.

cy = cylinder()
cy.min = 2
cy.max = 4
cy.mat.pat = solid_pattern(color(35/255, 153/255, 186/255))
cy.mat.pat.translation = scaling(vector(.1,.1,.1))

c_on_c.transform = translation(vector(-1,0,0))

c_on_c.add_child(cu)
c_on_c.add_child(cy)

w.objects.append( c_on_c )


# -----------------    cone and sphere  -----------------
c = cone()
c.transform = scaling(vector(1,2,1))@translation(vector(1,1,-1.5))
c.mat.pat = gradient_pattern(color(0.8,.3,.7),color(.7,.2,.3))

s1 = sphere()
s1.transform = translation(vector(1,1,1.5))
s1.mat.transparency = .9
s1.mat.diffuse = .1
s1.mat.ambient = .05
s1.mat.reflective = .95
s1.mat.refractive_index = 1.5


w.objects.append(c)
w.objects.append(s1)

# -----------------  teapot -----------------
teapot = obj_model('sample_obj_files/teapot-low.obj')
teapot.transform = translation(vector(0,0,-6))@scaling(vector(.2,.2,.2))@rotation_y(-0.2*tau)@rotation_x(-tau/4)
teapot.mat.reflective = 1
teapot.mat.diffuse = .05
teapot.mat.specular = .05
teapot.mat.ambient = .05
teapot.mat.shininess = 50.
w.objects.append(teapot)


# -----------------  set up rest of scene -----------------

w.light = point_light(point(10,3,-1), color(1, 1, 1))


cam = pinhole_camera(1920, 960, 0.2*tau)
cam.transform = view_transform(point(12,3,-3),point(0, 3, -3),vector(0, 1, 0))


image = render(cam, w)
image.to_ppm("test")

```

