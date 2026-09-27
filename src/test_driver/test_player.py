import tkinter as tk

from src.qa_manager.result_generator import generate_result
from src.datastruct.test_data import TestQuestion
from src.test_driver.question import QuestionView
from src.test_driver.stopwatch import Stopwatch


#3F6CB0
#5B87C4

class TestPlayer(tk.Toplevel):
    def __init__(self, parent, questions: tuple[TestQuestion, ...], name: str, finish_callback):
        super().__init__(parent,bg='#FFF')
        self.geometry("1280x720")
        self.title("ESAT Driver")
        # self.grab_set()

        self._name = name
        self._finish_callback = finish_callback

        self._length = len(questions)

        self._q = questions
        self._q_frames: list[QuestionView] = []

        self._q_num = 1
        self._q_num_tv = tk.StringVar(self, value=f"Question {self._q_num} of {self._length}")

        self._timer = Stopwatch()
        self._timer_tv = tk.StringVar(self, value="00:00")

        self.bind("<Alt-n>", lambda _: self.__next_q_callback)
        self.bind("<Alt-p>", lambda _: self.__prev_q_callback)

        self.__grid_config()

        self.__create_title_bar()
        self.__create_control_bar()
        self.__create_nav_bar()
        self.__create_pause_frame()
        self.__load_questions()

        self._pause_frame.tkraise()

        self.__refresh_timer()

    def __grid_config(self):
        self.rowconfigure((0,1,3),weight=1,uniform='a')
        self.rowconfigure(2,weight=15,uniform='a')
        self.columnconfigure(0,weight=1,uniform='a')

    def __create_pause_frame(self):
        self._pause_frame = tk.Frame(self,bg='#FFF')
        self._pause_frame.grid(row=2,column=0,sticky='wens')
        frame = tk.Frame(self._pause_frame,bg='#FFF')
        tk.Label(frame,text="The test is now paused",bg='#FFF',font=('Arial',24)
                 ).pack(fill='both')
        tk.Button(frame,text="Resume",font=("Arial",24),bg='#FFF',command=self.__pause_resume_callback
                 ).pack()
        frame.place(relx=0.5,rely=0.5,anchor='center')

    def __create_title_bar(self):
        colour="#3F6CB0"
        frame = tk.Frame(self,bg=colour,padx=2,pady=2)
        tk.Label(frame,text="Engineering and Science Admissions Test",font=("Arial",20),bg=colour,fg='#FFF',anchor='w'
                 ).pack(side="left",fill="both",padx=10)
        tk.Label(frame,textvariable=self._q_num_tv,font=("Arial",16),bg=colour,fg='#FFF'
                 ).pack(side="right",fill="both",padx=10)
        frame.grid(row=0,column=0,sticky='wens')

    def __create_control_bar(self):
        colour='#5B87C4'
        frame = tk.Frame(self,bg=colour,padx=2,pady=2)
        tk.Label(frame,textvariable=self._timer_tv,font=("Arial",16),bg=colour,fg='#FFF'
                 ).pack(side='left',fill="both",padx=10)
        tk.Label(frame,text=self._name,font=("Arial",16),bg=colour,fg='#FFF'
                 ).pack(side='left',fill="both",padx=10)
        frame.grid(row=1,column=0,sticky='wens')

    def __create_nav_bar(self):
        frame = tk.Frame(self,relief='flat',bg="#3F6CB0",padx=5,pady=5)
        tk.Button(frame,text="Previous",command=self.__prev_q_callback,font=("Arial",16)
                  ).pack(side='left', fill='both')
        tk.Button(frame,text="Next",command=self.__next_q_callback,font=("Arial",16)
                  ).pack(side='right', fill='both')
        tk.Button(frame,text='Finish',command=self.__finish_callback,font=("Arial",16)
                  ).pack(side='left',fill='both',padx=5)
        tk.Button(frame,text="Pause/Resume",command=self.__pause_resume_callback,font=("Arial",16)
                  ).pack(side="right",fill='both',padx=5)
        frame.grid(row=3,column=0,sticky='wens')

    def __load_questions(self):
        for item in self._q:
            q = QuestionView(self, item)
            q.grid(row=2,column=0,sticky='wens')
            self._q_frames.append(q)
        self._q_frames[0].tkraise()

    def __pause_resume_callback(self):
        if self._timer.running:
            # Pause
            self._timer.pause()
            self._q_frames[self._q_num-1].timer.pause()
            self._pause_frame.tkraise()
        else:
            # Resume
            self._timer.start()
            self._q_frames[self._q_num-1].timer.start()
            self._q_frames[self._q_num-1].tkraise()

    def __next_q_callback(self):
        if self._q_num == self._length or not self._timer.running: return
        self._q_frames[self._q_num-1].timer.pause()
        self._q_num += 1
        self._q_frames[self._q_num-1].tkraise()
        self._q_frames[self._q_num-1].timer.start()
        self._q_num_tv.set(f"Question {self._q_num} of {self._length}")

    def __prev_q_callback(self):
        if self._q_num == 1 or not self._timer.running: return
        self._q_frames[self._q_num-1].timer.pause()
        self._q_num -= 1
        self._q_frames[self._q_num-1].tkraise()
        self._q_frames[self._q_num-1].timer.start()
        self._q_num_tv.set(f"Question {self._q_num} of {self._length}")

    def __finish_callback(self):
        answers = []
        for i, frame in enumerate(self._q_frames):
            frame.timer.pause()
            answers.append({"qid": str(frame.question.id),
                    "selected": frame.choice,
                    "time": frame.timer.elapsed()})
        generate_result(answers)
        self.destroy()
        self._finish_callback(answers, self._q)

    def __refresh_timer(self, _=None):
        current = self._timer.elapsed()
        text = self._timer.format_seconds(current)
        self._timer_tv.set(text)
        self.after(50, self.__refresh_timer, None)








