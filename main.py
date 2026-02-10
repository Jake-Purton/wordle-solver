import pygame
import threading
from UIpygame import PyUI as pyui

from solver import WordleSolver

pygame.init()
screenw = 1200
screenh = 800
screen = pygame.display.set_mode((screenw, screenh), pygame.RESIZABLE)
ui = pyui.UI()
done = False
clock = pygame.time.Clock()
ui.styleload_brown()

def get_box_id(letter, word):
    return f"wordle_input_{letter}_{word}"

def letter_pressed(box_id):
    ui.IDs[box_id].wordle_state = (ui.IDs[box_id].wordle_state+1)%3

    update_box_col(box_id)
    refresh_words()

def update_box_col(box_id):
    box = ui.IDs[box_id]
    if box.wordle_state == 0:
        new_col = (120,124,126)
    elif box.wordle_state == 1:
        new_col = (160, 180, 20)
    elif box.wordle_state == 2:
        new_col = (106, 170, 100)
    else:
        box.wordle_state = 0
        update_box_col(box_id)
        return
    box.col = new_col
    box.hovercol = pyui.shiftcolor(new_col,20)
    box.refresh()

def make_wordle_grid(box_size=80, word_len=5, guesses=6):
    for row in range(guesses):
        for letter in range(word_len):
            box_id = get_box_id(letter, row)
            func = pyui.funcer(letter_pressed, box_id=box_id)
            new_button = ui.makebutton(30+letter*box_size,30+row*box_size,"",
                          textsize=box_size-10, width=box_size-10, height=box_size-10, textcol=(20,20,20), textoffsety=5,
                          hovercol=0, clickdownsize=1, command=func.func, ID=box_id, borderdraw=False,font="impact")
            new_button.wordle_state = 0
            update_box_col(box_id)
            # ui.maketextbox(30+letter*box_size,30+row*box_size,"", textsize=box_size-10, attachscroller=False, spacing=5,
            #                width=box_size-10, height=box_size-10, textcenter=True,
            #                lines=2, chrlimit=2, command=func.func, commandifkey=True, ID=box_id)

def get_prev_words():
    words = current_word
    letters = word_length

    prev_words = []

    for w in range(words):
        prev_words.append([])
        for l in range(letters):
            box_id = get_box_id(l, w)
            if box_id not in ui.IDs:
                break
            letter_box = ui.IDs[box_id]
            prev_words[-1].append({
                "letter": letter_box.text.lower(),
                "type": letter_box.wordle_state
            })

    return prev_words

def refresh_words():
    global solver_threads
    if "valid_words_title" not in ui.IDs:
        ui.maketext(460, 20, f"Best Words List", 40, ID="valid_words_title")
        ui.maketext(460, 60, "Loading...", maxwidth=600, ID="valid_words")
    ui.IDs["valid_words"].settext("Loading...")
    for thread_id in solver_threads:
        solver_threads[thread_id] = False
    new_thread = threading.Thread(target=run_solver)
    new_thread.start()
    solver_threads[new_thread.ident] = True

def run_solver():
    words = solver.get_best_words(get_prev_words())
    num_words = len(words)

    if solver_threads[threading.get_ident()]:
        st = ", ".join(list(map(lambda x: x.upper(), words[:30])))

        ui.IDs["valid_words_title"].settext(f"Best Words out of {num_words} possible:")
        ui.IDs["valid_words"].settext(st)

solver_threads = {}
current_word = 0
current_letter = 0
word_length = 5
solver = WordleSolver(word_length)

make_wordle_grid()
refresh_words()

while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            box = ui.IDs[get_box_id(current_letter, current_word)]
            if 97 <= event.key < 97+26:
                current_letter += 1
                if current_letter >= word_length:
                    current_letter = word_length-1
                box.settext(chr(event.key).upper())
            elif event.key == pygame.K_BACKSPACE:
                if box.text == "":
                    current_letter -= 1
                    if current_letter < 0:
                        current_word -= 1
                        if current_word < 0:
                            current_word = 0
                            current_letter = 0
                        else:
                            current_letter = word_length-1
                    else:
                        ui.IDs[get_box_id(current_letter, current_word)].settext("")
                else:
                    box.settext("")
            elif event.key == pygame.K_RETURN:
                if box.text != "":
                    current_word += 1
                    current_letter = 0
                    refresh_words()

    screen.fill(pyui.Style.wallpapercol)

    selected = ui.IDs[get_box_id(current_letter, current_word)]
    border = 2
    pygame.draw.rect(screen, (100,180,40), pygame.Rect(selected.x-border, selected.y-border, selected.width+border*2, selected.height+border*2))

    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
