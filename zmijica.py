import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

pygame.init()

# Globalne konstante
a = 25
visina = 10
sirina = 10
highscore = 0
brojep = 0
rekord = []
epbroj = []

import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

pygame.init()

a = 25
visina = 10
sirina = 10
highscore = 0
brojep = 0
rekord = []
epbroj = []

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

class Sumica:
    def __init__(self, zmijica, voce, app):
        self.n = 0
        self.w = 0
        self.s = 0
        self.j = 0
        self.z = 1
        self.i = 0
        self.state = [self.n, self.w, self.s, self.j, self.z, self.i]
        self.x1 = 1
        self.y1 = 0

    def encode(self):
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

    def step(self, action, zmijica, voce, app):
        nagrada = 0

        if action == 0 and self.x1 != 1:
            self.x1, self.y1 = -1, 0
        elif action == 1 and self.x1 != -1:
            self.x1, self.y1 = 1, 0
        elif action == 2 and self.y1 != 1:
            self.x1, self.y1 = 0, -1
        elif action == 3 and self.y1 != -1:
            self.x1, self.y1 = 0, 1
        else:
            nagrada -= 100

        if abs(zmijica.x - voce.vx) > abs(zmijica.x + self.x1 - voce.vx):
            nagrada += 20
        elif abs(zmijica.x - voce.vx) < abs(zmijica.x + self.x1 - voce.vx):
            nagrada -= 20

        if abs(zmijica.y - voce.vy) > abs(zmijica.y + self.y1 - voce.vy):
            nagrada += 20
        elif abs(zmijica.y - voce.vy) < abs(zmijica.y + self.y1 - voce.vy):
            nagrada -= 20

        zmijica.x += self.x1
        zmijica.y += self.y1

        if zmijica.x == voce.vx and zmijica.y == voce.vy:
            nagrada += 200

        self.n = 1 if zmijica.y == voce.vy else 0 if zmijica.y > voce.vy else 2
        self.w = 1 if zmijica.x == voce.vx else 0 if zmijica.x > voce.vx else 2

        self.sever = [zmijica.x, zmijica.y - 1]
        self.s = int(zmijica.SudarSaZidom(app, *self.sever) or zmijica.SudarSaTelom(*self.sever))
        if self.sever == [voce.vx, voce.vy]: nagrada += 30

        self.jug = [zmijica.x, zmijica.y + 1]
        self.j = int(zmijica.SudarSaZidom(app, *self.jug) or zmijica.SudarSaTelom(*self.jug))
        if self.jug == [voce.vx, voce.vy]: nagrada += 30

        self.zapad = [zmijica.x - 1, zmijica.y]
        self.z = int(zmijica.SudarSaZidom(app, *self.zapad) or zmijica.SudarSaTelom(*self.zapad))
        if self.zapad == [voce.vx, voce.vy]: nagrada += 30

        self.istok = [zmijica.x + 1, zmijica.y]
        self.i = int(zmijica.SudarSaZidom(app, *self.istok) or zmijica.SudarSaTelom(*self.istok))
        if self.istok == [voce.vx, voce.vy]: nagrada += 30

        self.state = [self.n, self.w, self.s, self.j, self.z, self.i]
        done = zmijica.SudarSaTelom(zmijica.x, zmijica.y) or zmijica.SudarSaZidom(app, zmijica.x, zmijica.y)
        if done:
            nagrada -= 100

        return self.state, nagrada, done, {}

    def reset(self, app):
        kruska = Jabucica(app)
        zmijica = Zmija(app.sirina // 2, app.visina // 2)
        self.state = [0, 0, 0, 0, 1, 0]
        self.x1 = 1
        self.y1 = 0
        return zmijica, kruska, False, 0, self.state

    def render(self, zmijica, voce, app):
        if zmijica.x == voce.vx and zmijica.y == voce.vy:
            zmijica.Njam(voce, app)
            voce.NapraviVoce(zmijica, app)
        else:
            app.Crtaj(zmijica, voce)


class DQN:
    def __init__(self):
        self.alpha = 0.9
        self.gamma = 0.9
        self.epsilon = 0.6
        self.learning_rate = 0.001
        self.episodes = 100
        self.model = self.network()
        self.memory = []

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(120, activation='relu', input_dim=6))
        model.add(Dropout(0.15))
        model.add(Dense(120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(4, activation='softmax'))
        opt = Adam(learning_rate=self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        minibatch = random.sample(self.memory, min(len(self.memory), 1000))
        for state, action, reward, next_state, done in minibatch:
            next_state = np.reshape(next_state, [1, 6])
            target = reward
            if not done:
                target += self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])

            state = np.reshape(state, [1, 6])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)


def GlavniDeo():
    global brojep, highscore
    run = True
    sat = pygame.time.Clock()
    vreme = 10

    dqn = DQN()
    app = Uopsteno(a, visina, sirina)
    polje = Sumica(Zmija(app.visina // 2, app.sirina // 2), Jabucica(app), app)

    zmijica, kruska, done, nagrada, stanje = polje.reset(app)
    stanje = np.reshape(stanje, [1, 6])

    kruska.NapraviVoce(zmijica, app)
    polje.render(zmijica, kruska, app)

    fall_time = 0
    pygame.time.delay(500)

    while run:
        fall_time += sat.get_rawtime()
        sat.tick()

        if fall_time >= vreme:
            fall_time = 0
            action = random.randint(0, 3) if random.uniform(0, 1) < dqn.epsilon else np.argmax(dqn.model.predict(stanje, verbose=0)[0])

            sledece_stanje, nagrada, done, _ = polje.step(action, zmijica, kruska, app)
            sledece_stanje = np.reshape(sledece_stanje, [1, 6])
            dqn.remember(stanje, action, nagrada, sledece_stanje, done)
            stanje = sledece_stanje

            polje.render(zmijica, kruska, app)

            if done:
                dqn.replay()
                brojep += 1
                if dqn.epsilon > 0.3:
                    dqn.epsilon -= 0.002
                if brojep == 1000:
                    dqn.epsilon = 0
                    vreme = 200
                print('Gotovo', brojep)
                zmijica, kruska, done, nagrada, stanje = polje.reset(app)
                stanje = np.reshape(stanje, [1, 6])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    plt.xlabel('epizoda')
    plt.ylabel('score')
    plt.plot(epbroj, rekord)
    plt.show()

GlavniDeo()
