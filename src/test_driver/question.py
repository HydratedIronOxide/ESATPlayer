import re
import tkinter as tk
import matplotlib.pyplot as plt

from PIL import Image, ImageTk
from io import BytesIO

from src.datastruct.test_data import TestQuestion
from src.test_driver.stopwatch import Stopwatch

plt.rcParams["mathtext.fontset"] = 'cm'
TOKEN_RE = re.compile(
    r"\$\$(?P<display>.*?)\$\$|(?<!\$)\$(?P<inline>.*?)\$(?!\$)",
    re.DOTALL,
)

def tex_to_image(tex: str, font_size: int = 16) -> ImageTk.PhotoImage:
    buf = BytesIO()
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0)
    txt = fig.text(0,0,tex,fontsize=font_size)
    fig.canvas.draw()
    bbox = txt.get_window_extent()
    w, h = bbox.width/fig.dpi, bbox.height/fig.dpi
    fig.set_size_inches(w,h)
    plt.savefig(buf,format="png",transparent=True,
                bbox_inches="tight",
                pad_inches=0.02,
                dpi=105)
    plt.close(fig)
    buf.seek(0)
    return ImageTk.PhotoImage(Image.open(buf))


def write_text(text: str, textbox: tk.Text, font_size: int = 16) -> list[ImageTk.PhotoImage]:
    idx = 0
    imgs = []
    for m in TOKEN_RE.finditer(text):
        start, end = m.span()

        # Plain text before maths block
        if start > idx:
            textbox.insert(tk.END, text[idx:start])

        # Maths in $$ ... $$
        if m.group("display") is not None:
            textbox.insert(tk.END, '\n')
            eqn = tex_to_image(f"${m.group('display').strip()}$", font_size)
            imgs.append(eqn)
            textbox.image_create(tk.END, image=eqn)
            textbox.insert(tk.END, '\n')

        # Inline maths in $ ... $
        else:
            eqn = tex_to_image(f"${m.group('inline').strip()}$", font_size)
            imgs.append(eqn)
            textbox.image_create(tk.END, image=eqn)

        idx = end

    # Add trailing text
    if idx < len(text):
        textbox.insert(tk.END, text[idx:])

    return imgs



class QuestionView(tk.Frame):
    def __init__(self, parent, question: TestQuestion):
        super().__init__(parent,bg='#FFF')
        self._canvas = tk.Canvas(self, bg='#FFF')
        self._canvas.pack(fill='both', expand=True)
        frame = tk.Frame(self._canvas,bg='#FFF')

        frame.grid_rowconfigure((0,1), weight=1, uniform='z')
        frame.grid_columnconfigure(0, weight=1, uniform='z')


        scrollbar = tk.Scrollbar(self._canvas, orient='vertical', command=self._canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self._canvas.create_window((0,0),window=frame,anchor='nw')
        self._canvas.configure(yscrollcommand=scrollbar.set)

        self.question = question

        frame.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox('all')))

        self._question_frame = _Question(frame, question.question)
        self._choices_frame = _Choices(frame, question.choices)

        self._question_frame.grid(row=0,column=0,pady=10,sticky="news")
        self._choices_frame.grid(row=1,column=0,pady=10,sticky="news")

        self.timer = Stopwatch()

    @property
    def choice(self): return self._choices_frame.choice



class _Question(tk.Frame):
    def __init__(self, parent: tk.Frame, q: str):
        super().__init__(parent,bg='#FFF')
        self._q = q
        self._text = tk.Text(self, wrap='word',font=("Arial",16),relief='flat',height=5)
        self._text.pack(fill="both", expand=True)
        self._imgs: list[ImageTk.PhotoImage] = []

        try:
            dat = write_text(self._q, self._text, 16)
            self._imgs += dat
        except Exception as e:
            print(f"Something went wrong: {e}")
        self._text.configure(state="disabled")



class _Choices(tk.Frame):
    def __init__(self, parent, c: tuple[str]):
        super().__init__(parent,bg='#FFF')
        self._var = tk.StringVar(self, "-")
        self._imgs = []
        for s in c:
            try:
                self._imgs.append(tex_to_image(s))
            except Exception as e: print(f"Something went wrong: {e}")

        self.grid_rowconfigure(list(range(len(c))), weight=1, uniform='a')
        self.grid_columnconfigure(0, weight=1, uniform='a')

        for (i, img) in enumerate(self._imgs):
            value = chr(65+i)
            tk.Radiobutton(self,image=img,text="",variable=self._var,value=value,bg='#FFF'
                           ).grid(row=i,column=0,sticky='w',ipady=2)

    @property
    def choice(self): return self._var.get()



