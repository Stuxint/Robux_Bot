from selenium import webdriver
from selenium.webdriver.edge.service import Service
import google.generativeai as genai
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import font
from tkinter import messagebox
import os, sys, threading, google.generativeai as genai, time
from selenium.webdriver.edge.options import Options as EdgeOptions

genai.configure(api_key="")
model = genai.GenerativeModel('gemini-2.0-flash')

prompt = """
Generate one example of text which can be used to search microsoft bing, in order to get Microsoft reward points.
It can be abotu anything, related to science, politics, countries, etc.(just make it random and it should lead to me getting points)
P.S: JUST GIVE ME THE TEXT, NOTHING ELSE!!!!!!!!!!!!!!!!
Example Output: Population of Iceland
"""




root = Tk()
root.title('Robux Bot')
root.configure(background="#565656")
root.geometry("295x350")
root.resizable(False, False)

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # For development, use the current working directory
        base_path = os.path.abspath(".")

    # Construct the full path to the resource
    return os.path.join(base_path, relative_path)

photo = resource_path("RB_Logo.png")
if os.path.exists(photo): #check if file exists before trying to load
    try:
        icon = PhotoImage(file=photo)
        root.iconphoto(False, icon)
    except TclError as e:
        print(f"Error loading icon: {e}")
else:
    print(f"Icon not found at {photo}")

#label 4
label4 = None


#Fonts
roblox_font = font.Font(family="Gotham Black", size=21)
roblox_font2 = font.Font(family="Gotham Black", size=15)
roblox_font3 = font.Font(family="Courier", size=15, weight="bold")
roblox_font4 = font.Font(family="Courier", size=11)
roblox_font5 = font.Font(family="Gotham Black", size=14)

#Func which handles point mining
def on_enter_pressed():
    global label4

    options = EdgeOptions()
    options.add_argument("--headless=new")
    edge_driver_path = resource_path("msedgedriver.exe")
    service = Service(edge_driver_path)
    service.creation_flags = 0x08000000
    web = webdriver.Edge(options=options, service=service)

    entry.config(state=DISABLED)

    if 'label4' in globals() and label4 is not None and label4.winfo_exists():
        label4.destroy()
        label4 = None        
           
            
    if not entry.get():
            messagebox.showwarning("No Number Was Given", "Please provide number of searches in order to start bot")

    else:
            b = entry.get()
            a = int(b)
            c = 0


            for c in range(a):
                web.get("https://www.bing.com")

                answer = model.generate_content([prompt], stream=False)
                response = answer.text.strip()

                search = web.find_element('xpath', '//*[@id="sb_form_q"]')
                search.send_keys(f'{response}')
                time.sleep(2)
                search.send_keys(Keys.ENTER)

                if 'label4' in globals() and label4 is not None and label4.winfo_exists():
                    label4.config(text=f'Status: {round(((c + 1) / a) * 100)}%')
                else:
                    label4 = Label(root, text=f'Status: {round(((c + 1) / a) * 100)}%', font=roblox_font5, fg='white', bg="#565656")
                    label4.place(x=75, y=225)  # Consistent position

                time.sleep(7)
    entry.config(state=NORMAL)        
    entry.delete(0, END)        

def start_thread(event):                
    thread = threading.Thread(target=on_enter_pressed)
    thread.start()           
        
    
#Labels and entries
label = Label(root, text='Robux Bot', fg='white', bg="#565656", font=roblox_font)
label.pack()

label2 = Label(root, text='Please enter # of times\nyou wish to search: ', fg='white', bg="#565656", font=roblox_font2)
label2.pack(pady=20)

entry = Entry(root, fg='black', bg='white', font=roblox_font3, width=16, justify=CENTER)
entry.pack(pady=22, padx=10)
entry.focus_set()
entry.bind("<Return>", start_thread)


root.mainloop()