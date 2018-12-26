#! /usr/bin/env python
# -*- coding: utf8 -*-
"""Port of NeHe Lesson 26 by Ivan Izuver <izuver@users.sourceforge.net>"""
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Image import *

import sys,gc

#posplanetas  1.9 | 3 | 4 | 5.5 | 7 | 8.5 | 10 | 11.5
ESCAPE = '\033'
lastX = 0
lastY = 0
rotateX = 0.0
rotateY = 0.0
condicion = False;
window = 0
rot = 0.0
LightAmb=(0.7,0.7,0.7)  
LightDif=(1.0,1.0,0.0)  
LightPos=(4.0,4.0,6.0,1.0)
xrot=yrot=0.0 

xrotspeed=yrotspeed=0.0 
zoom=-3.0 
height=0.5 
textures = {}

print("hola")
def LoadTextures(fname):
	if textures.get( fname ) is not None:
		return textures.get( fname )
	texture = textures[fname] = glGenTextures(1)
	image = open(fname)
	
	ix = image.size[0]
	iy = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
	
	# Comenzamos con la textura   
	glBindTexture(GL_TEXTURE_2D, texture)   # textura en 2d ( x y y)
	
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	return texture

 
def InitGL(Width, Height):                
	glClearColor(0.0, 0.0, 0.0, 0.0)    
	glClearDepth(1.0)                 
	glClearStencil(0)
	glDepthFunc(GL_LEQUAL)            
	glEnable(GL_DEPTH_TEST)           
	glShadeModel(GL_SMOOTH)         

	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	glEnable(GL_TEXTURE_2D)
	

	glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
	glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
	glEnable(GL_LIGHT0)           
	glEnable(GL_LIGHTING)
	
   

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()                    
			
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)
      

	
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevenimos para una division entro 0
        Height = 1

    glViewport(0, 0, Width, Height)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawStars(Width,Height):

        glColor3f(1.0, 1.0, 1.0);
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glDisable(GL_DEPTH_TEST)

	glBindTexture( GL_TEXTURE_2D, LoadTextures('stars.bmp') )
	glPushMatrix()
	glBegin(GL_QUADS)
	glTexCoord2f(-Width,Height)
	glVertex2d(-Width,-Height)
	glTexCoord2f(Width,Width)
	glVertex2d(Width,0)
	glTexCoord2f(Width,0.0)
	glVertex2d(Width,Height)
	glTexCoord2f(0.0,0.0)
	glVertex2d(0,Height)
	glEnd()
	glPopMatrix()


	glEnable(GL_DEPTH_TEST)


def DrawSun():
        global Q
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('sun.tga') )
	
	Q=gluNewQuadric()
	gluQuadricNormals(Q, GL_SMOOTH)
	gluQuadricTexture(Q, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	gluSphere(Q, 0.7, 32, 16)

	glColor4f(1.0, 1.0, 1.0, 0.4)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE)
	glEnable(GL_TEXTURE_GEN_S)
	glEnable(GL_TEXTURE_GEN_T)
	gluSphere(Q, 0.7, 32, 16)
	
	glDisable(GL_TEXTURE_GEN_S)
	glDisable(GL_TEXTURE_GEN_T)
	glDisable(GL_BLEND)
	gluDeleteQuadric( Q )

