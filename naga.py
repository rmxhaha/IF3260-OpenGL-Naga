import pygame
import numpy
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
	(1,-1,-1),
	(1, 1,-1),
	(-1, 1,-1),
	(-1,-1,-1),
	(1,-1,1),
	(1,1,1),
	(-1,-1,1),
	(-1,1,1),
	)

edges = (
	(0,1),
	(0,3),
	(0,4),
	(2,1),
	(2,3),
	(2,7),
	(6,3),
	(6,4),
	(6,7),
	(5,1),
	(5,4),
	(5,7),
	)
surfaces = (
	(0,1,2,3),
	(3,2,7,6),
	(6,7,5,4),
	(4,5,1,0),
	(1,5,7,2),
	(4,0,3,6),
	)
colors = (
	(1,0,0),
	(0.9,0,0),
	(0.7,0,0),
	(0.5,0,0),
	(0.3,0,0),
	)


def loadDragon():
	f = open('assets/Dragon/Dragon.obj', 'r')
	vertices = []
	uvs = []
	normals = []

	tvertices = []
	tuvs = []
	tnormals = []

	vertexIndices = []
	uvIndices = []
	normalIndices = []
	lineNum = 1

	for line in f:
		lineNum = lineNum + 1
		sline = line.split()
		if len(sline) == 0:
			continue
		if sline[0] == '#':
			continue
		if sline[0] == 'v':
			vertex = tuple( [float(x) for x in sline[1:4]] )
			tvertices.append(vertex)
		if sline[0] == 'vt':
			uv = tuple( [float(x) for x in sline[1:3]] )
			tuvs.append(uv)
		if sline[0] == 'vn':
			normal = tuple( [float(x) for x in sline[1:4]] )
			tnormals.append(normal)
		if sline[0] == 'f':
			ls = [ [int(float(x)) for x in face.split('/')] for face in sline[1:] ]
			if len(ls) != 4:
				continue
			for f in ls:
				vertexIndices.append(f[0])
				uvIndices.append(f[1])

	for vertexIndex in vertexIndices:
		vertex = tvertices[ vertexIndex - 1 ]
		vertices.append(vertex)
	for uvIndex in uvIndices:
		uv = tuvs[ uvIndex - 1 ]
		uvs.append(uv)

	return (vertices, uvs, normals)

dragon = loadDragon()
dragonVertices = dragon[0]

def Dragon():
	glBegin(GL_QUADS)
	i = 0
	fc = 0
	L = len(dragonVertices)
	while( i < L):
		fc += 1		
		glColor3fv(colors[fc%len(colors)])
		for x in range(4):
			glVertex3fv(dragonVertices[i])
			i = i + 1
	glEnd()
		
def Cube():
	glBegin(GL_QUADS)
	for surface in surfaces:
		x = 0
		for vertex in surface:
			glColor3fv(colors[x])
			x += 1
			glVertex3fv(verticies[vertex])
	glEnd()
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(verticies[vertex])
	glEnd()

def main():
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	# field of view, ratio, clipping plane how far before not drawn
	gluPerspective(45, (display[0]/display[1]), 0.1, 1000.0)
	
	#zoom out
	glTranslatef(-100,0.0,-400)

	# deg, x,y,z
	glRotatef(60,0,20,0)
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					glTranslatef(-10,0,0)
				if event.key == pygame.K_RIGHT:
					glTranslatef(10,0,0)
				if event.key == pygame.K_UP:
					glTranslatef(0,10,0)
				if event.key == pygame.K_DOWN:
					glTranslatef(0,-10,0)
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					glTranslatef(0,0,10.0)
				if event.button == 5:
					glTranslatef(0,0,-10.0)
					
		#glRotatef(1,3,1,1)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		#Cube()
		Dragon()
		pygame.display.flip()
		pygame.time.wait(10)

main()


	
