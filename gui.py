from tkinter import *
from typing import Callable, Final, Literal, Union
from controller import Controller


class Gui:
    # Consts
    FONT_SIZE_DEFAULT: Final[int] = 13
    FONT_SIZE_TITLE: Final[int] = 18

    WIDTH: Final[int] = 1280
    HEIGHT: Final[int] = 720

    # Private attrs
    __root: Tk
    __controller: Controller
    __obj_varlist: Variable  # holds a list

    # Constructor
    def __init__(self, controller: Controller) -> None:
        self.__controller = controller
        self.__root = Tk()
        self.__root.title("Sistema Básico de CG 2D")
        self.__root.resizable(width=False, height=False)
        self.__obj_varlist = Variable(value=['a', 'b'])

    # Private methods
    def __create_label(self, parent_frame: Frame, text: str, pady: int = 0, padx: int = 0,
                       font_size: int = FONT_SIZE_DEFAULT, align=TOP, anchor=None) -> Label:
        label = Label(parent_frame, text=text, font=('Helvetica', font_size))
        label.pack(pady=pady, padx=padx, side=align, anchor=anchor)
        return label

    def __create_input(self, parent_frame: Frame, placeholder: str = "", pady: int = 0,
                       padx: int = 0, width: int = 50, align=TOP, anchor=None) -> Entry:
        input = Entry(parent_frame, textvariable=StringVar(value=placeholder), width=width)
        input.pack(ipady=3, pady=pady, padx=padx, side=align, anchor=anchor)
        return input

    def __create_button(self, parent_frame: Frame, text: str, handler: Callable, *args,
                        pady: int = 0, padx: int = 0, align=TOP, anchor=None) -> Button:
        btn = Button(parent_frame, text=text, command=lambda: handler(*args))
        btn.pack(pady=pady, padx=padx, side=align, anchor=anchor)
        return btn

    # GUI components
    def __create_main_frame(self) -> Frame:
        main_frame = Frame(self.__root, width=self.WIDTH, height=self.HEIGHT)
        main_frame.pack(fill=BOTH, expand=True)
        main_frame.pack_propagate(0)
        return main_frame

    def __create_obj_list_frame(self, main_frame: Frame) -> Frame:
        obj_list_frame = LabelFrame(main_frame, text="Display File", font=('Helvetica', self.FONT_SIZE_DEFAULT),
            width=self.WIDTH/4, height=self.HEIGHT*4/6, borderwidth=2, relief=GROOVE)
        obj_list_frame.pack(padx=10, pady=10, side=TOP, anchor=W, fill=Y, expand=True)
        obj_list_frame.pack_propagate(0)

        list_box = Listbox(obj_list_frame, listvariable=self.__obj_varlist, selectmode=SINGLE, bg="#fff")
        list_box.pack(pady=1, padx=4, side=TOP, anchor=W, fill=BOTH, expand=True)
        
        self.__create_button(obj_list_frame, "Remover Objeto", self.__handle_remove_obj, list_box, padx=4, pady=2, align=LEFT)
        self.__create_button(obj_list_frame, "Adicionar Objeto", self.__handle_add_obj, padx=4, pady=2, align=RIGHT)
        
        return obj_list_frame

    def __create_navigation_frame(self, main_frame: Frame) -> Frame:
        navigation_frame = LabelFrame(main_frame, text="Navegação", font=('Helvetica', self.FONT_SIZE_DEFAULT), 
            width=self.WIDTH/4, height=self.HEIGHT*2/6, borderwidth=2, relief=GROOVE)
        navigation_frame.pack(padx=10, pady=10, side=TOP, anchor=W)
        navigation_frame.grid_propagate(0)

        for i in range(3):
            navigation_frame.rowconfigure(i, weight=1, uniform='r')
            navigation_frame.columnconfigure(i, weight=1, uniform='c')
        
        Button(navigation_frame, text="Zoom Out", command=lambda: self.__handle_zoom('out')).grid(row=0, column=0)
        Button(navigation_frame, text="Zoom In", command=lambda: self.__handle_zoom('in')).grid(row=0, column=2)
        
        Button(navigation_frame, text="↑", command=lambda: self.__handle_nav('up')).grid(row=0, column=1)
        Button(navigation_frame, text="←", command=lambda: self.__handle_nav('left')).grid(row=1, column=0)
        Button(navigation_frame, text="→", command=lambda: self.__handle_nav('right')).grid(row=1, column=2)
        Button(navigation_frame, text="↓", command=lambda: self.__handle_nav('down')).grid(row=2, column=1)
        
        return navigation_frame

    def __create_gui(self) -> None:
        main_frame = self.__create_main_frame()
        self.__create_obj_list_frame(main_frame)
        self.__create_navigation_frame(main_frame)

    # Handlers
    def __handle_remove_obj(self, list_box: Listbox) -> None:
        if list_box.curselection() == (): return
        selected_idx, = list_box.curselection()
        obj_list = list(self.__obj_varlist.get())
        obj_list.pop(selected_idx)
        self.__obj_varlist.set(obj_list)
        # TODO: Call controller remove

    def __handle_add_obj(self) -> None:
        # TODO: Call controller add
        pass
        
    def __handle_nav(self, direction: Literal['up', 'down', 'left', 'right']) -> None:
        # TODO: Call controller nav handler
        pass

    def __handle_zoom(self, direction: Literal['in', 'out']) -> None:
        # TODO: Call controller zoom handler
        pass

    # Public methods
    def run(self) -> None:
        self.__create_gui()
        self.__root.mainloop()