def DrawMercury():
        global Q2
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('mercurymap.bmp') )
	
	Q2=gluNewQuadric()
	gluQuadricNormals(Q2, GL_SMOOTH)
	gluQuadricTexture(Q2, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
 	glPushMatrix()
        glTranslatef(0.0,0.0,1.9)			
        gluSphere(Q2,0.2,32,16) 
	glPopMatrix()

	gluDeleteQuadric( Q2 )
def DrawVenus():
        global Q3
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('venusmap.bmp') )
	
	Q3=gluNewQuadric()
	gluQuadricNormals(Q3, GL_SMOOTH)
	gluQuadricTexture(Q3, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	
	glPushMatrix() 
        glTranslatef(2.5,0.0,0.0)	
        gluSphere(Q3,0.3,32,16) 
	glPopMatrix()

	gluDeleteQuadric( Q3 )

def DrawEarth():
        global Q1
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('earthmap.bmp') )
	
	Q1=gluNewQuadric()
	gluQuadricNormals(Q1, GL_SMOOTH)
	gluQuadricTexture(Q1, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	glPushMatrix()
        glTranslatef(2.5,0.0,-4.0)			
        gluSphere(Q1,0.40,32,16) 
	gluDeleteQuadric( Q1 )
	glPopMatrix()

def DrawMars():
        global Q4
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('marsmap.bmp') )
	
	Q4=gluNewQuadric()
	gluQuadricNormals(Q4, GL_SMOOTH)
	gluQuadricTexture(Q4, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	glPushMatrix()
        glTranslatef(0,0.0,-5.5)			
        gluSphere(Q4,0.45,32,16)	
	gluDeleteQuadric( Q4 )
	glPopMatrix()

def DrawJupiter():
        global Q5
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('jupitermap.bmp') )
	
	Q5=gluNewQuadric()
	gluQuadricNormals(Q5, GL_SMOOTH)
	gluQuadricTexture(Q5, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	glPushMatrix()
        glTranslatef(-3.5,0.0,-6.5)			
        gluSphere(Q5,0.60,32,16) 
	glPopMatrix()
	
	gluDeleteQuadric( Q5 )
def DrawSaturn():
        global Q6
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('saturnmap.bmp') )
	
	Q6=gluNewQuadric()
	gluQuadricNormals(Q6, GL_SMOOTH)
	gluQuadricTexture(Q6, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	glPushMatrix()
        glTranslatef(-9.5,0.0,-1.5)	
	glPushMatrix()
	glScalef(1.1,1,1)	
        glutWireTorus(0.10,0.67, 100, 50);
	glPopMatrix()
        gluSphere(Q6,0.55,32,16) 
	glPopMatrix()	
	gluDeleteQuadric( Q6 )


def DrawUranus():
        global Q7
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('uranusmap.bmp') )
	
	Q7=gluNewQuadric()
	gluQuadricNormals(Q7, GL_SMOOTH)
	gluQuadricTexture(Q7, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	glPushMatrix()
        glTranslatef(0.0,0.0,10.0)			
        gluSphere(Q7,0.55,32,16) 
	glPopMatrix()
	gluDeleteQuadric( Q7 )

def DrawNeptuno():
        global Q8
        glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('neptunemap.bmp') )
	
	Q8=gluNewQuadric()
	gluQuadricNormals(Q8, GL_SMOOTH)
	gluQuadricTexture(Q8, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	
	glPushMatrix() 
        glTranslatef(6.0,0.0,11.5)	#11.5
        gluSphere(Q8,0.45,32,16) 
	glPopMatrix()
	gluDeleteQuadric( Q8 )

def mouse(button,state,x,y):
    lastX = x;
    lastY = y;

def motion(x,y):

    global rotateX
    global rotateY
    global lastX
    global lastY

    dx = x - lastX;
    dy = y - lastY;

    rotateX += dy;
    rotateY += dx;
 
    lastX = x;
    lastY = y;

  #  glutPostRedisplay()


def mover():
    global rot

    if(condicion):
	rot = (rot + 0.2) % 360  # rotacion
	glutPostRedisplay()
    else: pass	



def DrawGLScene():
    global rot, texture
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 

    

    glLoadIdentity()	

    glTranslatef(0.0, 0.0, -21.0)  # Move Into The Screen

    #gluLookAt(0.0, 0.0, zoom, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    gluLookAt(0.0, 1.0, 2.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0);

    glRotatef (rotateX, 1.0, 0.0, 0.0);
    glRotatef (rotateY, 0.0, 1.0, 0.0);
    glRotatef(rot, 1.0, 0.0, 0.0)  
    glRotatef(rot, 0.0, 1.0, 0.0)  
    glRotatef(-1, 0.0, 0.0, 1.0)   

    glBegin(GL_LINES);

  	# x axis */
   # glColor3f(1.0, 0.0, 0.0);
   # glVertex3f(0.0, 0.0, 0.0);
   # glVertex3f(15, 0.0, 0.0);

   # y axis */
   # glColor3f(0.0, 1.0, 0.0);
   # glVertex3f(0.0, 0.0, 0.0);
   # glVertex3f(0.0, 15, 0.0);

   # z axis */
   # glColor3f(0.0, 0.0, 1.0);
   # glVertex3f(0.0, 0.0, 0.0);
   # glVertex3f(0.0, 0.0, 15);

    glEnd();


    glPushMatrix()
    DrawStars(25,25)
    glPopMatrix()
  
    DrawSun()
 
    DrawMercury()
    DrawVenus()
    DrawEarth()
    DrawMars()
    DrawJupiter()
    DrawSaturn()
    DrawUranus()
    DrawNeptuno()

    mover()

    glutSwapBuffers()


def keyPressed(*args):
     
    global condicion

    if args[0] == ESCAPE:
        sys.exit()

    if args[0] == '1':
        condicion = True;
    if args[0] == '2':
	condicion = False;

def main():

    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1224, 1080)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Lab. Semana 05: texturas ")
    glutDisplayFunc(DrawGLScene)
    # glutFullScreen()
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouse);
    glutMotionFunc(motion);
    InitGL(1024, 1080)
    glutMainLoop()

if __name__ == "__main__":
    print "Hit ESC key to quit."
    main()















