from pinhole_camera import *
from sys import path

path.append("../linear_algebra")
from linear_algebra import *



def view_transform(fro,to,up):
	forward = normalize(to-fro)
	upn = normalize(up)
	left = vector(*cross(forward[0:3],upn[0:3]))
	true_up = vector(*cross(left[0:3],forward[0:3]))
	orientation = np.eye(4)
	orientation[0,:] = left
	orientation[1,:] = true_up
	orientation[2,:] = -forward
	return orientation @ translation(-fro[x:w])
