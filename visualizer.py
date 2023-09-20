import pygame

fileName = "trace.txt"

pygame.init()

window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

font = pygame.font.SysFont('freesanbold.ttf', 50)
texts = []
textRects = []
for i in range(25):
    texts.append(font.render(chr(97 + i), True, (0, 255, 0)))
    textRects.append(texts[i].get_rect())
    textRects[i].center = (i % 5 * 100 + 50,i // 5 * 100 + 50)

string = "devilladaemonusspellbound"
#string = "axe----------------------"
workerString = "[0:0:a],[0:1:g],[0:2:e],[0:3:-],"

file = open("trace.txt")
lines = file.readlines()
string = lines[0]
lines.remove(string)
file.close()
lineRead = 0
#input()

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((255, 255, 255))


    
    for i in range(25):
        texts[i] = font.render(string[i], True, (0, 255, 0))
        #window.blit(texts[i], textRects[i])  

    workerString = lines[lineRead % len(lines)]
    lineRead += 1
    bits = workerString.split(",")[:-1]
    z = []
    for bit in bits:
        nx = int(bit[1])
        ny = int(bit[3])
        char = bit[5]
        custom = bool(int(bit[7]))
        isWord = bool(int(bit[9]))
        if custom:
            texts[nx * 5 + ny] = font.render(char, True, (255, 255, 0))
        else:
            texts[nx * 5 + ny] = font.render(char, True, (0, 255, 0))
        z.append(nx * 5 + ny)

        if isWord:
            pygame.draw.rect(window, (250, 0, 250), (ny * 100, nx * 100, 100, 100))
        else:
            pygame.draw.rect(window, (0, 0, 250), (ny * 100, nx * 100, 100, 100))
        window.blit(texts[nx * 5 + ny], textRects[nx * 5 + ny])
    else:
        nx = int(bit[1])
        ny = int(bit[3])
        char = bit[5]
        texts[nx * 5 + ny]
        z.append(nx * 5 + ny)
        pygame.draw.rect(window, (0, 250, 250), (ny * 100, nx * 100, 100, 100))
        window.blit(texts[nx * 5 + ny], textRects[nx * 5 + ny])

    for i in range(25):
        if not i in z:
            window.blit(texts[i], textRects[i])
    
    for x in range(5):
        for y in range(5):
            pygame.draw.rect(window, (0, 0, 0), (x * 100, y * 100, 100, 100), width = 1)          

    pygame.display.flip()

pygame.quit()
exit()
