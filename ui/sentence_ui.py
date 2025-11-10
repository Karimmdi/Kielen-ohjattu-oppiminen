from tkinter import *
from tkinter import ttk
from typing import Callable
from config.settings import config
import os
import csv

SENTENCE_HISTORY_FILE = os.path.join("languages", "sentence_history.csv")

class SentencesUI:
  def __init__(self, master: Frame, on_back: Callable):
    self.on_back = on_back
    self.root = master.winfo_toplevel()
    self.frame = Frame(master, bg=config.BACKGROUND_COLOR)
    self.tree = None
    self._build()

  def _build(self):
    # Styles (match WordsUI)
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.Treeview",
                    background=config.BACKGROUND_COLOR,
                    fieldbackground=config.BACKGROUND_COLOR,
                    foreground="black",
                    rowheight=45,
                    font=("Arial", 13, "bold"),
                    padding=(5, 5, 5, 5))
    style.configure("Custom.Treeview.Heading",
                    font=("Arial", 16, "bold"),
                    background="#E8E8E8",
                    relief="flat")
    style.map("Custom.Treeview.Heading",
              background=[('active', '#D0D0D0')])
    style.configure("Custom.Vertical.TScrollbar",
                    gripcount=0,
                    background="#E8E8E8",
                    troughcolor=config.BACKGROUND_COLOR,
                    bordercolor=config.BACKGROUND_COLOR,
                    arrowcolor="black")

    header_frame = Frame(self.frame, bg=config.BACKGROUND_COLOR)
    header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
    Label(header_frame, text="Learned Sentences", font=("Arial", 40, "italic"), bg=config.BACKGROUND_COLOR).pack()
    Label(header_frame, text="Finnish — English", font=("Arial", 20, "bold"), bg=config.BACKGROUND_COLOR).pack()

    table_frame = Frame(self.frame, bg=config.BACKGROUND_COLOR)
    table_frame.grid(row=1, column=0, sticky="nsew", pady=12)

    self.frame.grid_rowconfigure(0, weight=0)
    self.frame.grid_rowconfigure(1, weight=1)
    self.frame.grid_columnconfigure(0, weight=1)

    columns = ("finnish", "english")
    self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Custom.Treeview")
    self.tree.heading("finnish", text="Finnish", anchor=CENTER)
    self.tree.heading("english", text="English", anchor=CENTER)
    self.tree.column("finnish", width=380, anchor=CENTER)
    self.tree.column("english", width=380, anchor=CENTER)

    self.tree.tag_configure('oddrow', background='white', font=("Arial", 13, "bold"))

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview, style="Custom.Vertical.TScrollbar")
    self.tree.configure(yscrollcommand=vsb.set)

    self.tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

  def refresh(self):
    # Reload from sentence_history.csv
    for row in self.tree.get_children():
      self.tree.delete(row)

    rows = []
    if os.path.exists(SENTENCE_HISTORY_FILE):
      with open(SENTENCE_HISTORY_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
          fi = r.get("Finnish") or r.get("finnish") or ""
          en = r.get("English") or r.get("english") or ""
          if fi or en:
            rows.append((fi, en))

    for i, (fi, en) in enumerate(rows):
      tag = 'oddrow' if i % 2 == 1 else ''
      self.tree.insert("", "end", values=(fi, en), tags=(tag,))

  def show(self):
    self.frame.grid(row=0, column=0, sticky="nsew")
    self.refresh()

  def hide(self):
    self.frame.grid_remove()