import pygame
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

pygame.init()

a = 25
visina = 10
sirina = 10
highscore = 0
brojep = 0
rekord = []
epbroj = []

class Sumica(object):
    global highscore

    def __init__(self, zmijica, voce, app):

        self.n = 0
        self.w = 0

        self.sever = [zmijica.x, zmijica.y - 1]
        self.s = 0

        self.jug = [zmijica.x, zmijica.y + 1]
        self.j = 0

        self.zapad = [zmijica.x - 1, zmijica.y]
        self.z = 1

        self.istok = [zmijica.x + 1, zmijica.y]
        self.i = 0

        self.state = [ self.n, self.w, self.s, self.j, self.z, self.i]

        #(north, west) = jabuka, (sever, jug, zapad, istok) = prepreke da/ne

##        self.x1 = random.randint(0,1)
##        if self.x1 == 0:
##            if random.uniform(0, 1) < 0.5:
##                self.y1 = 1
##            else:
##                self.y1 = -1
##        else:
##            self.y1 = 0
        self.x1 = 1
        self.y1 = 0

    def encode(self, app):
        # north i west jabuka north = 0 ako jeste severno, north = 1 ako je tacno na osi, north = 2 ako je juzno,  slicno vazi za west
        # sever, jug, zapad, istok kvadratici prepreke oko glave gde je 1 da a 0 ne      
        i = self.state[0]
       
        i *= 3
        i += self.state[1]
       
        i *= 2
        i += self.state[2]
       
        i *= 2
        i += self.state[3]
       
        i *= 2
        i += self.state[4]
       
        i *= 2
        i += self.state[5]
        return i

    def step(self, action, zmijica, voce):

        nagrada = 0

        # 0 je levo
        if action == 0:
                if self.x1 != 1:
                    self.x1 = -1
                    self.y1 = 0
                else:
                    nagrada -= 100

        # 1 je desno
        if action == 1:
                if self.x1 != -1:
                    self.x1 = 1
                    self.y1 = 0
                else:
                    nagrada -= 100
                   
        # 2 je gore
        if action == 2:
                if self.y1 != 1:
                    self.x1 = 0
                    self.y1 = -1
                else:
                    nagrada -= 100
                   
        # 3 je dole
        if action == 3:
                if self.y1 != -1:
                    self.x1 = 0
                    self.y1 = 1
                else:
                    nagrada -= 100
       

        if (abs(zmijica.x - voce.vx) > abs(zmijica.x + self.x1 - voce.vx)):
            nagrada += 20
        elif (abs(zmijica.x - voce.vx) < abs(zmijica.x + self.x1 - voce.vx)):
            nagrada -= 20
        if (abs(zmijica.y - voce.vy) > abs(zmijica.y + self.y1 - voce.vy)):
            nagrada += 20
        elif (abs(zmijica.y - voce.vy) < abs(zmijica.y + self.y1 - voce.vy)):
            nagrada -= 20

        zmijica.x += self.x1
        zmijica.y += self.y1

        if ((zmijica.x == voce.vx) and (zmijica.y == voce.vy)):
            nagrada += 200

        # north i west jabuka north = 0 ako jeste severno, north = 1 ako je tacno na osi, north = 2 ako je juzno,  slicno vazi za west

        if (zmijica.y == voce.vy):
            self.n = 1
        elif (zmijica.y > voce.vy):
            self.n = 0
        else:
            self.n = 2

        self.state[0] = self.n

        if (zmijica.x == voce.vx):
            self.w = 1
        elif (zmijica.x > voce.vx):
            self.w = 0
        else:
            self.w = 2

        self.state[1] = self.w

        # gleda 4 kvadratica oko glave zmije:

        self.sever = [zmijica.x, zmijica.y - 1]
        if (zmijica.SudarSaZidom(app, self.sever[0], self.sever[1]) or zmijica.SudarSaTelom(self.sever[0], self.sever[1])):
            self.s = 1
        else:
            self.s = 0
        if ((self.sever[0] == voce.vx) and (self.sever[1] == voce.vy)):
            nagrada += 30
           
        self.state[2] = self.s


        self.jug = [zmijica.x, zmijica.y + 1]
        if (zmijica.SudarSaZidom(app, self.jug[0], self.jug[1]) or zmijica.SudarSaTelom(self.jug[0], self.jug[1])):
            self.j = 1
        else:
            self.j = 0
        if ((self.jug[0] == voce.vx) and (self.jug[1] == voce.vy)):
            nagrada += 30

        self.state[3] = self.j
       

        self.zapad = [zmijica.x - 1, zmijica.y]
        if (zmijica.SudarSaZidom(app, self.zapad[0], self.zapad[1]) or zmijica.SudarSaTelom(self.zapad[0], self.zapad[1])):
            self.z = 1
        else:
            self.z = 0
        if ((self.zapad[0] == voce.vx) and (self.zapad[1] == voce.vy)):
            nagrada += 30

        self.state[4] = self.z

        self.istok = [zmijica.x + 1, zmijica.y]
        if (zmijica.SudarSaZidom(app, self.istok[0], self.istok[1]) or zmijica.SudarSaTelom(self.istok[0], self.istok[1])):
            self.i = 1
        else:
            self.i = 0
        if ((self.istok[0] == voce.vx) and (self.istok[1] == voce.vy)):
            nagrada += 30

        self.state[5] = self.i

        done = zmijica.SudarSaTelom(zmijica.x, zmijica.y) or zmijica.SudarSaZidom(app, zmijica.x, zmijica.y)
        if done:
            nagrada -= 100

        return self.state, nagrada, done, {}


    def reset(self, app):
        kruska = Jabucica(app)
        zmijica = Zmija(app.sirina//2, app.visina//2)
        self.state = [ 0, 0, 0, 0, 1, 0]
        self.x1 = 1
        self.y1 = 0
        return zmijica, kruska, False, 0, self.state  # done = False, nagrada = 0

    def render(self, zmijica, voce, app):
        if ((zmijica.x == voce.vx) and (zmijica.y == voce.vy)):
            zmijica.Njam(voce, app)
            zmijica.NapraviVoce(voce, app)
        else:
            zmijica.Crtaj(voce, app)

class Uopsteno(object):
    def __init__(self, a, visina, sirina):
        self.a = a
        self.visina = visina
        self.sirina = sirina
        self.prozor = pygame.display.set_mode((self.sirina * self.a, self.visina * self.a))

    def NacrtajGrid(self):
        for i in range(self.visina):
            for j in range(self.sirina):
                pygame.draw.line(self.prozor, (50, 50, 50), (i * self.a, 0), (i * self.a, 500))
                pygame.draw.line(self.prozor, (50, 50, 50), (0, j * self.a), (500, j * self.a))
        pygame.display.update()


class Jabucica(object):
    def __init__(self, app):
        self.vx = random.randint(0, app.sirina - 1)
        self.vy = random.randint(0, app.visina - 1)


class Zmija(object):

    global highscore
           
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xtacke_zmije = [self.x - 2, self.x - 1]
        self.ytacke_zmije = [self.y, self.y]

    def SudarSaZidom(self, app, x, y):
        if (x > app.sirina-1) or (x < 0) or (y > app.visina-1) or (y < 0):
            return True
        return False

    def SudarSaTelom(self, x, y):
        for i in range(len(self.xtacke_zmije)):
            if (x == self.xtacke_zmije[i]) and (y == self.ytacke_zmije[i]):
                return True
        return False

    def Crtaj(self, jabuka, app):

        global highscore
        global rekord
        global epbroj
       
        app.prozor.fill((0, 0, 0))

##        pygame.draw.rect(app.prozor, (50,40,40), (self.x * app.a, (self.y - 1) * app.a, app.a, app.a))
##        pygame.draw.rect(app.prozor, (50,40,40), (self.x * app.a, (self.y + 1) * app.a, app.a, app.a))
##        pygame.draw.rect(app.prozor, (50,40,40), ((self.x - 1) * app.a, self.y * app.a, app.a, app.a))
##        pygame.draw.rect(app.prozor, (50,40,40), ((self.x + 1) * app.a, self.y * app.a, app.a, app.a))
       
        app.NacrtajGrid()

        del self.xtacke_zmije[0]
        self.xtacke_zmije.append(self.x)

        del self.ytacke_zmije[0]
        self.ytacke_zmije.append(self.y)

        for i in range(len(self.xtacke_zmije)):
            pygame.draw.rect(app.prozor, (230, 230, 230), (self.xtacke_zmije[i] * app.a, self.ytacke_zmije[i] * app.a, app.a, app.a))

        pygame.draw.rect(app.prozor, (250, 0, 0), (jabuka.vx * app.a, jabuka.vy * app.a, app.a, app.a))

        #slika = pygame.image.load('apple.bmp')
        #app.prozor.blit(slika, (jabuka.vx * app.a, jabuka.vy * app.a, app.a, app.a))

        font = pygame.font.Font('freesansbold.ttf', 20)

        score = len(self.xtacke_zmije) - 2
        tekst = font.render('Score: ' + str(score), True, (255, 255, 255))
       
        if highscore < score:
            highscore = score
            rekord.append(highscore)
            epbroj.append(brojep)
            #print('rekord, broj ep = ', rekord[-1],' ', epbroj[-1])
           
        tekst1 = font.render('Highscore:' + str(highscore), True, (255, 255, 255))
       
        app.prozor.blit(tekst, (1, 1))
        app.prozor.blit(tekst1, (100, 1))
       
        pygame.display.update()

    def NapraviVoce(self, jabuka, app):
        while (self.SudarSaTelom(jabuka.vx, jabuka.vy)):
            jabuka.vx = random.randint(0, app.sirina - 1)
            jabuka.vy = random.randint(0, app.visina - 1)

    def Njam(self, jabuka, app):
        app.prozor.fill((0, 0, 0))

        pygame.draw.rect(app.prozor, (250, 0, 0), (jabuka.vx * app.a, jabuka.vy * app.a, app.a, app.a))

        self.xtacke_zmije.append(self.x)

        self.ytacke_zmije.append(self.y)

        app.NacrtajGrid()

        for i in range(len(self.xtacke_zmije)):
            pygame.draw.rect(app.prozor, (255, 255, 255),
                             (self.xtacke_zmije[i] * app.a, self.ytacke_zmije[i] * app.a, app.a, app.a))

        pygame.display.update()

class DQN():

    def __init__(self):

        self.alpha = 0.9
        self.gamma = .9
        self.epsilon = 0.6
        self.episodes = 100
        self.short_memory = np.array([])
        self.model = self.network()
        self.memory = []

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=6))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=4, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

