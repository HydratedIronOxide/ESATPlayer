import re
import tkinter as tk
import matplotlib.pyplot as plt

from PIL import Image, ImageTk
from io import BytesIO


from src.datastruct.test_data import TestQuestion
from test_driver.stopwatch import Stopwatch

plt.rcParams["mathtext.fontset"] = 'cm'
TOKEN_RE = re.compile(r"\$\$(.*?)\$\$ | \$(.*?)\$", re.DOTALL)


def tex_to_image(tex: str, font_size: int = 16) -> ImageTk.PhotoImage:
    print(tex)
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
                dpi=75)
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
        if m.group(1) is not None:
            eqn = tex_to_image(f"${m.group(1).strip()}$", font_size)
            imgs.append(eqn)
            textbox.image_create(tk.END, image=eqn)

        # Inline maths in $ ... $
        else:
            eqn = tex_to_image(f"${m.group(2).strip()}$")
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

        scrollbar = tk.Scrollbar(self._canvas, orient='vertical', command=self._canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self._canvas.create_window((0,0),window=frame,anchor='nw')
        self._canvas.configure(yscrollcommand=scrollbar.set)

        self.question = question

        frame.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox('all')))

        self._question_frame = _Question(self._canvas, question.question)
        self._choices_frame = _Choices(self._canvas, question.choices)

        self._question_frame.pack(padx=10, pady=10, fill='both')
        self._choices_frame.pack(fill='both', padx=10, pady=10)

        self.timer = Stopwatch()

    @property
    def choice(self): return self._choices_frame.choice

    @property
    def correct(self): return self.question.correct



class _Question(tk.Frame):
    def __init__(self, parent: tk.Canvas, q: str):
        super().__init__(parent,bg='#FFF')
        self._q = q
        self._text = tk.Text(self, wrap='word',font=("Arial",16),relief='flat',height=5)
        self._text.pack(fill="both", expand=True)
        self._imgs: list[ImageTk.PhotoImage] = []

        dat = write_text(self._q, self._text, 16)
        self._text.configure(state="disabled")

        self._imgs += dat


class _Choices(tk.Frame):
    def __init__(self, parent, c: tuple[str]):
        print(c)
        super().__init__(parent,bg='#FFF')
        self._var = tk.StringVar(self, "-")
        self._imgs = [tex_to_image(s) for s in c]

        self.grid_rowconfigure(list(range(len(c))), weight=1, uniform='a')
        self.grid_columnconfigure(0, weight=1, uniform='a')

        for (i, img) in enumerate(self._imgs):
            value = chr(65+i)
            tk.Radiobutton(self,image=img,text="",variable=self._var,value=value,bg='#FFF'
                           ).grid(row=i,column=0,sticky='w',ipady=2)

    @property
    def choice(self): return self._var.get()




