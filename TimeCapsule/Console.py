import PyBear.TimeCapsule.Core as Core

def AF(Clue):
    return input(Clue)
Core.AskFunction = AF

while(True):
    Input = input("Code: ")
    Core.Cast(Input)