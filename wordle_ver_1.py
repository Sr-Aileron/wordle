#ver1 単語の正誤のみ判定

import pygame
import random

pygame.init()

#画面の設定
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("wordle(5x5)")

#色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

#フォントの設定
font = pygame.font.Font(None, 48)

#単語読み込み
word_list = []
with open("_wordle/wordle.txt", "r") as file:
    for line in file:
        if len(line.strip()) == 5:
            word_list.append(line.strip().lower())

#正解の単語を決める
answer = random.choice(word_list)
print(f'デバッグ用正解:{answer}')

#ここで使いたい変数を定義
input_word = ""
result = []

#メインループ
run = True
while run:

    #背景塗りつぶし
    screen.fill(WHITE)

    #イベントの取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            
            #確定時の処理
            elif event.key == pygame.K_RETURN and len(input_word) == 5:
                result = []
                for i, char in enumerate(input_word):
                    if char == answer[i]:
                        result.append((char, "green"))
                    elif char in answer:
                        result.append((char, "yellow"))
                    else:
                        result.append((char, "gray"))

            #単語追加の処理
            elif event.unicode.isalpha() == True and len(input_word) < 5:
                input_word += event.unicode.lower()

            #単語削除の処理
            elif event.key == pygame.K_BACKSPACE:
                input_word = input_word[:-1]
    

    #単語の描画
    for i, char in enumerate(input_word):
        input_text_surface = font.render(char.upper(), True, BLACK)
        screen.blit(input_text_surface, (50 + i*50, 200))
    
    #結果の描画
    col = None
    for i, (char, color) in enumerate(result):
        if color == "green":
            col = GREEN
        elif color == "yellow":
            col = YELLOW
        else:
            col = GRAY
        result_text_surface = font.render(char.upper(), True, col)
        screen.blit(result_text_surface, (50 + i*50, 300))
    
    pygame.display.update()

pygame.quit()