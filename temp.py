import pygame
import tkinter as tk
from tkinter import *
import os


def main():
    root = tk.Tk()
    embed = tk.Frame(root, width=500, height=500)
    embed.grid(columnspan = 600, rowspan = 500)
    embed.pack(side = LEFT)

    buttonwin = tk.Frame(root, width = 75, height = 500)
    buttonwin.pack(side = LEFT)

    button1 = Button(buttonwin, text='Draw')
    button1.pack(side=LEFT, padx=20, pady=20)

    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    screen = pygame.display.set_mode((500, 500))
    screen.fill(pygame.Color(255, 255, 255))
    pygame.display.init()
    pygame.display.update()

    while True:
        pygame.display.update()
        root.update()

main()


