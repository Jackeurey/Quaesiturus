# -*- coding: utf-8 -*-
import webbrowser
from pynput import keyboard
from pynput.keyboard import Key, Controller
import clipboard
import threading
import time

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path),preferred=True)

control = Controller()

# Copying from PDF can be buggy, this removes the 'artifacts' from the PDF copy  
def clean_macron_artifacts(x):
  x = x.replace("a","ā")
  x = x.replace("e","ē")
  x = x.replace("ı","ī")
  x = x.replace("o","ō")
  x = x.replace("u","ū")
  return x

#This uses a closure that allows me reuse code. it returns the procedure that has the proper link that will be opened when the hot keys are pressed
def on_activate(link):
  def action():
    # These keys need to be released or else it does not read the hot keys correctly
    control.release(Key.ctrl)
    control.release(Key.alt)

    #Takes the old clipboard contents
    old_clipboard = clipboard.paste()

    with control.pressed(Key.ctrl):
      control.press('c')
      control.release('c')
    # There needs to be a delay or the clipboard will not load properly
    time.sleep(0.1)
    #Open webpage with dictionary entry open.
    webbrowser.get('chrome').open(link + clean_macron_artifacts(clipboard.paste().strip()), new=0)
    #load old content back into the system clipboard
    clipboard.copy(old_clipboard)
  return action

# Just cleans input and puts it in the clipboard
def copy_clean():
  time.sleep(0.1)
  clipboard.copy(clean_macron_artifacts(clipboard.paste()))

# Creates hot keys for each website.
def set_up():
  with keyboard.GlobalHotKeys(
    {'<ctrl>+<alt>': on_activate('https://www.latin-is-simple.com/en/vocabulary/search/?q='),
     '<alt>+1' : on_activate('https://www.online-latin-dictionary.com/latin-english-dictionary.php?parola='),
     '<ctrl>+c': copy_clean,
     '<alt>+2': on_activate('https://www.latin-is-simple.com/en/analysis/?text=+')}) as h:
    h.join()

print("Starting Quaesiturus...")
set_up()
