import tkinter as tk
import uuid

from src.datastruct.test_data import TestQuestion
from src.ui.question import QuestionView


#3F6CB0
#5B87C4



class TestPlayer(tk.Toplevel):
    def __init__(self, parent, questions: tuple[TestQuestion]):
        super().__init__(parent,bg='#FFF')
        self.geometry("1280x720")
        self.title("ESAT Driver")
        # self.grab_set()

        self._q = questions
        self._q_frames: list[tk.Canvas] = []

        self._q_num_tv = tk.StringVar(self, value="Question 1")
        self._q_num = 1

        self._timer_tv = tk.StringVar(self, value="00:00")
        self._timer = 0

        self.bind("<Alt-n>", lambda _: self.__next_q_callback)
        self.bind("<Alt-p>", lambda _: self.__prev_q_callback)

        self.__grid_config()

        self.__create_title_bar()
        self.__create_nav_bar()

        self.__load_questions()

    def __grid_config(self):
        self.rowconfigure((0,2),weight=1,uniform='a')
        self.rowconfigure(1,weight=15,uniform='a')
        self.columnconfigure(0,weight=1,uniform='a')

    def __create_title_bar(self):
        colour="#3F6CD0"
        frame = tk.Frame(self,bg=colour,padx=2,pady=2)
        frame.columnconfigure(0,weight=5,uniform='a')
        frame.columnconfigure(1,weight=3,uniform='a')
        frame.columnconfigure(2,weight=1,uniform='a')
        tk.Label(frame,text="Engineering and Science Admissions Test",font=("Arial",24),bg=colour,fg='#FFF',anchor='w'
                 ).grid(row=0,column=0,sticky='wens')
        tk.Label(frame,textvariable=self._timer_tv,font=("Arial",16),bg=colour,fg='#FFF'
                 ).grid(row=0,column=1,sticky='wens')
        tk.Label(frame,textvariable=self._q_num_tv,font=("Arial",16),bg=colour,fg='#FFF'
                 ).grid(row=0,column=2)
        frame.grid(row=0,column=0,sticky='wens')

    def __create_nav_bar(self):
        frame = tk.Frame(self,relief='flat',bg="#3F6CD0",padx=5,pady=5)
        tk.Button(frame,text="Previous",command=self.__next_q_callback,font=("Arial",16)
                  ).pack(side='left', fill='both')
        tk.Button(frame,text="Next",command=self.__prev_q_callback,font=("Arial",16)
                  ).pack(side='right', fill='both')
        frame.grid(row=2,column=0,sticky='wens')

    def __load_questions(self):
        for item in self._q:
            q = QuestionView(self, item)
            q.grid(row=1,column=0,sticky='wens')
            self._q_frames.append(q)


    def __next_q_callback(self):
        ...
        self._q_frames[0].tkraise()

    def __prev_q_callback(self):
        ...






if __name__ == "__main__":
    c = tk.Tk()
    tp = TestPlayer(c, (TestQuestion(
        "Find the initial charge of capacitor $\\int_{0}^{\\infty}{I_0 e^{\\frac{-t}{RC}}}$ as function of Q.",
        ("$Q=I_0 CR$", "before $Q$ plaintext", "plaintext"),
        uuid.uuid4()
    ),))
    c.mainloop()



