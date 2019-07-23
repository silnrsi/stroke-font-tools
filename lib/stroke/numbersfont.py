import sys, os
from fontParts.world import OpenFont

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

numbersource = os.path.join(dir_path,"numbersfont.ufo")
numbers = ["one", "two","three","four","five","six","seven","eight","nine"]
numbersfont = OpenFont(numbersource)
