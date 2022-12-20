import numpy as np

x,y,z,w = 0,1,2,3

def translation(v):
	A = np.eye(4)
	A[x:w,w] = v[x:w]
	return A

def scaling(v):
	A = np.eye(4)
	A[x,x] = v[x]
	A[y,y] = v[y]
	A[z,z] = v[z]
	return A

def rotation_x(r):
	A = np.eye(4)
	A[y,y] = np.cos(r)
	A[y,z] = -np.sin(r)
	A[z,y] = np.sin(r)
	A[z,z] = np.cos(r)
	return A

def rotation_y(r):
	A = np.eye(4)
	A[x,x] = np.cos(r)
	A[x,z] = np.sin(r)
	A[z,x] = -np.sin(r)
	A[z,z] = np.cos(r)
	return A

def rotation_z(r):
	A = np.eye(4)
	A[x,x] = np.cos(r)
	A[x,y] = -np.sin(r)
	A[y,x] = np.sin(r)
	A[y,y] = np.cos(r)
	return A

def shearing(xy,xz,yx,yz,zx,zy):
	A = np.eye(4)
	A[0,1]=xy
	A[0,2]=xz
	A[1,0]=yx
	A[1,2]=yz
	A[2,0]=zx
	A[2,1]=zy
	return A
