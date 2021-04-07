import sys, pygame
import math
import heapq
import random
import time


EXPLORANDO = 0
HACIA_ORIGEN = 1
HACIA_RECURSO = 2
TAREA_COMPLETADA = 3

class Agente:
  
  puntos_recursos = []  #Variable para almacenar las ubicaciones de los recursos

  def __init__(self, x, y, image, screen):
    self.image = pygame.image.load(image)
    self.rect = self.image.get_rect()
    self.init_x = x
    self.init_y = y
    self.x = x
    self.y = y
    self.map = None
    self.puntos_recorridos = []
    self.ubicacion_recurso = None
    self.status = EXPLORANDO
    self.camino = []
    self.step = 0
    self.total_steps = 0
    self.screen = screen
    self.recursos_recogidos = 0

  def quitar_recurso(self,punto):
    for r in Recurso.recursos:
      if r.punto == punto:
        return r.quitar_recurso()
    print("Recurso no encontrado")
    return 0


  def draw(self, screen):
    self.rect.x = self.x
    self.rect.y = self.y
    screen.blit(self.image, self.rect)
    pygame.draw.circle(screen, yellow, (self.init_x, self.init_y), self.recursos_recogidos) 
    screen.blit(font.render(str(self.recursos_recogidos), True, black), (self.init_x, self.init_y))

  
  def calcular_distancia(self, p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))  

  def get_vecinos_diponibles(self, punto, camino, puntos_sin_salida):
    vecinos_diponibles = []
    
    #Arriba
    x,y = punto[0], punto[1]
    up = (x, y-10)

    if up in self.puntos_recorridos and up not in camino and up not in puntos_sin_salida:
      vecinos_diponibles.append(up)

    left = (x - 10, y)
    if left in self.puntos_recorridos and left not in camino and left not in puntos_sin_salida:
      vecinos_diponibles.append(left)
    
    down = (x, y + 10)
    if down in self.puntos_recorridos and down not in camino and down not in puntos_sin_salida:
      vecinos_diponibles.append(down)
    
    right = (x + 10, y)
    if right in self.puntos_recorridos and right not in camino and right not in puntos_sin_salida:
      vecinos_diponibles.append(right)

    return vecinos_diponibles
    


  def calcular_camino(self):
    actual = (self.x, self.y)
    origen = (self.init_x, self.init_y)
    camino = []
    puntos_sin_salida = []
    while True:
      print("Calculando camino")
      vecinos_diponibles = self.get_vecinos_diponibles(actual, camino, puntos_sin_salida)
      if len(vecinos_diponibles) > 0:
        siguiente_punto = vecinos_diponibles[0]
        distancia_menor = self.calcular_distancia(siguiente_punto, origen)
        for i in range(0, len(vecinos_diponibles)):
          vecino_actual = vecinos_diponibles[i]
          distancia = self.calcular_distancia(vecino_actual, origen)
          if distancia < distancia_menor:
            distancia_menor = distancia
            siguiente_punto = vecino_actual
        camino.append(siguiente_punto)
        actual = siguiente_punto

        for step in camino:
          pygame.draw.circle(self.screen, blue, step, 5)
      else:
        puntos_sin_salida.append(actual)

        if len(camino) > 0:
          camino.pop()

        if len(camino) == 0:
          actual = (self.x, self.y)
        else: 
          actual = camino[len(camino) - 1]

        
      if actual == origen:
        break
    camino.insert(0,(self.x, self.y))
    return camino

  def hacia_origen(self):
    punto_siguiente = self.camino[self.step]
    self.x, self.y = punto_siguiente[0], punto_siguiente[1]
    if punto_siguiente == (self.init_x, self.init_y):
      self.recursos_recogidos += 1
      if self.recursos_recogidos == 25:
        self.status = TAREA_COMPLETADA
      elif self.ubicacion_recurso == None:
        self.status = EXPLORANDO
      else:
        self.status = HACIA_RECURSO
    elif self.step+1 != self.total_steps:
        self.step += 1

  def hacia_recurso(self):
    punto_siguiente = self.camino[self.step]
    self.x, self.y = punto_siguiente[0], punto_siguiente[1]
    if punto_siguiente == self.ubicacion_recurso:
       size = self.quitar_recurso(self.ubicacion_recurso)
       if size == 0:
         self.ubicacion_recurso = None
       self.status = HACIA_ORIGEN 
    elif self.step != 0:
        self.step -= 1

  def explorar(self):
    self.puntos_recorridos.append([self.x, self.y])
    while True:
      move_type =  random.randint(0,1)
      dx = 0
      dy = 0
      if move_type == 1: 
        dy = 10 #movimiento vertical
      else:
        dx = 10 #movimiento horizontal
      
      move_type =  random.randint(0,1)
      if move_type == 1: 
        dy *= -1
        dx *= -1

      self.x += dx
      self.y += dy

      if self.x  > width:
        self.x -= 20
      
      elif self.x < 0:
        self.x += 20
      
      if self.y  > height:
        self.y -= 20
      
      elif self.y < 0:
        self.y += 20
      punto = (self.x, self.y)
      if punto in obstaculos:
        self.puntos_recorridos.append(punto)
      elif punto in Agente.puntos_recursos: #El agente se encuentra en un punto
        size = self.quitar_recurso(punto)  
        if size == 0: #El recurso se elimino
          self.ubicacion_recurso = None

        self.ubicacion_recurso = punto
        self.camino = self.calcular_camino()
        self.status = HACIA_ORIGEN
        self.total_steps  = len(self.camino)
        self.step = 0
        
        break
      elif punto not in self.puntos_recorridos: #Moverse en una direccion que previamente no se hayan explorado
        puntos_explorados.append(punto)
        self.puntos_recorridos.append(punto)
        break


    
        
    


