# main.py
import asyncio
import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configurações da janela
LARGURA = 800
ALTURA = 600
janela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Jogo do Macaco")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
MARROM = (139, 69, 19)

class Macaco:
    def __init__(self):
        self.largura = 50
        self.altura = 50
        self.x = LARGURA // 4
        self.y = ALTURA - self.altura - 10
        self.velocidade_y = 0
        self.pulando = False
        self.gravidade = 0.8

    def pular(self):
        if not self.pulando:
            self.velocidade_y = -15
            self.pulando = True

    def atualizar(self):
        self.velocidade_y += self.gravidade
        self.y += self.velocidade_y

        if self.y > ALTURA - self.altura - 10:
            self.y = ALTURA - self.altura - 10
            self.velocidade_y = 0
            self.pulando = False

    def desenhar(self):
        pygame.draw.rect(janela, MARROM, (self.x, self.y, self.largura, self.altura))

class Banana:
    def __init__(self):
        self.largura = 30
        self.altura = 30
        self.x = LARGURA
        self.y = random.randint(100, ALTURA - 100)
        self.velocidade = 5

    def atualizar(self):
        self.x -= self.velocidade

    def desenhar(self):
        pygame.draw.rect(janela, AMARELO, (self.x, self.y, self.largura, self.altura))

class Obstaculo:
    def __init__(self):
        self.largura = 30
        self.altura = random.randint(100, 300)
        self.x = LARGURA
        self.y = ALTURA - self.altura
        self.velocidade = 5

    def atualizar(self):
        self.x -= self.velocidade

    def desenhar(self):
        pygame.draw.rect(janela, AZUL, (self.x, self.y, self.largura, self.altura))

async def main():
    macaco = Macaco()
    bananas = []
    obstaculos = []
    pontos = 0
    clock = pygame.time.Clock()
    tempo_ultimo_spawn = 0
    
    jogando = True
    while jogando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    macaco.pular()
            elif evento.type == pygame.FINGERDOWN:  # Suporte a toque
                macaco.pular()

        if pygame.time.get_ticks() - tempo_ultimo_spawn > 2000:
            if random.random() < 0.5:
                bananas.append(Banana())
            else:
                obstaculos.append(Obstaculo())
            tempo_ultimo_spawn = pygame.time.get_ticks()

        macaco.atualizar()
        
        for banana in bananas[:]:
            banana.atualizar()
            if banana.x < -banana.largura:
                bananas.remove(banana)
            elif (macaco.x < banana.x + banana.largura and
                  macaco.x + macaco.largura > banana.x and
                  macaco.y < banana.y + banana.altura and
                  macaco.y + macaco.altura > banana.y):
                bananas.remove(banana)
                pontos += 1

        for obstaculo in obstaculos[:]:
            obstaculo.atualizar()
            if obstaculo.x < -obstaculo.largura:
                obstaculos.remove(obstaculo)
            elif (macaco.x < obstaculo.x + obstaculo.largura and
                  macaco.x + macaco.largura > obstaculo.x and
                  macaco.y < obstaculo.y + obstaculo.altura and
                  macaco.y + macaco.altura > obstaculo.y):
                jogando = False

        janela.fill(BRANCO)
        macaco.desenhar()
        for banana in bananas:
            banana.desenhar()
        for obstaculo in obstaculos:
            obstaculo.desenhar()

        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f'Pontos: {pontos}', True, (0, 0, 0))
        janela.blit(texto, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)  # Necessário para web

    pygame.quit()

asyncio.run(main())
