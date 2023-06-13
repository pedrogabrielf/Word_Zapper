import pygame
import sys
import string
import random
import os
from pathlib import Path
# Classe principal do jogo 
class principal:
    def __init__(self,posicao_inicial_x,posicao_inicial_y,velocidade):
        espaconave = pygame.image.load(caminho_arquivo('naveEspacial.png'))
        self.nave = pygame.transform.scale(espaconave, (75,75))
        self.rect = pygame.Rect(posicao_inicial_x, posicao_inicial_y, self.nave.get_width(), self.nave.get_height())
        self.rect.topleft = posicao_inicial_x,posicao_inicial_y
        self.velocidade = velocidade
        self.tiro_disparado = False

    # Funcao para movimentacao da nave
    def move(self):
        window.blit(self.nave,self.rect)

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
            if self.rect.x < -5:
                self.rect.x += self.velocidade

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
            if self.rect.x >= 1210:
                self.rect.x -= self.velocidade

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rect.y += self.velocidade
            if self.rect.y >= 525:
                self.rect.y -= self.velocidade

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.rect.y -= self.velocidade
            if self.rect.y < 150:
                self.rect.y += self.velocidade


    # Fucao para o tiro 
    def tiro(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.tiro_disparado:
            tiro = disparo(self.rect.center[0],self.rect.top)
            grupoTiros.add(tiro)

            self.tiro_disparado = True
        elif not pygame.key.get_pressed()[pygame.K_SPACE]:
            self.tiro_disparado = False

 # Funcao coringa para todos os botoes
class botao():
    def __init__(self,texto,x,y,largura,altura,funcao):

        self.clicou = False

        # Especifica o retangulo que sera desenhado
        self.retanguloConteiner = pygame.Rect(x,y,largura,altura)
        self.corBotao = (100,100,100)

        # escreve o texto na superficie
        self.texto = fonte_texto.render(texto,True,(255,255,0))
        # Obtem o tamanho do texto e o guarda dentro do retangulo que ira conter-lo
        self.retanguloTamnhoTexto = self.texto.get_rect(center=(self.retanguloConteiner.centerx, self.retanguloConteiner.centery))

        self.funcao = funcao

    def desenha_botao(self):
        # Desenha o retangulo especificado
        pygame.draw.rect(window,self.corBotao,self.retanguloConteiner,border_radius=10)
        # Coloca o retangulo na tela
        window.blit(self.texto,self.retanguloTamnhoTexto)

    def click(self):

        # Obtem a posição do mouse
        mouse = pygame.mouse.get_pos()

        # Verifica se o mouse esta dentro do botão
        if self.retanguloConteiner.collidepoint(mouse):
            
            # Muda a cor do botão quando o mouse esta dentro dele
            self.corBotao = (55,55,55)

            # Verifica se foi clicado com o botao direito
            if pygame.mouse.get_pressed()[0]:
                # Significa que ele clicou e somente uma booleana ira ser atribuida a essa variavel
                self.clicou = True
                
            # Quando a condição acima deixar de ser verdadeira ou seja o player deixou de pressionar o botao então a booleana volta a ser falsa por padrao e se executa a ação
            else:
                # Isso é feito dessa forma por conta de que ao se colocar uma grande quantidade de frames na execução do jogo essa ação seria executada varias vezes o que pode comprometer a performace do jogo em determinados dispositivos
                if self.clicou == True:
                    self.clicou = False
                    self.funcao()
        else:
            self.corBotao = (200,100,0)

class alfabeto():
    def __init__(self,letra, fonteLetra, Retangulo, velocidade, larguraFonte, alturaFonte):
        self.letra = letra
        self.fonteLetra = fonteLetra
        self.retangulo = Retangulo
        self.velocidade = velocidade
        self.larguraFonte = larguraFonte
        self.alturaFonte = alturaFonte
        self.cor = (255,255,255)
        self.colidiu = False

    def desenha_alfabeto_movendo(self):
        
        letraTela = self.fonteLetra.render(self.letra, True, self.cor)
        window.blit(letraTela, self.retangulo)

        self.retangulo.x -= self.velocidade

        if self.retangulo.x < 0:
            self.retangulo.x = 1700
            self.cor = (255,255,255)
            self.colidiu = False


class disparo(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        disparo = pygame.image.load(caminho_arquivo('Flame5.png'))
        self.image = pygame.transform.scale(disparo,(20,15))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        global listaOpcoes
        global palavraSorteada
        global letrasPalavra
        global venceu
        global listaVerificacao

        #Vel disparo
        self.rect.y -= 10

        # Configs colisao
        for i in range(26):
            
            if self.rect.colliderect(listaOpcoes[i].retangulo) and not listaOpcoes[i].colidiu:
                self.kill()
                listaOpcoes[i].cor = (0,0,0)

                listaOpcoes[i].colidiu = True

                if listaOpcoes[i].letra in palavraSorteada:
                    for letra in range (len(palavraSorteada)):
                        if palavraSorteada[letra] == listaOpcoes[i].letra:
                            letrasPalavra[letra].letra = palavraSorteada[letra]
                            listaVerificacao[letra] = palavraSorteada[letra]
                            print(listaVerificacao)
                            if "_" not in listaVerificacao:
                                venceu = True

        if self.rect.y < 0:  
            self.kill()


# Classe para a palavra sorteada
class letra():
    def __init__(self,letra,fonteUsada,x,y,larguraFonte,alturaFonte):
        self.letra = letra
        self.fonteUsada = fonteUsada
        self.x = x
        self.y = y
        self.larguraFonte = larguraFonte
        self.alturaFonte = alturaFonte
        self.cor = (0,0,0)

    # Desenhas as letras da palavra sorteada para o jogador ver as letras que tera que acertar !

    def desenha_letras_alfabeto(self):
        retangulo = pygame.draw.rect(window,(85, 232, 84),(self.x,620,self.larguraFonte,self.alturaFonte), border_radius=10)

        letraTela = self.fonteUsada.render(self.letra, True, self.cor)

        x_letra = retangulo.centerx - letraTela.get_width() // 2
        y_letra = retangulo.centery - letraTela.get_height() // 2

        # Desenha a letra na posição correta
        window.blit(letraTela, (x_letra, y_letra))


#Funcao para escrever textos na tela 
def escreve_texto(texto,fonte,corTexto,posicaoX,posicaoY):
    textoEscrito = fonte.render(texto,True,corTexto)
    window.blit(textoEscrito,(posicaoX,posicaoY))

#Funcao para sortear palavras da lista de palavras
def sorteia_palavra():
    with open("Word_Zapper/palavras.txt", encoding="utf-8 ") as arquivo: # Lê o arquivo na forma de "utf-8"
        palavras = arquivo.readlines() # Lê cada linha do arquivo e guarda elas em uma lista
        palavras = list(map(str.strip, palavras)) # Remove possiveis espaços em brancono inicio e no final da lista
        palavraSorteada = random.choice(palavras).upper() # padroniza a palavra sorteada para que todas as letras sejam minusculas
    return palavraSorteada


def paraJogar():
    global jogar, venceu
    jogar = True
    
def jogarFalse():
    global jogo
    jogo = False

def caminho_arquivo(nome):
    caminho = os.getcwd()
    caminhoAbsoluto = os.path.join(caminho, "Word_Zapper/img", nome)
    caminhoAbsoluto = Path(caminhoAbsoluto)
    return caminhoAbsoluto

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    relogio = pygame.time.Clock()

    largura = 1280
    altura = 720

    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("WordZapper")

    #fonte texto
    fonte_texto = pygame.font.SysFont("arial", 30)

    botaojogar = botao("JOGAR", 530, 275, 200, 100, paraJogar)
    botaoQUIT = botao("QUIT", 575,450,100,100,jogarFalse)

    botaojogarDNV = botao("JOGAR NOVAMENTE", 530, 275, 300, 100, paraJogar)

    #configs background
    tamanho_bg= (55,55)
    bg = pygame.image.load(caminho_arquivo('background_space.png'))
    bg = pygame.transform.scale(bg, (largura,altura))

    bgInicio = pygame.image.load(caminho_arquivo('fundo2.jpg'))
    bgInicio = pygame.transform.scale(bgInicio, (largura,altura))

    fonteAlfabeto = pygame.font.Font(caminho_arquivo("fonte.ttf"),50)
    fonteLetrasPalavraSorteada = pygame.font.Font(caminho_arquivo("fonte.ttf"),50)
    # Tg exemplo de fonte que e utilizado
    larguraFontePalavraSorteada = fonteLetrasPalavraSorteada.size("Ym")[0]
    alturaFontePalavraSorteada = fonteLetrasPalavraSorteada.size("Ym")[1]

    larguraFonteAlfabeto = fonteAlfabeto.size("Ym")[0]
    alturaFonteAlfabeto = fonteAlfabeto.size("Ym")[1]

    listaAlfabeto = list(string.ascii_uppercase)

    listaRetangulos = []

    xRetangulosConteiners = 50

    letrasPalavra = []

    grupoTiros = pygame.sprite.Group()

    palavraSorteada = sorteia_palavra()

    caminho = os.getcwd()

    # Seta alfabeto na tela e a respectiva distantia entre as letras e tambem altura
    for i in range(26):
        listaRetangulos.append(pygame.Rect(xRetangulosConteiners,75,larguraFonteAlfabeto,alturaFonteAlfabeto))
        xRetangulosConteiners += 65

    listaOpcoes = []
    
    #configs alfabeto
    for i in range(26):
        listaOpcoes.append(alfabeto(listaAlfabeto[i],fonteAlfabeto,listaRetangulos[i],5,larguraFonteAlfabeto,alturaFonteAlfabeto))

    largura = (larguraFontePalavraSorteada + 10) * len(palavraSorteada)

    # Retangulo da palavra sorteada 
    xRetanguloLetraAtual = int(580 - largura / 2)
    
    backup = xRetanguloLetraAtual

    letrasPalavra = []
  
    listaVerificacao = []

    for i in range(len(palavraSorteada)):
        letrasPalavra.append(letra(palavraSorteada[i],fonteLetrasPalavraSorteada,xRetanguloLetraAtual,550,larguraFontePalavraSorteada,alturaFontePalavraSorteada))

        xRetanguloLetraAtual += (larguraFontePalavraSorteada + 30)


    player = principal(370,400,5)

    jogar = False
    jogo = True
    contador = True
    venceu = False
    
    while jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if jogar:
            if venceu:
                window.blit(bgInicio, (0,0))
                botaojogarDNV.desenha_botao()
                botaojogarDNV.click()
                botaoQUIT.desenha_botao()
                botaoQUIT.click()
            
            else:
                if contador:
                    # Tempo para ver a palavra
                    tempo = pygame.time.get_ticks()
                    if tempo > 3000:
                        for i in range(len(palavraSorteada)):

                            if palavraSorteada != "-":
                                letrasPalavra[i].letra = "_"
                                listaVerificacao.append("_")
                            else:
                                letrasPalavra[i].letra = "-"
                                listaVerificacao.append("-")

                        contador = False

                window.blit(bg,(0,0))

                for i in range(26):
                    listaOpcoes[i].desenha_alfabeto_movendo()

                
                for i in range(len(palavraSorteada)):
                    letrasPalavra[i].desenha_letras_alfabeto()

                player.move()
                player.tiro()

                grupoTiros.draw(window)

                grupoTiros.update()

        else:
            window.blit(bgInicio, (0,0))
            botaojogar.desenha_botao()
            botaojogar.click()

            botaoQUIT.desenha_botao()
            botaoQUIT.click()

        pygame.display.update()
        relogio.tick(60)