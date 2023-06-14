import curses
import curses.textpad

import time
from typing import List, Tuple

import draw

class View:
    '''Vista para mostrar el contenido de un "curses._CursesWindow".
    Por ahora usa coordenadas absolutas ya que los pads no tiene posicion en el mapa.'''

    def __init__(self, y: int, x: int, size: Tuple[int,int], matrixview:'MatrixView', screen:'curses._CursesWindow', offset: Tuple[int,int] = [0, 0]):
        self.y = y
        self.x = x
        self.size = size
        self.offset = offset

        self.matrixview = matrixview
        self.screen = screen

    @property
    def pminrow(self):
        return self.offset[0]

    @property
    def pmincol(self):
        return self.offset[1]
    
    @property
    def sminrow(self):
        return self.y
    
    @property
    def smincol(self):
        return self.x
    
    @property
    def smaxrow(self):
        return self.y + self.size[0]
    
    @property
    def smaxcol(self):
        return self.x + self.size[1]

    def update(self):
        pass

    def boxouter(self):
        '''Dibuja un rectangulo alrededor de la vista. Por ahora lo dibuja en screen, la pantalla principal.'''
        draw.rectangle(self.screen, self.sminrow, self.smincol, self.smaxrow+1, self.smaxcol+1)
        self.screen.refresh()
    
    def getsize(self) -> Tuple[int,int]:
        '''Devuelve el tamaño de la ventana vista a dibujar.'''
        return self.size
    
    def getposyx(self) -> Tuple[int, int]:
        '''Devuelve la posicion (en Screen por ahora) de la vista.'''
        return self.pminrow, self.pmincol



class Widget:
    '''Clase "abstracta" que generaliza los elementos que formarán un menú como MatrixView.'''
    def __init__(self, win: 'MatrixView', id: str, posyx: Tuple[int,int], listening: bool=1):
        self.id = id
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
    def __init__(self, win: 'MatrixView', id: str, posyx: Tuple[int,int], command, symbol: str='x', listening: bool=1, onborder: bool=0):
        Widget.__init__(self, win, id, posyx, listening)
        self.command = command
        self.symbol = symbol
        self.onborder = onborder
        self.pressed = False

    '''Maneja el input'''
    def input(self, key: int, mouse_info: Tuple[int, int, int, int, int]):
        mx, my = mouse_info[1], mouse_info[2]
        self.win.screen.addstr(self.win.screen.getmaxyx()[0]-2, 0, str(mouse_info))
        if my == self.posyx[0] and mx == self.posyx[1]:
            # TODO cambiar despues
            self.win.showinfo()

    def ispressed(self) -> bool:
        return self.pressed
    
    def press(self):
        self.pressed = True

    def release(self):
        self.pressed = False

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

    def __init__(self, nlines, ncols, viewinfo: Tuple[int, int, int, int], screen:'curses._CursesWindow', border=1, defaultbuttons: Tuple[bool, bool, bool] = [1,1,1]):
        self.pad = curses.newpad(nlines, ncols)
        self.border = border
        self.screen = screen
        self.wm = WidgetManager(self)
        self.view = View(viewinfo[0],viewinfo[1], [viewinfo[2],viewinfo[3]], self, screen)
        self.view.boxouter()

        self._adddefaultbuttons(defaultbuttons)
        
    def getsize(self):
        '''Devuelve el tamaño del pad y de la vista.'''
        return [self.pad.getmaxyx(), self.view.getsize()]
    
    def _adddefaultbuttons(self, defaultbuttons: Tuple[bool, bool, bool]):
        y,x = self.view.y, self.view.x+self.view.size[1]
        if defaultbuttons[0]:
            exit = Button(self, 'exit', [y,x], lambda self: self.showinfo(), 'X', onborder=1)
            self.wm.addwidget(exit)
        if defaultbuttons[1]:
            minimize = Button(self, 'minimize', [y,x-1], None, '▭', onborder=1)
            self.wm.addwidget(minimize)
        if defaultbuttons[2]:
            help = Button(self, 'help', [y,x-2], None, '!', onborder=1)
            self.wm.addwidget(help)

    
    def showinfo(self):
        '''Muestra informacion sobre el pad y la vista.'''
        info = f"Vista:{self.getsize()[0]}, Pad:{self.getsize()[1]}"
        self.screen.addstr(self.view.smaxrow+1,self.view.smincol+2, info)
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

def exitcallback():
    pass

def main(screen:'curses._CursesWindow'):
    curses.curs_set(0)
    curses.mousemask(-1)

    win = MatrixView(15,30, [0,0, 15, 40], screen)
    win.addstr(0, 0, 'Ventanica 1')
    win.addstr(1,0, 'Hay '+str(curses.LINES)+' líneas y '+str(curses.COLS)+' columnas')
    win.refresh()

    win2 = MatrixView(15,30, [0,42, screen.getmaxyx()[0]-0-3, screen.getmaxyx()[1]-42-3], screen)
    win2.refresh()
    win3 = MatrixView(15,30, [17,0, screen.getmaxyx()[0]-17-2-2, 40], screen)
    win3.refresh()
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
                win2.wm.input(event, minfo)
                win3.wm.input(event, minfo)

        win.refresh()
        win2.refresh()
        screen.refresh()
        time.sleep(0.0167)
        


curses.wrapper(main)