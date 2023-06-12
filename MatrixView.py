import curses
import curses.textpad

import time
from typing import List, Tuple

import draw

class View:
    '''Vista para mostrar el contenido de un "curses._CursesWindow".
    Por ahora usa coordenadas absolutas ya que los pads no tiene posicion en el mapa.'''

    def __init__(self, pminrow: int, pmincol: int, sminrow: int, smincol: int, smaxrow: int, smaxcol: int, matrixview:'MatrixView', screen:'curses._CursesWindow'):
        self.pminrow = pminrow
        self.pmincol = pmincol
        self.sminrow = sminrow
        self.smincol = smincol
        self.smaxrow = smaxrow
        self.smaxcol = smaxcol

        self.matrixview = matrixview
        self.screen = screen


    def update(self):
        pass

    def boxouter(self):
        '''Dibuja un rectangulo alrededor de la vista. Por ahora lo dibuja en screen, la pantalla principal.'''
        draw.rectangle(self.screen, self.sminrow, self.smincol, self.smaxrow+1, self.smaxcol+1)
        self.screen.refresh()
    
    def getsize(self) -> Tuple[int,int]:
        '''Devuelve el tamaño de la ventana vista a dibujar.'''
        return self.smaxrow - self.sminrow, self.smaxcol - self.smincol
    
    def getposyx(self) -> Tuple[int, int]:
        '''Devuelve la posicion (en Screen por ahora) de la vista.'''
        return self.pminrow, self.pmincol



class Widget:
    '''Clase "abstracta" que generaliza los elementos que formarán un menú como MatrixView.'''
    def __init__(self, win: 'MatrixView', posyx, listening: bool=1):
        self.win = win
        self.posyx = posyx
        
    def setdata(self, data):
        self.data = data

    def draw(self):
        pass

    def input(self):
        pass



class Button(Widget):
    '''Clase que representa un botón como el de cerrar ventana o mostar info.'''
    def __init__(self, win: 'MatrixView', posyx: Tuple[int,int], symbol: str='x', listening: bool=1, onborder: bool=0):
        Widget.__init__(self, win, posyx, listening)
        self.symbol = symbol
        self.onborder = onborder

    def input(self, key: int, mouse_info: Tuple[int, int, int, int, int]):
        mx, my = mouse_info[1], mouse_info[2]
        self.win.screen.addstr(self.win.screen.getmaxyx()[0]-2, 0, str(mouse_info))
        if my == self.posyx[0] and mx == self.posyx[1]:
            # TODO cambiar despues
            self.win.showinfo()


    def ispressed(self, mouse_pos: Tuple[int, int]):
        if self.posyx == mouse_pos:
            pass

    def draw(self):
        '''Dibuja el botón. Si está en el borde exterior, 
        entonces lo dibuja en screen, fuera de la ventana a la que petenece.'''
        if self.onborder:
            self.win.screen.addstr(self.posyx[0]+self.win.view.pminrow, self.posyx[1]+self.win.view.pmincol, self.symbol)
        else:
            self.win.addstr(self.posyx[0], self.posyx[1], self.symbol)


class WidgetManager:
    def __init__(self, win:'MatrixView'):
        self.win = win
        self.widgets: List[Widget] = list()

    def addwidget(self, w: Widget):
        self.widgets.append(w)

    def drawwidget(self, w: Widget):
        w.draw()

    def drawwidgets(self):
        for w in self.widgets:
            self.drawwidget(w)

    def refresh(self):
        self.win.refresh()

    def input(self, key: int, mouse_info: Tuple[int, int, int, int, int]):
        for w in self.widgets:
            w.input(key, mouse_info)



class Panel():
    """Clase que encapsula una ventana de curses. Generaliza los distintos tipos de ventanas como MatrixView."""
    pass



class MatrixView(Panel):
    """Clase hereda de Pane"""

    def __init__(self, nlines, ncols, screen:'curses._CursesWindow', border=1, defaultbuttons: Tuple[bool, bool, bool] = [1,1,1]):
        self.pad = curses.newpad(nlines, ncols)
        self.border = border
        self.screen = screen
        self.wm = WidgetManager(self)
        self.view = View(0,0, 0,0, 15,30, self, screen)
        self.view.boxouter()

        self._adddefaultbuttons(defaultbuttons)
        
    def getsize(self):
        '''Devuelve el tamaño del pad y de la vista.'''
        return [self.pad.getmaxyx(), self.view.getsize()]
    
    def _adddefaultbuttons(self, defaultbuttons: Tuple[bool, bool, bool]):
        y,x = 0, self.view.getsize()[1]
        if defaultbuttons[0]:
            exit = Button(self, [y,x], 'X', onborder=1)
            self.wm.addwidget(exit)
        if defaultbuttons[1]:
            minimize = Button(self, [y,x-1], '▭', onborder=1)
            self.wm.addwidget(minimize)
        if defaultbuttons[2]:
            help = Button(self, [y,x-2], '!', onborder=1)
            self.wm.addwidget(help)

    
    def showinfo(self):
        '''Muestra informacion sobre el pad y la vista.'''
        info = f"Vista:{self.getsize()[0]}, Pad:{self.getsize()[1]}"
        self.screen.addstr(self.view.smaxrow+1,0, info)
        self.screen.refresh()

    def addstr(self, y, x, string, attr=0):
        '''Añade string al pad. Por ahora es lo mismo que usar pad.addstr()'''
        self.pad.addstr(y, x, string, attr)

    def processinput(self):
        pass

    def update(self):
        pass

    def refresh(self):
        '''Dibuja la View del pad.'''
        self.pad.refresh(self.view.pminrow,self.view.pmincol, 
                         self.view.sminrow+self.border,self.view.smincol+self.border, 
                         self.view.smaxrow+self.border*2,self.view.smaxcol+self.border*2)
        self.wm.drawwidgets()



def main(screen:'curses._CursesWindow'):
    curses.curs_set(0)
    curses.mousemask(-1)

    win = MatrixView(15,30, screen)
    win.addstr(0, 0, 'Test string added.')
    win.addstr(1,0, 'Hay '+str(curses.LINES)+' líneas y '+str(curses.COLS)+' columnas')
    win.refresh()
    screen.refresh()

    end = True

    while(end):
        event: str = screen.getch()

        if ((event == curses.KEY_ENTER) | (event == ord('q'))):
            # Si Q es pulsada termina de pedir input
            end = False
        if event == curses.KEY_MOUSE:
            _, mx, my, _, bstate = curses.getmouse()
            minfo = _, mx, my, _, bstate
            if (bstate == curses.BUTTON1_CLICKED):
                screen.addstr(screen.getmaxyx()[0]-1, 0, f"{mx:03},{my:03}")

                win.wm.input(event, minfo)

        win.refresh()
        screen.refresh()
        time.sleep(0.0167)
        


curses.wrapper(main)