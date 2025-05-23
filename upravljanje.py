import pygame
import random

pygame.init()

a = 25
visina = 20
sirina = 20
replay = False

class Uopsteno(object):
    def __init__(self, a, visina, sirina):
        self.a = a
        self.visina = visina
        self.sirina = sirina
        self.prozor = pygame.display.set_mode((self.sirina * self.a, self.visina * self.a))

    def NacrtajGrid(self):
        for i in range(self.visina):
            for j in range(self.sirina):
                pygame.draw.line(self.prozor, (50, 50, 50), (i * self.a, 0), (i * a, 500))
                pygame.draw.line(self.prozor, (50, 50, 50), (0, j * self.a), (500, j * self.a))
        pygame.display.update()

    def cekaj_na_restart(self):
        global replay
        font = pygame.font.Font('freesansbold.ttf', 32)
        tekst = font.render("Pritisni 0 da igras ponovo", True, (255, 255, 255))
        self.prozor.blit(tekst, (50, 250))
        pygame.display.update()

        cekaj = True
        while cekaj:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        cekaj = False
                        replay = True

    def Crtaj(self, zmijica, jabuka):
        self.prozor.fill((0, 0, 0))
        self.NacrtajGrid()

        del zmijica.xtacke_zmije[0]
        zmijica.xtacke_zmije.append(zmijica.x)

        del zmijica.ytacke_zmije[0]
        zmijica.ytacke_zmije.append(zmijica.y)

        for i in range(len(zmijica.xtacke_zmije)):
            pygame.draw.rect(self.prozor, (230, 230, 230),
                             (zmijica.xtacke_zmije[i] * self.a, zmijica.ytacke_zmije[i] * self.a, self.a, self.a))

        pygame.draw.rect(self.prozor, (250, 0, 0), (jabuka.vx * self.a, jabuka.vy * self.a, self.a, self.a))

        font = pygame.font.Font('freesansbold.ttf', 20)
        tekst = font.render('Score: ' + str(len(zmijica.xtacke_zmije) - 2), True, (255, 255, 255))
        self.prozor.blit(tekst, (200, 1))

        pygame.display.update()

class Jabucica(object):
    def __init__(self, app):
        self.vx = random.randint(0, app.sirina - 1)
        self.vy = random.randint(0, app.visina - 1)

    def NapraviVoce(self, zmijica, app):
        while (zmijica.SudarSaTelom(self.vx, self.vy)):
            self.vx = random.randint(0, app.sirina - 1)
            self.vy = random.randint(0, app.visina - 1)

class Zmija(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xtacke_zmije = [self.x - 2, self.x - 1]
        self.ytacke_zmije = [self.y, self.y]

    def SudarSaZidom(self, app):
        return self.x < 0 or self.x >= app.sirina or self.y < 0 or self.y >= app.visina

    def SudarSaTelom(self, x, y):
        for i in range(len(self.xtacke_zmije)):
            if (x == self.xtacke_zmije[i]) and (y == self.ytacke_zmije[i]):
                return True
        return False

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


def GlavniDeo():
    run = True
    sat = pygame.time.Clock()
    global replay
    replay = False

    app = Uopsteno(a, visina, sirina)
    kruska = Jabucica(app)
    zmijica = Zmija(10, 10)

    x1 = 1
    y1 = 0

    kruska.NapraviVoce(zmijica, app)
    fall_time = 0

    app.Crtaj(zmijica, kruska)
    pygame.time.delay(500)

    while run:
        fall_time += sat.get_rawtime()
        sat.tick()

        if fall_time >= 200:
            fall_time = 0
            zmijica.x += x1
            zmijica.y += y1

            if zmijica.SudarSaTelom(zmijica.x, zmijica.y) or zmijica.SudarSaZidom(app):
                run = False
                app.cekaj_na_restart()
                return

            app.Crtaj(zmijica, kruska)

        if (kruska.vx == zmijica.x) and (kruska.vy == zmijica.y):
            zmijica.Njam(kruska, app)
            kruska.NapraviVoce(zmijica, app)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1 != 1:
                    x1 = -1
                    y1 = 0
                elif event.key == pygame.K_RIGHT and x1 != -1:
                    x1 = 1
                    y1 = 0
                elif event.key == pygame.K_UP and y1 != 1:
                    x1 = 0
                    y1 = -1
                elif event.key == pygame.K_DOWN and y1 != -1:
                    x1 = 0
                    y1 = 1

GlavniDeo()
while replay:
    GlavniDeo()

pygame.quit()
