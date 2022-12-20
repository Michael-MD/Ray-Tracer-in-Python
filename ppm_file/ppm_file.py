class ppmFile:
	def __init__(self,w,h):
		self.w = w
		self.h = h

		self.screen = [[0,0,0] for x in range(w*h)]


	def write_pixel(self,x,y,c):
		try:
			self.screen[y*self.w+x] = c
		except:
			print("pixel out of range")

	def to_ppm(self, filename):
		ftype='P3'
		ppmfile=open(filename+".ppm",'w+')
		ppmfile.write("%s\n" % (ftype)) 
		ppmfile.write("%d %d\n" % (self.w, self.h)) 
		ppmfile.write("255\n")


		for r,g,b in self.screen:
			ppmfile.write(str(r*255)+' '+str(g*255)+' '+str(b*255)+'\n')
		ppmfile.close()

	def __getitem__(self,pos):
		x,y = pos
		return self.screen[y*self.w+x]
