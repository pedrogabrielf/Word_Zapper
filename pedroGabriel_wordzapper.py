import pygame
import sys
class botao():
    def __init__(self,texto,x,y,largura,altura,funcao):
        # Atributos padrões para verificações por motivos de performace
        self.clicou = False

        # Especifica o retangulo que sera desenhado
        self.retanguloConteiner = pygame.Rect(x,y,largura,altura)
        self.corBotao = (100,100,100)

        # escreve o texto na superficie
        self.texto = fonte_texto.render(texto,True,(255,255,255))
        # Obtem o tamanho do texto e o guarda dentro do retangulo que ira conter-lo
        self.retanguloTamnhoTexto = self.texto.get_rect(center=(self.retanguloConteiner.centerx, self.retanguloConteiner.centery))

        self.funcao = funcao

    def desenha_botao(self):
        # Desenha o retangulo especificado
        pygame.draw.rect(window,self.corBotao,self.retanguloConteiner,border_radius=10)
        # Coloca o retangulo na tela
        window.blit(self.texto,self.retanguloTamnhoTexto)

    def click(self):

        # Obtem a posição do maouse
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
                # Isso é feito dessa forma por conta de que aou se colocar uma grande quantidade de frames na execução do jogo essa ação seria executada varias vezes o que pode comprometer a performace do jogo em determinados dispositivos
                if self.clicou == True:
                    self.clicou = False
                    self.funcao()
        else:
            self.corBotao = (200,100,100)

def teste():
    global jogar
    jogar = True

def jogarFalse():
    global jogo
    jogo = False

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    relogio = pygame.time.Clock()

    largura = 1000
    altura = 700

    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("WordZapper")

    #fonte texto
    fonte_texto = pygame.font.SysFont("arial", 30)

    botaojogar = botao("JOGAR", 400, 275, 200, 100, teste)
    botaoQUIT = botao("QUIT", 450,450,100,100,jogarFalse)

    #configs background
    tamanho_bg= (55,55)
    bg = pygame.image.load('img/background_space2.png')
    bg = pygame.transform.scale(bg, (largura,altura))


    bgInicio = pygame.image.load('img/fundo2.jpg')
    bgInicio = pygame.transform.scale(bgInicio, (largura,altura))

    #configs nave principal
    velocidade_nave1 = 7
    posicao_nave1_x = 400
    posicao_nave1_y = 300
    tamanho_nave_principal = (95,95)
    nave_principal = pygame.image.load('img/navePrincipal.png')
    nave_principal = pygame.transform.scale(nave_principal, tamanho_nave_principal)

    jogar = False
    jogo = True
    while jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if jogar:
            # movimentacao da nave principal
            comandos = pygame.key.get_pressed()
            if comandos[pygame.K_UP]: #and posicao_frog_y >= 0:
                posicao_nave1_y -= velocidade_nave1
            if comandos[pygame.K_DOWN]: #and posicao_frog_y <= 535:
                posicao_nave1_y += velocidade_nave1
            if comandos[pygame.K_RIGHT]: #and posicao_frog_x <= 745:
                posicao_nave1_x += velocidade_nave1
            if comandos[pygame.K_LEFT]: #and posicao_frog_x >= 12:
                posicao_nave1_x -= velocidade_nave1

            window.blit(bg, (0, 0))
            window.blit(nave_principal, (posicao_nave1_x, posicao_nave1_y))
        
        else:
            window.blit(bgInicio, (0,0))

            botaojogar.desenha_botao()
            botaojogar.click()

            botaoQUIT.desenha_botao()
            botaoQUIT.click()
        pygame.display.update()
        relogio.tick(60)