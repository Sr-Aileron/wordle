#ver2

import pygame
import random

pygame.init()

#画面の設定
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("wordle(6x5)")

#色の設定
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
GREEN = (0, 180, 0)
YELLOW = (180, 180, 0)
GRAY = (128, 128, 128)
DARKGRAY = (50, 50, 50)

#フォントの設定
font = pygame.font.Font(None, 60)
font_keyboard = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 35)

#関数

def draw_grid():
    grid_type = None
    for i in range(6):
        for j in range(5):

            #テキストのバックの形式を決定
            if i < len(guesses):
                if guesses[i][1][j][1] == "gray":
                    grid_type = DARKGRAY
                elif guesses[i][1][j][1] == "yellow":
                    grid_type = YELLOW
                elif guesses[i][1][j][1] == "green":
                    grid_type = GREEN
                tex_rect = pygame.Rect(155 + j*60, 25 + i*60, 52, 52)
                screen.fill(grid_type, tex_rect)

            elif i == len(guesses) and j < len(current_input):
                pygame.draw.rect(screen, GRAY, (155 + j*60, 25 + i*60, 52, 52), 2)
            else:
                pygame.draw.rect(screen, DARKGRAY, (155 + j*60, 25 + i*60, 52, 52), 2)

def draw_keyboard():
    col = None
    for i in range(10):
        col = draw_keyboard_a(i)
        key_rect = pygame.Rect(105 + i*40, 420, 30, 40)
        screen.fill(col, key_rect)
        bg_screen = font_keyboard.render(keyboard[i][0], True, WHITE)
        screen.blit(bg_screen, (110 + i*40, 425))

    for i in range(9):
        col = draw_keyboard_a(i+10)
        key_rect = pygame.Rect(125 + i*40, 470, 30, 40)
        screen.fill(col, key_rect)
        bg_screen = font_keyboard.render(keyboard[i+10][0], True, WHITE)
        screen.blit(bg_screen, (130 + i*40, 475))

    for i in range(7):
        col = draw_keyboard_a(i+19)
        key_rect = pygame.Rect(165 + i*40, 520, 30, 40)
        screen.fill(col, key_rect)
        bg_screen = font_keyboard.render(keyboard[i+19][0], True, WHITE)
        screen.blit(bg_screen, (170 + i*40, 525))

def draw_keyboard_a(n):
    if keyboard[n][1] == "unused":
        return GRAY
    elif keyboard[n][1] == "yellow":
        return YELLOW
    elif keyboard[n][1] == "green":
        return GREEN
    else:
        return DARKGRAY

def draw_current_word():
    for i, char in enumerate(current_input):
        text_screen = font.render(char.upper(), True, WHITE)
        screen.blit(text_screen, (165 + i*60, 35 + 60*len(guesses)))

def draw_previous_word():
    for i, pre_guess in enumerate(guesses):
        for j, (char, color) in enumerate(pre_guess[1]):
            text_screen = font.render(char.upper(), True, WHITE)
            screen.blit(text_screen, (165 + j*60, 35 + i*60))

def draw_winlose():
    if game_state == "win":
        judge_screen = font_small.render("You Win!", True, WHITE)
        screen.blit(judge_screen, (250, 385))
    elif game_state == "lose":
        judge_screen = font_small.render("Game Over! answer: {}".format(answer), True, WHITE)
        screen.blit(judge_screen, (150, 385))

#単語読み込み
word_list = []
with open("_wordle/wordle.txt", "r") as file:
    for line in file:
        if len(line.strip()) == 5:
            word_list.append(line.strip().lower())

#正解の単語を決める
answer = random.choice(word_list)
#print(f'デバッグ用正解:{answer}')

#ここで使いたい変数を定義
current_input = ""
result = []
guesses = []
game_state = "playing"
keyboard = [[w, "unused"] for w in "qwertyuiopasdfghjklzxcvbnm"]

#メインループ
run = True
while run:

    #背景塗りつぶし
    screen.fill(BLACK)

    #イベントの取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            
            #return時の処理
            elif event.key == pygame.K_RETURN and len(current_input) == 5 and game_state == "playing":
                result = []
                for i, char in enumerate(current_input):
                    if char == answer[i]:
                        result.append((char, "green"))
                    elif char in answer:
                        result.append((char, "yellow"))
                    else:
                        result.append((char, "gray"))

                    #キーボードの色の変更
                    for j, key in enumerate(keyboard):
                        if char == key[0]:
                            if result[i][1] == "yellow" and keyboard[j][1] == "green":
                                continue
                            if result[i][1] == "gray" and keyboard[j][1] != "unused":
                                continue
                            keyboard[j][1] = result[i][1]


                guesses.append((current_input, result))


                #勝敗の判定
                if current_input == answer:
                    game_state = "win"
                elif len(guesses) >= 6:
                    game_state = "lose"

                current_input = ""

            #単語追加の処理
            elif event.unicode.isalpha() == True and len(current_input) < 5 and game_state == "playing":
                current_input += event.unicode.lower()

            #単語削除の処理
            elif event.key == pygame.K_BACKSPACE and game_state == "playing":
                current_input = current_input[:-1]

            #デバッグ用
            """
            elif event.key == pygame.K_SPACE:
                print(guesses, current_input, game_state,)
            """
    
    #グリッド描画（未使用）
    """
    pygame.draw.rect(screen, BLACK, (150, 20, 300, 360), 2)
    for i in range(1, 6):
        pygame.draw.line(screen, BLACK, (150, 20 + i*60), (450, 20 + i*60), 2)
    for i in range(1, 5):
        pygame.draw.line(screen, BLACK, (150 + i*60, 20), (150 + i*60, 380), 2)
    """
    
    #単語のバックの描画
    draw_grid()
    
    #キーボードの描画
    draw_keyboard()

    #単語の描画
    draw_current_word()
    
    #結果が確定した単語の描画
    draw_previous_word()
    
    #win-loseの描画
    draw_winlose()
    
    pygame.display.update()

pygame.quit()