def GlavniDeo():
    run = True
    sat = pygame.time.Clock()

    global brojep
    global highscore
    global app
    vreme = 10

    dqn = DQN()

    app = Uopsteno(a, visina, sirina)
    polje = Sumica(Zmija(app.visina//2, app.sirina//2), Jabucica(app), app)

    zmijica, kruska, done, nagrada, stanje = polje.reset(app)
    stanje = np.reshape(stanje, [1, 6])
   
    zmijica.NapraviVoce(kruska, app)
    polje.render(zmijica, kruska, app)

    fall_time = 0
    pygame.time.delay(500)

# broj stanja, mada ovde nije potrebno
    maxstanje = 144


                           
    while run:
       
        fall_time += sat.get_rawtime()
        sat.tick()

        if fall_time >= vreme:
            fall_time = 0

            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 3)
            else:
                action = np.argmax(dqn.model.predict(stanje)[0])
               
           
            sledece_stanje, nagrada, done, info = polje.step(action, zmijica, kruska)
            sledece_stanje = np.reshape(sledece_stanje, [1, 6])
            dqn.remember(stanje, action, nagrada, sledece_stanje)
            stanje = sledece_stanje

            polje.render(zmijica, kruska, app)

            if done:
                dqn.replay(dqn.memory)

                brojep += 1
               
                if (epsilon > 0.3):
                    epsilon -= 0.002
                if brojep == 1000:
                    epsilon = 0
                    vreme = 200
                     
                print('gotovo', brojep)            
                polje.render(zmijica, kruska, app)

               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

GlavniDeo()

plt.xlabel('epizoda')
plt.ylabel('score')

plt.plot(epbroj, rekord)
plt.show()

pygame.quit()
