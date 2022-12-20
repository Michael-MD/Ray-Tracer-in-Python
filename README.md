# Ray-Tracer-in-Python
Ray Tracer in Python based on Jamis Buck's Ray Tracing Challenge.

## 1. Setup
# 1.1. Install Python
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
</ul>
The triangle primitive expects three points during initilization for the three vertices. For example
```
triangle(point(0,0,0),point(1,1,1),point(-1,0,1))
```
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

## 2.4. Materials
### 2.4.1
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

## 2.5. Lighting
Currently the only light available is a point light.
### 2.5.1 Point Light
This is a light source which radiates in all directions. To assign a point light
```
w.light = point_light( position, intensity )
```
position: where the light is located
intensity: The color of the source e.g. bright white light is color(1,1,1).

## 2.6. Camera
Finally, we need to add a camera to our scene.
### 2.6.1 Pinhole Camera
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

## 2.7. Render Image
To render the image simply include these two lines
```
image = render(cam, w)
image.to_ppm(filename)
```

# 3. Extra Content
## 3.1 Bounding Boxes
To be more efficient, before calculating ray intersections with entire groups, the renderer will check if the ray intersects a axis-aligned-bounding box.


