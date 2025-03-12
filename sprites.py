import math
import random
import pygame as pg
from config import *

class Spritesheet:
    def __init__(self, file):
        self.sheet = pg.image.load(file).convert_alpha()

    def getSprite(self, x, y, width, height):
        sprite = pg.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        return sprite


class Jogador(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = CAMADA_JOGADOR
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TAMANHO_PISO
        self.y = y * TAMANHO_PISO

        self.width = TAMANHO_PISO
        self.height = TAMANHO_PISO

        self.exibicao = 'down'
        self.loop_animacao = 1

        self.image = self.game.personagem_spritesheet.getSprite(0, 0, self.width, self.height)
        self.jogadorEsquerda = Spritesheet('sprites/personagemSprite/characterFlip.png')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.y_change = 0

        self.down_animations = [self.game.personagem_spritesheet.getSprite(0, 0, self.width, self.height),
                           self.game.personagem_spritesheet.getSprite(34, 1, self.width, self.height),
                           self.game.personagem_spritesheet.getSprite(98, 1, self.width, self.height)]

        self.up_animations = [self.game.personagem_spritesheet.getSprite(0, 71, self.width, self.height),
                         self.game.personagem_spritesheet.getSprite(34, 71, self.width, self.height),
                         self.game.personagem_spritesheet.getSprite(97, 71, self.width, self.height)]

        self.left_animations = [self.jogadorEsquerda.getSprite(133, 37, self.width, self.height),
                           self.jogadorEsquerda.getSprite(167, 37, self.width, self.height),
                           self.jogadorEsquerda.getSprite(231, 37, self.width, self.height)]

        self.right_animations = [self.game.personagem_spritesheet.getSprite(7, 36, self.width, self.height),
                            self.game.personagem_spritesheet.getSprite(40, 36, self.width, self.height),
                            self.game.personagem_spritesheet.getSprite(103, 36, self.width, self.height)]


        self.velocidade_jogador=2.5
    def update(self):
        self.movement()
        self.animate()
        self.collideInimigo()
        self.rect.x += self.x_change
        self.collideBlocks('x')
        self.rect.y += self.y_change
        self.collideBlocks('y')

    def movement(self):
        teclas = pg.key.get_pressed()
        self.x_change = 0
        self.y_change = 0

        if (teclas[pg.K_q]):
            self.velocidade_jogador+=0.1

        if (teclas[pg.K_LEFT] or teclas[pg.K_a]):
            self.x_change -= self.velocidade_jogador
            self.exibicao = 'left'
            print(self.exibicao)

        if (teclas[pg.K_RIGHT] or teclas[pg.K_d]):
            self.x_change += self.velocidade_jogador
            self.exibicao = 'right'
            print(self.exibicao)

        if (teclas[pg.K_DOWN] or teclas[pg.K_s]):
            self.y_change += self.velocidade_jogador
            self.exibicao = 'down'
            print(self.exibicao)

        if (teclas[pg.K_UP] or teclas[pg.K_w]):
            self.y_change -= self.velocidade_jogador
            self.exibicao = 'up'
            print(self.exibicao)

    def collideInimigo(self):
        hitsBox = pg.sprite.spritecollide(self, self.game.inimigos, False)
        if hitsBox:
            self.kill()
            self.game.jogando = False

    def collideBlocks(self, direction):
        if direction == "x":
            hitsBox = pg.sprite.spritecollide(self, self.game.blocos, False)
            if hitsBox:
                if self.x_change > 0:
                    self.rect.x = hitsBox[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hitsBox[0].rect.right
        if direction == "y":
            hitsBox = pg.sprite.spritecollide(self, self.game.blocos, False)
            if hitsBox:
                if self.y_change > 0:
                    self.rect.y = hitsBox[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hitsBox[0].rect.bottom

    def animate(self):

        if self.exibicao == "down":
            if self.y_change == 0:
                self.image = self.game.personagem_spritesheet.getSprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor((self.loop_animacao))]
                self.loop_animacao += 0.1
                if self.loop_animacao >= 3:
                    self.loop_animacao = 1

        if self.exibicao == "up":
            if self.y_change == 0:
                self.image = self.game.personagem_spritesheet.getSprite(0, 71, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor((self.loop_animacao))]
                self.loop_animacao += 0.1
                if self.loop_animacao >= 3:
                    self.loop_animacao = 1

        if self.exibicao == "left":
            if self.x_change == 0:
                self.image = self.jogadorEsquerda.getSprite(133, 37, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor((self.loop_animacao))]
                self.loop_animacao += 0.1
                if self.loop_animacao >= 3:
                    self.loop_animacao = 1

        if self.exibicao == "right":
            if self.x_change == 0:
                self.image = self.game.personagem_spritesheet.getSprite(7, 36, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor((self.loop_animacao))]
                self.loop_animacao += 0.1
                if self.loop_animacao >= 3:
                    self.loop_animacao = 1


class Inimigo(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = CAMADA_INIMIGO
        self.groups = self.game.all_sprites, self.game.inimigos
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TAMANHO_PISO
        self.y = y * TAMANHO_PISO
        self.width = TAMANHO_PISO
        self.height = TAMANHO_PISO

        self.x_change = 0
        self.y_change = 0

        self.exibicao = random.choice(['left', 'right'])
        self.animacao_loop = 1
        self.movimento_loop = 0
        self.max_trajeto = random.randint(-320, 150)

        self.image = self.game.inimigo_spritesheet.getSprite(2, 0, self.width, self.height)
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.left_animations = [self.game.inimigo_spritesheet.getSprite(1, 30, self.width, self.height),
                           self.game.inimigo_spritesheet.getSprite(35, 30, self.width, self.height),
                           self.game.inimigo_spritesheet.getSprite(66, 30, self.width, self.height)]

        self.right_animations = [self.game.inimigo_spritesheet.getSprite(1, 62, self.width, self.height),
                            self.game.inimigo_spritesheet.getSprite(32, 62, self.width, self.height),
                            self.game.inimigo_spritesheet.getSprite(64, 62, self.width, self.height)]

    def update(self):
        self.animate()
        self.moviment()

        self.x_change = 0
        self.y_change = 0

        self.rect.x = max(0, min(self.rect.x, LARGURA - self.width * 2))
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.height * 2))

    def moviment(self):
        if self.exibicao == "left":
            self.x_change -= VELOCIDADE_INIMIGO
            self.movimento_loop -= 1
            if self.movimento_loop <= self.max_trajeto:
                self.exibicao = "right"
                self.max_trajeto = random.randint(-320, 150)

        if self.exibicao == "right":
            self.x_change += VELOCIDADE_INIMIGO
            self.movimento_loop += 1
            if self.movimento_loop >= self.max_trajeto:
                self.exibicao = "left"
                self.max_trajeto = random.randint(-320, 150)

        '''if self.exibicao == "up":
            self.y_change += VELOCIDADE_INIMIGO
            self.movimento_loop += 1
            if self.movimento_loop >= self.max_trajeto:
                self.exibicao = "down"
                self.max_trajeto = random.randint(50, 100)

        if self.exibicao == "down":
            self.y_change -= VELOCIDADE_INIMIGO
            self.movimento_loop -= 1
            if self.movimento_loop >= self.max_trajeto:
                self.exibicao = "up"
                self.max_trajeto = random.randint(50, 50)
    '''
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    def collideBlocks(self):
        hitsBox = pg.sprite.spritecollide(self, self.game.blocos, False)
        for block in hitsBox:
            if self.x_change > 0:
                self.rect.right = block.rect.left
            elif self.x_change < 0:
                self.rect.left = block.rect.right

            if self.y_change > 0:
                self.rect.bottom = block.rect.top
            elif self.y_change < 0:
                self.rect.top = block.rect.bottom

    def animate(self):

        if self.exibicao == "left":
            if self.x_change == 0:
                self.image = self.game.inimigo_spritesheet.getSprite(1, 30, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor((self.loop_animacao))]
                self.loop_animacao += 0.1
                if self.loop_animacao >= 3:
                    self.loop_animacao = 1

        if self.exibicao == "right":
            if self.x_change == 0:
                self.image = self.game.inimigo_spritesheet.getSprite(1, 62, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor((self.loop_animacao))]
                self.loop_animacao += 0.1
                if self.loop_animacao >= 3:
                    self.loop_animacao = 1


class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = CAMADA_BLOCO
        self.groups = self.game.all_sprites, self.game.blocos
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TAMANHO_PISO
        self.y = y * TAMANHO_PISO

        self.width = TAMANHO_PISO
        self.height = TAMANHO_PISO

        self.image = self.game.bloco_spritesheet.getSprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Chao(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.chao = CAMADA_CHAO
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TAMANHO_PISO
        self.y = y * TAMANHO_PISO
        self.width = TAMANHO_PISO
        self.height = TAMANHO_PISO

        self.image = self.game.chao_spritesheet.getSprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Botao:
    def __init__(self, x, y, width, height, fg, bg, content, fontSize):
        self.font = pg.font.Font('sprites/leadcoat.ttf', fontSize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pg.Surface((self.width, self.height))
        self.image.fill(self.bg)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def pressionar(self, position, mouse_pressed):
        if self.rect.collidepoint(position):
            if mouse_pressed[0]:
                return True
            return False
        return False


class Ataque(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = CAMADA_JOGADOR
        self.groups = self.game.all_sprites, self.game.ataques
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TAMANHO_PISO
        self.height = TAMANHO_PISO

        self.animacao_loop = 0

        self.image = self.game.ataque_spritesheet.getSprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.ataque_spritesheet.getSprite(0, 32, self.width, self.height),
                                self.game.ataque_spritesheet.getSprite(32, 32, self.width, self.height),
                                self.game.ataque_spritesheet.getSprite(64, 32, self.width, self.height),
                                self.game.ataque_spritesheet.getSprite(96, 32, self.width, self.height),
                                self.game.ataque_spritesheet.getSprite(128, 32, self.width, self.height)]

        self.up_animations = [self.game.ataque_spritesheet.getSprite(0, 0, self.width, self.height),
                              self.game.ataque_spritesheet.getSprite(32, 0, self.width, self.height),
                              self.game.ataque_spritesheet.getSprite(64, 0, self.width, self.height),
                              self.game.ataque_spritesheet.getSprite(96, 0, self.width, self.height),
                              self.game.ataque_spritesheet.getSprite(128, 0, self.width, self.height)]

        self.left_animations = [self.game.ataque_spritesheet.getSprite(0, 96, self.width, self.height),
                                self.game.ataque_spritesheet.getSprite(32, 96, self.width, self.height),
                                self.game.ataque_spritesheet.getSprite(64, 96, self.width, self.height),
                                self.game.ataque_spritesheet.getSprite(96, 96, self.width, self.height),
                                self.game.ataque_spritesheet.getSprite(128, 96, self.width, self.height)]

        self.right_animations = [self.game.ataque_spritesheet.getSprite(0, 64, self.width, self.height),
                                 self.game.ataque_spritesheet.getSprite(32, 64, self.width, self.height),
                                 self.game.ataque_spritesheet.getSprite(64, 64, self.width, self.height),
                                 self.game.ataque_spritesheet.getSprite(96, 64, self.width, self.height),
                                 self.game.ataque_spritesheet.getSprite(128, 64, self.width, self.height)]
    def update(self):

        self.animate()
        self.collide()

    def collide(self):

        hitsBox = pg.sprite.spritecollide(self, self.game.inimigos, True)

        if hitsBox:
            self.game.pontos=self.game.pontos+1
            print("inimigo morreu")
            print(self.game.pontos)

        if self.game.pontos == 10:
            print("venceu")
            self.game.venceu = True

    def animate(self):
        direction = self.game.jogador.exibicao

        if direction == "up":
            self.image = self.up_animations[math.floor(self.animacao_loop)]
            self.animacao_loop += 0.5

            if self.animacao_loop >= 5:
                self.kill()

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animacao_loop)]
            self.animacao_loop += 0.5

            if self.animacao_loop >= 5:
                    self.kill()

        if direction == "left":
            self.image = self.left_animations[math.floor(self.animacao_loop)]
            self.animacao_loop += 0.5

            if self.animacao_loop >= 5:
                    self.kill()

        if direction == "right":
            self.image = self.right_animations[math.floor(self.animacao_loop)]
            self.animacao_loop += 0.5

            if self.animacao_loop >= 5:
                    self.kill()
