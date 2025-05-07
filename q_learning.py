import pygame
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import os

pygame.init()

# Konstante
A = 25
VISINA = 10
SIRINA = 10
MAXSTANJE = 144

# Globalne promenljive
highscore = 0
brojep = 0
rekord = []
epbroj = []

class Sumica:
    def __init__(self, zmijica, voce, app):
        self.app = app
        self.n = 0 # 0 - jabuka je severno, 1 - jabuka je u isto liniji, 2 - jabuka je juzno
        self.w = 0 # 0 - jabuka je zapadno, 1 - jabuka je u isto liniji, 2 - jabuka je istocno
        self.s = 0 # da li postoji prepreka severno
        self.j = 0
        self.z = 1 # postoji prepreka zapadno, jer se na pocetku krece ka desno
        self.i = 0

        self.state = [self.n, self.w, self.s, self.j, self.z, self.i]

        self.x1 = 1 # ide desno
        self.y1 = 0 # ide ne ide ni gore ni dole

    def encode(self):
        i = self.state[0] * 3 + self.state[1]
        i = i * 2 + self.state[2]
        i = i * 2 + self.state[3]
        i = i * 2 + self.state[4]
        i = i * 2 + self.state[5]
        return i

    def step(self, action, zmijica, voce):
        nagrada = 0

        if action == 0: # hoce da skrene levo
            if self.x1 != 1:
                self.x1 = -1
                self.y1 = 0
            else:
                nagrada -= 100
        elif action == 1: # hoce da skrene desno
            if self.x1 != -1:
                self.x1 = 1
                self.y1 = 0
            else:
                nagrada -= 100
        elif action == 2: # gore
            if self.y1 != 1:
                self.x1 = 0
                self.y1 = -1
            else:
                nagrada -= 100
        elif action == 3: # dole
            if self.y1 != -1:
                self.x1 = 0
                self.y1 = 1
            else:
                nagrada -= 100

        # ako se sa tom akcijom priblizava jabuci, dajemo nagradu
        if abs(zmijica.x - voce.vx) > abs(zmijica.x + self.x1 - voce.vx):
            nagrada += 20
        elif abs(zmijica.x - voce.vx) < abs(zmijica.x + self.x1 - voce.vx):
            nagrada -= 20
        if abs(zmijica.y - voce.vy) > abs(zmijica.y + self.y1 - voce.vy):
            nagrada += 20
        elif abs(zmijica.y - voce.vy) < abs(zmijica.y + self.y1 - voce.vy):
            nagrada -= 20

        # odradimo akciju
        zmijica.x += self.x1
        zmijica.y += self.y1

        # ako smo pojeli voce, najveca nagrada
        if zmijica.x == voce.vx and zmijica.y == voce.vy:
            nagrada += 200

        # azuriramo parametre koji opisuju poziciju jabuke
        if zmijica.y == voce.vy:
            self.n = 1
        elif zmijica.y > voce.vy:
            self.n = 0
        else:
            self.n = 2
        self.state[0] = self.n

        if zmijica.x == voce.vx:
            self.w = 1
        elif zmijica.x > voce.vx:
            self.w = 0
        else:
            self.w = 2
        self.state[1] = self.w

        self.sever = [zmijica.x, zmijica.y - 1]
        self.s = int(zmijica.SudarSaZidom(self.app, *self.sever) or zmijica.SudarSaTelom(*self.sever))
        if self.sever[0] == voce.vx and self.sever[1] == voce.vy:
            nagrada += 30

        self.jug = [zmijica.x, zmijica.y + 1]
        self.j = int(zmijica.SudarSaZidom(self.app, *self.jug) or zmijica.SudarSaTelom(*self.jug))
        if self.jug[0] == voce.vx and self.jug[1] == voce.vy:
            nagrada += 30

        self.zapad = [zmijica.x - 1, zmijica.y]
        self.z = int(zmijica.SudarSaZidom(self.app, *self.zapad) or zmijica.SudarSaTelom(*self.zapad))
        if self.zapad[0] == voce.vx and self.zapad[1] == voce.vy:
            nagrada += 30

        self.istok = [zmijica.x + 1, zmijica.y]
        self.i = int(zmijica.SudarSaZidom(self.app, *self.istok) or zmijica.SudarSaTelom(*self.istok))
        if self.istok[0] == voce.vx and self.istok[1] == voce.vy:
            nagrada += 30

        self.state[2:6] = [self.s, self.j, self.z, self.i]

        done = zmijica.SudarSaTelom(zmijica.x, zmijica.y) or zmijica.SudarSaZidom(self.app, zmijica.x, zmijica.y)
        if done:
            nagrada -= 100

        return self.encode(), nagrada, done, {}

    def reset(self, app):
        kruska = Jabucica(app)
        zmijica = Zmija(app.sirina // 2, app.visina // 2)
        self.state = [0, 0, 0, 0, 1, 0]
        self.x1 = 1
        self.y1 = 0
        return zmijica, kruska, False, 0, self.encode()

    def render(self, zmijica, voce, app):
        if zmijica.x == voce.vx and zmijica.y == voce.vy:
            zmijica.Njam(voce, app)
            voce.NapraviVoce(zmijica, app)
        else:
            app.Crtaj(zmijica, voce)

class Uopsteno:
    def __init__(self, a, visina, sirina):
        self.a = a
        self.visina = visina
        self.sirina = sirina
        self.prozor = pygame.display.set_mode((sirina * a, visina * a))

    def NacrtajGrid(self):
        for i in range(self.visina):
            for j in range(self.sirina):
                pygame.draw.line(self.prozor, (50, 50, 50), (i * self.a, 0), (i * self.a, 500))
                pygame.draw.line(self.prozor, (50, 50, 50), (0, j * self.a), (500, j * self.a))
        pygame.display.update()

    def Crtaj(self, zmijica, jabuka):
        global highscore, rekord, epbroj

        self.prozor.fill((0, 0, 0))
        self.NacrtajGrid()

        zmijica.xtacke_zmije.pop(0)
        zmijica.ytacke_zmije.pop(0)
        zmijica.xtacke_zmije.append(zmijica.x)
        zmijica.ytacke_zmije.append(zmijica.y)

        for i in range(len(zmijica.xtacke_zmije)):
            pygame.draw.rect(self.prozor, (230, 230, 230), (zmijica.xtacke_zmije[i] * self.a, zmijica.ytacke_zmije[i] * self.a, self.a, self.a))

        pygame.draw.rect(self.prozor, (250, 0, 0), (jabuka.vx * self.a, jabuka.vy * self.a, self.a, self.a))

        font = pygame.font.SysFont(None, 20)
        score = len(zmijica.xtacke_zmije) - 2

        if highscore < score:
            highscore = score
            rekord.append(highscore)
            epbroj.append(brojep)

        tekst = font.render(f'Score: {score}', True, (255, 255, 255))
        tekst1 = font.render(f'Highscore: {highscore}', True, (255, 255, 255))

        self.prozor.blit(tekst, (1, 1))
        self.prozor.blit(tekst1, (100, 1))

        pygame.display.update()


class Jabucica:
    def __init__(self, app):
        self.vx = random.randint(0, app.sirina - 1)
        self.vy = random.randint(0, app.visina - 1)

    def NapraviVoce(self, zmijica, app):
        attempts = 0
        while zmijica.SudarSaTelom(self.vx, self.vy):
            self.vx = random.randint(0, app.sirina - 1)
            self.vy = random.randint(0, app.visina - 1)
            attempts += 1
            if attempts > 100:
                break

class Zmija:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xtacke_zmije = [x - 2, x - 1]
        self.ytacke_zmije = [y, y]

    def SudarSaZidom(self, app, x, y):
        return x < 0 or x >= app.sirina or y < 0 or y >= app.visina

    def SudarSaTelom(self, x, y):
        return any(x == self.xtacke_zmije[i] and y == self.ytacke_zmije[i] for i in range(len(self.xtacke_zmije)))

    def Njam(self, jabuka, app):
        app.prozor.fill((0, 0, 0))
        pygame.draw.rect(app.prozor, (250, 0, 0), (jabuka.vx * app.a, jabuka.vy * app.a, app.a, app.a))
        self.xtacke_zmije.append(self.x)
        self.ytacke_zmije.append(self.y)
        app.NacrtajGrid()
        for i in range(len(self.xtacke_zmije)):
            pygame.draw.rect(app.prozor, (255, 255, 255), (self.xtacke_zmije[i] * app.a, self.ytacke_zmije[i] * app.a, app.a, app.a))
        pygame.display.update()

def GlavniDeo():
    global brojep, highscore
    vreme = 10

    app = Uopsteno(A, VISINA, SIRINA)
    polje = Sumica(Zmija(SIRINA // 2, VISINA // 2), Jabucica(app), app)

    zmijica, kruska, done, nagrada, stanje = polje.reset(app)
    kruska.NapraviVoce(zmijica, app)
    polje.render(zmijica, kruska, app)

    Q_path = "q_matrica.npy"
    if os.path.exists(Q_path):
        Q = np.load(Q_path)
    else:
        Q = np.zeros((MAXSTANJE, 4))

    alpha = 0.9
    gamma = 0.9
    epsilon = 0.6

    run = True
    sat = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_time += sat.get_rawtime()
        sat.tick()

        if fall_time >= vreme:
            fall_time = 0

            action = random.randint(0, 3) if random.uniform(0, 1) < epsilon else np.argmax(Q[stanje])
            sledece_stanje, nagrada, done, _ = polje.step(action, zmijica, kruska)

            stara_vrednost = Q[stanje][action]
            if sledece_stanje < 0 or sledece_stanje >= MAXSTANJE:
                nova_vrednost = (1 - alpha) * stara_vrednost + alpha * (nagrada + gamma * (-100))
                Q[stanje][action] = nova_vrednost
                done = True
            else:
                nova_vrednost = (1 - alpha) * stara_vrednost + alpha * (nagrada + gamma * max(Q[sledece_stanje]))
                Q[stanje][action] = nova_vrednost
                stanje = sledece_stanje
                polje.render(zmijica, kruska, app)

            if done:
                zmijica, kruska, done, nagrada, sledece_stanje = polje.reset(app)
                Q[stanje][action] = (1 - alpha) * Q[stanje][action] + alpha * (nagrada + gamma * np.max(Q[sledece_stanje]))
                stanje = sledece_stanje
                brojep += 1
                if epsilon > 0.3:
                    epsilon -= 0.002
                if brojep == 1000:
                    epsilon = 0
                    vreme = 200
                print('gotovo', brojep)
                polje.render(zmijica, kruska, app)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                np.save(Q_path, Q)
                pygame.quit()
                return

GlavniDeo()

plt.xlabel('Epizoda')
plt.ylabel('Score')
plt.plot(epbroj, rekord)
plt.show()
pygame.quit()
