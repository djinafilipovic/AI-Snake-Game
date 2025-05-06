import pygame
import random

pygame.init()

a = 25
visina = 20
sirina = 20


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


class Jabucica(object):
    def __init__(self, app):
        self.vx = random.randint(0, app.sirina - 1)
        self.vy = random.randint(0, app.visina - 1)


class Zmija(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xtacke_zmije = [self.x - 2, self.x - 1]
        self.ytacke_zmije = [self.y, self.y]

    def SudarSaZidom(self, app):
        if (self.x == app.sirina) or (self.x == -1) or (self.y == app.visina) or (self.y == -1):
            return True
        return False

    def SudarSaTelom(self, x, y):
        for i in range(len(self.xtacke_zmije)):
            if (x == self.xtacke_zmije[i]) and (y == self.ytacke_zmije[i]):
                return True
        return False

    def Crtaj(self, jabuka, app):

        app.prozor.fill((0, 0, 0))
        app.NacrtajGrid()

        del self.xtacke_zmije[0]
        self.xtacke_zmije.append(self.x)

        del self.ytacke_zmije[0]
        self.ytacke_zmije.append(self.y)

        for i in range(len(self.xtacke_zmije)):
            pygame.draw.rect(app.prozor, (230, 230, 230),
                             (self.xtacke_zmije[i] * app.a, self.ytacke_zmije[i] * app.a, app.a, app.a))

        pygame.draw.rect(app.prozor, (250, 0, 0), (jabuka.vx * app.a, jabuka.vy * app.a, app.a, app.a))

        font = pygame.font.Font('freesansbold.ttf', 20)
        tekst = font.render('Score: ' + str(len(self.xtacke_zmije) - 2), True, (255, 255, 255))
        app.prozor.blit(tekst, (200, 1))

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


def GlavniDeo():
    run = True
    sat = pygame.time.Clock()

    app = Uopsteno(a, visina, sirina)
    kruska = Jabucica(app)
    zmijica = Zmija(10, 10)

    x1 = 1
    y1 = 0

    zmijica.NapraviVoce(kruska, app)
    fall_time = 0

    zmijica.Crtaj(kruska, app)
    pygame.time.delay(500)

    while run:

        fall_time += sat.get_rawtime()
        sat.tick()

        if fall_time >= 200:
            fall_time = 0
            zmijica.x += x1
            zmijica.y += y1

            if zmijica.SudarSaTelom(zmijica.x, zmijica.y):
                print("telo")
                run = False
                GlavniDeo()

            zmijica.Crtaj(kruska, app)

        if (kruska.vx == zmijica.x) and (kruska.vy == zmijica.y):
            zmijica.Njam(kruska, app)
            zmijica.NapraviVoce(kruska, app)

        if zmijica.SudarSaZidom(app):
            print("zid")
            run = False
            GlavniDeo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x1 != 1:
                        x1 = -1
                        y1 = 0

                if event.key == pygame.K_RIGHT:
                    if x1 != -1:
                        x1 = 1
                        y1 = 0

                if event.key == pygame.K_UP:
                    if y1 != 1:
                        x1 = 0
                        y1 = -1

                if event.key == pygame.K_DOWN:
                    if y1 != -1:
                        x1 = 0
                        y1 = 1


GlavniDeo()
pygame.quit()