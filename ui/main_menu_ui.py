from tkinter import *
from typing import Callable, Optional
from config.settings import config
import os

class MainMenuUI:
    def __init__(self, master: Frame, on_start_flashcards: Callable, on_show_words: Callable = None, on_show_sentences: Optional[Callable] = None):
        self.on_start_flashcards = on_start_flashcards
        self.on_show_words = on_show_words
        self.on_show_sentences = on_show_sentences
        self.root = master.winfo_toplevel()
        self.frame = Frame(master, bg=config.BACKGROUND_COLOR)
        self.canvas = None
        self.card_front_img = None
        self._build()

    def _build(self):
        # Canvas matches flashcard layout
        self.canvas = Canvas(self.frame, width=800, height=526, bg=config.BACKGROUND_COLOR, highlightthickness=0)

        # Title + subtitle
        self.canvas.create_text(400, 140, text="Language Learning", font=("Arial", 40, "italic"), fill="black")
        self.canvas.create_text(400, 200, text="Select a mode", font=("Arial", 24, "bold"), fill="black")

        # Buttons on the card
        button_font = ("Arial", 16, "bold")
        btn_frame = Frame(self.canvas, bg=config.BACKGROUND_COLOR, highlightthickness=0)

        start_btn = Button(btn_frame, text="Start Flashcards", font=button_font, width=22,
                          command=self.on_start_flashcards, relief="flat", bg="#E8E8E8", activebackground="#91C2AF")
        word_btn = Button(btn_frame, text="Learned Words", font=button_font, width=22,
                          command=self.on_show_words, relief="flat", bg="#E8E8E8", activebackground="#91C2AF")
        sentence_btn = Button(btn_frame, text="Learned Sentences", font=button_font, width=22,
                          command=self.on_show_sentences, relief="flat", bg="#E8E8E8", activebackground="#91C2AF")

        start_btn.pack(pady=6)
        word_btn.pack(pady=6)
        sentence_btn.pack(pady=6)

        self.canvas.create_window(400, 330, window=btn_frame)
        self.canvas.grid(row=0, column=0)

    # Screen control
    def show(self):
        self.frame.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        self.frame.grid_remove()