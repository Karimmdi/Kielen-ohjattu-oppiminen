from tkinter import *
from tkinter import ttk
from typing import Callable
from config.settings import config
from models.word import WordManager
import os

class WordsUI:
  def __init__(self, master: Frame, word_manager: WordManager, on_back: Callable):
    self.word_manager = word_manager
    self.on_back = on_back

    self.root = master.winfo_toplevel()
    self.frame = Frame(master, bg=config.BACKGROUND_COLOR)
    
    self.tree = None
    self._build()

  def _build(self):
    # --- Setup custom style for ttk widgets ---
    style = ttk.Style()
    style.theme_use("default")
    
    # Style for the Treeview
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
              background=[('active', '#D0D0D0')]) # Click effect
              
    # Style for the Scrollbar
    style.configure("Custom.Vertical.TScrollbar",
                    gripcount=0,
                    background="#E8E8E8", # Scrollbar handle
                    troughcolor=config.BACKGROUND_COLOR, # Scrollbar track
                    bordercolor=config.BACKGROUND_COLOR,
                    arrowcolor="black")

    # This frame just holds the titles and won't expand
    header_frame = Frame(self.frame, bg=config.BACKGROUND_COLOR)
    header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    # Add titles as Labels
    title_label = Label(header_frame, text="Learned Words", font=("Arial", 40, "italic"), bg=config.BACKGROUND_COLOR)
    title_label.pack()
    
    subtitle_label = Label(header_frame, text="Finnish — English", font=("Arial", 20, "bold"), bg=config.BACKGROUND_COLOR)
    subtitle_label.pack()
    
    table_frame = Frame(self.frame, bg=config.BACKGROUND_COLOR)
    table_frame.grid(row=1, column=0, sticky="nsew", pady=12)

    # Make row 1 (table) expand, but not row 0 (header)
    self.frame.grid_rowconfigure(0, weight=0)
    self.frame.grid_rowconfigure(1, weight=1)
    self.frame.grid_columnconfigure(0, weight=1)

    columns = ("finnish", "english")
    self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Custom.Treeview")
    self.tree.heading("finnish", text="Finnish", anchor=CENTER)
    self.tree.heading("english", text="English", anchor=CENTER)
    self.tree.column("finnish", width=380, anchor=CENTER)
    self.tree.column("english", width=380, anchor=CENTER)
    
    # Different style for every other row
    self.tree.tag_configure('oddrow', background='white', font=("Arial", 13, "bold"))

    # Scrollbar
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview, style="Custom.Vertical.TScrollbar")
    self.tree.configure(yscrollcommand=vsb.set)

    # Grid the tree and scrollbar
    self.tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")

    # Configure table_frame grid
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

  def refresh(self):
    # Reload from file each time
    for row in self.tree.get_children():
      self.tree.delete(row)
    words = self.word_manager.get_learned_words()
    
    # Every other row is 'oddrow' style
    for i, w in enumerate(words):
      tag = 'oddrow' if i % 2 == 1 else ''
      self.tree.insert("", "end", values=(w.finnish, w.english), tags=(tag,))

  # Screen control
  def show(self):
    self.frame.grid(row=0, column=0, sticky="nsew")
    self.refresh()

  def hide(self):
    self.frame.grid_remove()