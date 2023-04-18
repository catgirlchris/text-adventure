import time
import sys
import curses
import curses.textpad
import traceback
import random

game_name : str = 'text-adventure'
game_version : str = 'v0'

dlog_casa : str = ("Te despiertas. Estabas teniendo una pesadilla pero no recuerdas qué estaba ocurriendo. Parecía inquietante, como si algo te hubiese estado aterrando durante un periodo muy largo de tiempo.*insertar choose*\n\n"

"Intentas hacer memoria, pero está todo muy difuso. Sólo consigues recordar un incesante miedo y una figura inimagibable observandote, pero no visualmente. Es raro.\n\n"

"Abres los ojos. Te encuentras con un techo familiar. Blanco y un poco antiguo, con troncos de madera cruzando todo el techo. Te recuerda a tu antigua casa de campo donde pasabas el verano con tus abuelos, tíos y primos.\n\n"

"Mientras te reincorporas para girarte, un intenso olor a especias recorre tu cara. Todo es tan familiar que hasta te comienza a molestar no ubicarte. La pesadilla te ha dejado fuera de luegar.\n\n"

"Miras a tu derecha para encontrarte con una pared. Blanca, igual que el techo. Un cuadro con una figura angelical de vestimentas verdes y rojas, brillantes y suaves rellena la zona de la pared que da a la cama. El marco es de madera con un grabado precioso con figuras onduladas, asemejandose a hojas rodeando el cuadro.\n\n")

bigpad_sizeyx = [14, 52]

def print_slow_old(text:str, pause_time:float = 0.8):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(pause_time)

def print_slow(pad:curses.window):
    pass
    """i = 0
    letter_in_line_count = 0
    word_letter_count = 0
    cols = bigpad_sizeyx[0]
    for c in dlog_casa:
        if c == ' ':
            word_letter_count = 0
        else:
            word_letter_count += 1

        if letter_in_line_count >= cols:
            letter_in_line_count = 0
        else:
            letter_in_line_count += 1

        i += 1

        bigpad.addch(c, curses.color_pair(2))
        bigpad.refresh(0,0, 2,67, 14,116)
        time.sleep(0.06)
    """

def init_color_pairs():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

class Window():
    def __init__(self, nlines, ncols, begin_y, begin_x):
        self.win = curses.newwin(nlines, ncols, begin_y, begin_x)    

def draw_x(pad:curses.window, offset:int):
    j:int = 0
    for k in range(10):
        if k%2==0:
            for i in range(0,26,1):
                pad.chgat(i+j,i+j, i, curses.color_pair(1))
                pad.refresh(offset,0, 2,67, 26,116)
                time.sleep(0.1)
        else:
            for i in range(26,0,-1):
                pad.chgat(26-i+j,i+j, i, curses.color_pair(3))
                pad.refresh(offset,0, 2,67, 26,116)
                time.sleep(0.1)
        j = (j+3)%26

def rain(pad:curses.window, offset:int):
    size = [26, 67]

    gotas = []
    for g in range(0,26,1):
        gotas.append(0)

    prev_cursor_state = curses.curs_set(False)
    for k in range(100):
        for i in range(1,26,1):
            gotas[i] += random.randint(0,1)

            pad.chgat(gotas[i],i, 1, curses.color_pair(3))
            pad.noutrefresh(offset,0, 2,67, 26,116)
        curses.doupdate()
        time.sleep(0.05)

    curses.curs_set(prev_cursor_state)


def main(stdscr:curses.window):
    # init color pairs (color, fondo)
    init_color_pairs()

    # gui sizes and data
    header_info = {'begin_yx':[0,0],
                   'text':str('Bienvenide a mi juego '+game_name+' '+game_version),
                   'attr':curses.color_pair(1)}
    
    editwin_info = {'size':[5,30],
                    'begin_yx':[2,1]}
    editwin2_info = {'size':[7,30],
                     'begin_yx':[9,1]}

    # codigo principal
    # header
    stdscr.addstr(header_info['begin_yx'][0],header_info['begin_yx'][1],
                  header_info['text'], header_info['attr'])

    # left editwin
    editwin = curses.newwin(editwin_info['size'][0],editwin_info['size'][1],
                            editwin_info['begin_yx'][0],editwin_info['begin_yx'][1])
    editwin2 = curses.newwin(editwin2_info['size'][0],editwin2_info['size'][1],
                            editwin2_info['begin_yx'][0],editwin2_info['begin_yx'][1])
    displaypad = curses.newpad(14,60)
    bigpad = curses.newpad(200, 50)

    stdscr.addstr(27,0, 'Hay '+str(curses.LINES)+' líneas y '+str(curses.COLS)+' columnas')
    stdscr.addstr(28,0, 'Pulsa Ctrl-G para en enviar mensajes')
    
    curses.textpad.rectangle(stdscr, editwin_info['begin_yx'][0]-1,editwin_info['begin_yx'][1]-1,
                             1+editwin_info['size'][0]+1, 1+editwin_info['size'][1]+1)
    editbox = curses.textpad.Textbox(editwin)

    curses.textpad.rectangle(stdscr, editwin2_info['begin_yx'][0]-1,editwin_info['begin_yx'][1]-1,
                             1+14+1, 1+30+1)
    editbox2 = curses.textpad.Textbox(editwin2)

    curses.textpad.rectangle(stdscr, 1,33, 1+14+1, 1+63+1)
    curses.textpad.rectangle(stdscr, 1,66, 1+26+1,1+116+1)

    stdscr.refresh()

    # print slow
    offset = 0
    for c in dlog_casa:
        bigpad.addch(c, curses.color_pair(2))
        if bigpad.getyx()[0]-offset == 26:
            offset += 3
        bigpad.refresh(offset,0, 2,67, 26,116)
        time.sleep(0)
    
    #draw_x(bigpad, offset)
    rain(bigpad, offset)

    stdscr.refresh()
    offset = 0
    for i in range(10):
        editbox.edit()
        message = editbox.gather()
        editwin.clear()

        displaypad.addstr('chris', curses.color_pair(1))
        displaypad.addch(':', curses.color_pair(0))
        displaypad.addstr(message, curses.color_pair(2))
        
        displaypad.refresh(0,0, 2,34+offset, 14,63+offset)
        

    editbox2.edit()
    message = editbox2.gather()
    stdscr.addstr(19,0, message)
    stdscr.refresh()

    # pause
    stdscr.getch()
    
    #print_slow(dlog_casa, 0.05)

    
if __name__ == '__main__':
    curses.wrapper(main)


"""if __name__ == '__main__':
    try:        
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        if curses.has_colors():
            curses.start_color()
        stdscr.keypad(True)
        
        main(stdscr)

        stdscr.keypad(False)
        curses.echo() ; curses.nocbreak()
        curses.endwin()

    except:
        stdscr.keypad(False)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
        traceback.print_exc()"""