class Recurso:

  recursos = []
  def __init__(self,width, height):
    self.size = random.randint(1,5) # Tamanio
    x = math.floor(random.randint(0,width)/10)*10
    y = math.floor(random.randint(0,height)/10)*10
    # Posicion aleatoria
    self.x = x 
    self.y = y
    self.punto = (x,y)
    Agente.puntos_recursos.append(self.punto)

  
  def quitar_recurso(self):
    self.size -= 1
    if self.size <= 0:
      aux = []
      index = 0
      indexPunto = 0
      for punto in Agente.puntos_recursos:
        if punto != self.punto:
          aux.append(punto)
        else:
          indexPunto = index
        index += 1
      Agente.puntos_recursos = aux.copy()
      del Recurso.recursos[indexPunto]
     
    return self.size


  def draw(self, screen):
    pygame.draw.circle(screen, green, (self.x, self.y), self.size*3) 
    screen.blit(font.render(str(self.size), True, black), (self.x-5, self.y+5))
  


white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
grey = (213, 213, 213)
yellow = (243, 235, 104)



pygame.init()

width = 800 #ancho de la ventana
height = 600  #alto de la ventana


size = width + 30, height + 30

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Proyecto - Fase 1")


run = True



font = pygame.font.SysFont('Arial', 10)

agents = []
agents.append(Agente(0,0,"robot1-20x20.png", screen))
""" agents.append(Agente(0,height,"robot2-20x20.png",screen))
agents.append(Agente(width,0,"robot2-20x20.png",screen))
agents.append(Agente(width,height,"robot2-20x20.png",screen)) """




Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))
Recurso.recursos.append(Recurso(width, height))



obstaculos = []

# Abajo izquierda
obstaculos.append((100,500))
obstaculos.append((100,510))
obstaculos.append((100,520))
obstaculos.append((100,530))
obstaculos.append((100,540))
obstaculos.append((110,540))
obstaculos.append((120,540))
obstaculos.append((130,540))
obstaculos.append((140,540))
obstaculos.append((150,540))
obstaculos.append((160,540))
obstaculos.append((170,540))
obstaculos.append((180,540))

# Abajo derecha
obstaculos.append((600,540))
obstaculos.append((610,540))
obstaculos.append((620,540))
obstaculos.append((630,540))
obstaculos.append((640,540))
obstaculos.append((650,540))
obstaculos.append((660,540))
obstaculos.append((670,540))
obstaculos.append((680,540))
obstaculos.append((680,530))
obstaculos.append((680,520))
obstaculos.append((680,510))
obstaculos.append((680,500))

# Arriba derecha
obstaculos.append((600,140))
obstaculos.append((610,140))
obstaculos.append((620,140))
obstaculos.append((630,140))
obstaculos.append((640,140))
obstaculos.append((650,140))
obstaculos.append((660,140))
obstaculos.append((670,140))
obstaculos.append((680,140))
obstaculos.append((680,150))
obstaculos.append((680,160))
obstaculos.append((680,170))
obstaculos.append((680,180))



# Arriba izquierda
obstaculos.append((100,140))
obstaculos.append((110,140))
obstaculos.append((120,140))
obstaculos.append((130,140))
obstaculos.append((140,140))
obstaculos.append((150,140))
obstaculos.append((160,140))
obstaculos.append((170,140))
obstaculos.append((180,140))
obstaculos.append((100,150))
obstaculos.append((100,160))
obstaculos.append((100,170))
obstaculos.append((100,180))




total_unidades = 0
puntos_explorados = []

while (run):
  pygame.time.delay(50)
  screen.fill(white)
  for event in pygame.event.get():
    if event.type == pygame.QUIT: run = False
  
  for punto in puntos_explorados:
    pygame.draw.circle(screen, grey, punto, 5)
  
  for punto in obstaculos:
    pygame.draw.circle(screen, red, punto, 5)

  for agent in agents:
    if agent.status == EXPLORANDO:
      agent.explorar()
    elif agent.status == HACIA_ORIGEN:
      agent.hacia_origen()
    elif agent.status == HACIA_RECURSO:
      agent.hacia_recurso()
    elif agent.status == TAREA_COMPLETADA:
      pass
    agent.draw(screen)
  

  for recurso in Recurso.recursos:
    if recurso.size > 0:
      recurso.draw(screen)

 
  
  pygame.display.update()  

pygame.quit()
