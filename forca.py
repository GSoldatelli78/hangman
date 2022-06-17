import pygame
import math
import random

pygame.init()

# Setup do display
largura = 1366
altura = 768
dimensao = (largura, altura)
janela = pygame.display.set_mode(dimensao)
pygame.display.set_caption('Jogo da Forca')

# Variáveis das letras do jogo
raio = 25
gap = 20
letras = []
iniciox = round((largura - (raio * 2 + gap) * 13)/2)
inicioy = 550
A = 65
for i in range(26):
    posicaox = iniciox + gap * 2 + ((raio * 2 + gap) * (i % 13))
    posicaoy = inicioy + ((i // 13) * (gap + raio * 2))
    letras.append([posicaox,posicaoy, chr(A + i), True])

# Fontes
fonteLetras = pygame.font.SysFont('Unispace', 40)
fontePalavra = pygame.font.SysFont('Unispace', 60)
fonteTitulo = pygame.font.SysFont('Unispace', 80)
fonteMenu = pygame.font.SysFont('Unispace', 70)
fonteMenu2 = pygame.font.SysFont('Unispace', 50)
fonteAviso = pygame.font.SysFont('Unispace', 25)

# Cores
purple = (101,57,163)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
white = (255,255,255)

# Variáveis importantes
statusForca = 0
palavras_lista = ['PYTHON', 'PYGAME', 'LISTAS', 'CARRO', 'MERCADO', 'FORCA', 'GATO', 'DRAGAO', 'LULA', 'ORNINTORRINCO', 'PATO', 'PINGUIM', 'ONOMATOPEIA', 'OTORRINOLARINGOLOGISTA', 'CACHORRO', 'LUZ', 'ESCURO', 'PRETO', 'BRANCO', 'LARANJA', 'VERDE', 'VERMELHO', 'ERVA', 'CHIMARRAO', 'FUTEBOL', 'BASQUETE', 'VIDEOGAME', 'VAMPIRO', 'MARMOTA', 'CARROSSEL', 'GELATINA', 'LASANHA', 'CHOCOLATE', 'BOLA', 'COMIDA', 'SAPO']

tentativas = []


# Setup das imagens do jogo
vitoria = pygame.image.load('vitoria.png')
derrota = pygame.image.load('derrota.png')
imagens = []

for i in range(8):
    imagem = pygame.image.load('forca' + str(i) + '.png')
    imagens.append(imagem)

# Setup da tela
def jogar(type):
    janela.fill(purple)

    # Mostra o titulo na tela
    texto = fonteTitulo.render('Jogo da Forca', 1, black)
    janela.blit(texto, ((largura/2 - texto.get_width()/2), 50))
    
    # Desenha as palavras
    palavraTela = ''
    for letra in (type):
        if letra in tentativas:
            palavraTela += letra + ' '
        else:
            palavraTela += '_ '
    texto = fontePalavra.render(palavraTela, 1, black)
    janela.blit(texto, (550, 300))

    # Desenha os botões
    for letra in letras:
        posicaox, posicaoy, ltr, visivel = letra                                                                #Letra tem de ter posição x, posição y, a própria letra e se é visível ou não (True ou False)
        if visivel:
            pygame.draw.circle(janela, black, (posicaox, posicaoy), raio, 5)
            texto = fonteLetras.render(ltr, 1, black)
            janela.blit(texto, ((posicaox - texto.get_width()/2), (posicaoy - texto.get_height()/2 + 2)))
    janela.blit(imagens[statusForca], (175, 125))
    pygame.display.update()

# Mostra se o jogador ganhou ou perdeu
def mensagem_tela(mensagem, cor):
    pygame.time.delay(1000)
    janela.fill(black)
    texto = fontePalavra.render(mensagem, 1, cor)
    janela.blit(texto, ((largura/2 - texto.get_width()/2), (altura/2 - texto.get_height()/2)))
    pygame.display.update()
    pygame.time.delay(5000)

# Função de jogador contra CPU
def jogoCPU():
    global statusForca
    statusForca = statusForca - statusForca
    # Setup do looping do jogo
    FPS = 60
    clock = pygame.time.Clock()
    rodando = True
    palavra_random = random.choice(palavras_lista)

    while rodando:                                                                                                  
        clock.tick(FPS)                                                                                            

        for event in pygame.event.get():                                                                            # Looping que verifica eventos (ações) no jogo
            if event.type == pygame.QUIT:                                                                           # Fecha o jogo
                rodando = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:                                                                # Verifica cliques do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()    
                for letra in letras:
                    x, y, ltr, visivel = letra                                                                          
                    if visivel:
                        dist = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)                                       # Verifica a distância entre a posição das letras e os cliques no mouse           
                        if dist < raio:
                            letra[3] = False
                            tentativas.append(ltr)
                            if ltr not in palavra_random:
                                statusForca += 1
                                                                                                                                       
        jogar(palavra_random)
        
        venceu = True
        for letra in palavra_random:
            if letra not in tentativas:
                venceu = False
                break
        if venceu:
            for letra in letras:
                letra[3] = True
                mensagem_tela('Você VENCEU!', green)
                for letra in letras:
                    letra[3] = True
                main_menu()
        if statusForca == 7:       
                mensagem_tela('Você PERDEU!', red)
                for letra in letras:                                                                                # Repõe os botões na tela
                    letra[3] = True
                main_menu()

def jogoPVP():
    global statusForca
    statusForca = statusForca - statusForca
    # Setup do looping do jogo
    FPS = 60
    clock = pygame.time.Clock()
    rodando = True

    while rodando:                                                                                                  
        clock.tick(FPS)                                                                                             # Roda o jogo na taxa de atualização definida
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                                           # Fecha o jogo
                pygame.quit()                                                                                       
            if event.type == pygame.MOUSEBUTTONDOWN:                                                                # Verifica cliques do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letra in letras:                                                                                # Verifica a distância entre a posição das letras e os cliques no mouse
                    x, y, ltr, visivel = letra
                    if visivel:
                        dist = math.sqrt((x - mouse_x)**2 + (y - mouse_y)**2)
                        if dist < raio:
                            letra[3] = False
                            tentativas.append(ltr)
                            if ltr not in user_text:
                                statusForca += 1
        
        jogar(user_text)
        
        venceu = True
        for letra in user_text:
            if letra not in tentativas:
                venceu = False
                break
        if venceu:
                mensagem_tela('Você VENCEU!', green)
                for letra in letras:
                    letra[3] = True
                main_menu()
        if statusForca == 7:    
                mensagem_tela('Você PERDEU!', red)
                for letra in letras:
                    letra[3] = True
                main_menu()

def text_input():
    global user_text
    
    user_text = ''
    input_rect = pygame.Rect((largura/2 - 341.5), (altura/2 - 25), (largura/2), 50)   
    # Setup do looping do jogo
    FPS = 60
    clock = pygame.time.Clock()
    rodando = True

    while rodando:                                                                                                  
        clock.tick(FPS)                                                                                             # Roda o jogo na taxa de atualização definida
        janela.fill(purple)

        pygame.draw.rect(janela, white, input_rect)
        text_surface = fontePalavra.render(user_text, True, black)
        janela.blit(text_surface, (input_rect.x+5, input_rect.y+5))

        texto = fonteLetras.render('Insira uma palavra!', 1, black)
        janela.blit(texto, ((largura/2 - texto.get_width()/2), (altura/2.3 - texto.get_height()/2)))

        aviso = fonteAviso.render('Nota: Utilize apenas letras, espaços e caractéres especiais não são aceitos.', 1, white)
        janela.blit(aviso, ((largura/2 - aviso.get_width()/2), (altura/1.80 - aviso.get_height()/2)))
        aviso2 = fonteAviso.render('Pressione ENTER para continuar', 1, white)
        janela.blit(aviso2, ((largura/2 - aviso2.get_width()/2), (altura/1.70 - aviso2.get_height()/2)))
        pygame.display.update()

        for event in pygame.event.get():                                                                            # Verifica eventos (ações) no jogo
            if event.type == pygame.QUIT:                                                                           # Fecha o jogo
                pygame.quit()
            if event.type == pygame.KEYDOWN:                                                                        #Registra as teclas digitadas
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_text.isalpha():
                        jogoPVP()
                    else:
                        text_input()
                else:
                    user_text += event.unicode.upper()
                
# Setup do menu do jogo
def main_menu():
    janela.fill(purple)

    tentativas.clear()
    
    # Setup do looping do jogo
    FPS = 60
    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        clock.tick(FPS)
        
        botaoJogar = fonteMenu.render('Jogar', 1, black)
        janela.blit(botaoJogar, ((largura/2 - botaoJogar.get_width()/2), (altura/2 - botaoJogar.get_height()/2)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_x, menu_mouse_y = pygame.mouse.get_pos()
                if 760 > menu_mouse_x > 615 and 390 > menu_mouse_y > 360:
                    modo_jogo()

# Setup da seleção de modo                  
def modo_jogo():
    rodando = True
    janela.fill(purple)

    # Setup do looping do jogo
    FPS = 60
    clock = pygame.time.Clock()
    rodando = True
    clock.tick(FPS)

    while rodando:
        
        jogarPVP = fonteMenu.render('Jogador contra Jogador', 1, black)
        janela.blit(jogarPVP, ((largura/2 - jogarPVP.get_width()/2), (altura/2 - jogarPVP.get_height()/2)))

        jogarPVE = fonteMenu2.render('Jogador contra CPU', 1, black)
        janela.blit(jogarPVE, ((largura/2 - jogarPVE.get_width()/2), 468))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_mouse_x, menu_mouse_y = pygame.mouse.get_pos()
                if 850 > menu_mouse_x > 515 and 495 > menu_mouse_y > 470:
                    jogoCPU()
                if 965 > menu_mouse_x > 400 and 400 > menu_mouse_y > 355:
                    text_input()  

main_menu()
pygame.quit()                                                                                                   # Fecha o jogo ao sair do looping