import os
import sys
import tkinter as tk
import customtkinter
import pyperclip
import webbrowser
from tkinter import filedialog


window =tk.Tk()
window.title("CustomCavesGenerator | v2")
window.geometry("700x450")
window.configure(bg="#242424")
window.resizable(False, False)


if getattr(sys, 'frozen', False): 
    icon_path = os.path.join(sys._MEIPASS, "NX.ico")
else: 
    icon_path = os.path.join(os.getcwd(), "NX.ico")


try:
    window.iconbitmap(icon_path)  
except Exception as e:
    print(f"Error setting icon: {e}")



# Labels
label_title = customtkinter.CTkLabel(window, text="CCG - v2", font=("Arial", 36), text_color="#ffffff", bg_color="#242424")
label_title.place(x=30, y=30)

label_width = customtkinter.CTkLabel(window, text="Width -", font=("Arial", 17), text_color="#ffffff", bg_color="#242424")
label_width.place(x=30, y=120)

label_height = customtkinter.CTkLabel(window, text="Height -", font=("Arial", 17), text_color="#ffffff", bg_color="#242424")
label_height.place(x=30, y=170)

label_length = customtkinter.CTkLabel(window, text="Length -", font=("Arial", 17), text_color="#ffffff", bg_color="#242424")
label_length.place(x=30, y=220)

label_killaoe = customtkinter.CTkLabel(window, text="KillAOE -", font=("Arial", 14), text_color="#ffffff", bg_color="#242424")
label_killaoe.place(x=360, y=120)


# Entrys
entry_width = customtkinter.CTkEntry(window, placeholder_text="Enter Width", font=("Arial", 14), text_color="#000000", height=30, width=195, border_width=2, corner_radius=6, border_color="#000000", fg_color="#F0F0F0")
entry_width.place(x=130, y=120)

entry_height = customtkinter.CTkEntry(window, placeholder_text="Enter Height", font=("Arial", 14), text_color="#000000", height=30, width=195, border_width=2, corner_radius=6, border_color="#000000", fg_color="#F0F0F0")
entry_height.place(x=130, y=170)

entry_length = customtkinter.CTkEntry(window, placeholder_text="Enter Length", font=("Arial", 14), text_color="#000000", height=30, width=195, border_width=2, corner_radius=6, border_color="#000000", fg_color="#F0F0F0")
entry_length.place(x=130, y=220)

entry_path = customtkinter.CTkEntry(window, placeholder_text="Save Path", font=("Arial", 14), text_color="#000000", height=30, width=195, border_width=2, corner_radius=6, border_color="#000000", fg_color="#F0F0F0")
entry_path.place(x=130, y=380)

entry_CCC = customtkinter.CTkEntry(window, placeholder_text="Enter CCC", font=("Arial", 14), text_color="#000000", height=30, width=200, fg_color="#F0F0F0")
entry_CCC.place(x=360, y=380)

# Dropdown
dropdown_killaoe = customtkinter.CTkComboBox(window, values=["100", "500", "1000", "5000", "10000"], font=("Arial", 14), text_color="#000000", width=100, height=30, border_width=1, corner_radius=6, border_color="#000000", fg_color="#F0F0F0", dropdown_fg_color="#242424", dropdown_text_color="#ffffff", state="readonly")
dropdown_killaoe.place(x=455, y=120)
dropdown_killaoe.set("100")

# Text
output_text = customtkinter.CTkTextbox(window, width=315, height=160, font=("Arial", 14), text_color="#000000", border_width=2, corner_radius=6, border_color="#000000", fg_color="#F0F0F0")
output_text.place(x=360, y=160)
output_text.configure(state="disabled")

# Function
def generate_command():
    try:
        width = int(entry_width.get())
        height = int(entry_height.get())
        length = int(entry_length.get())

        result = ""
        for i in range(0, height * 278, 278):
            for j in range(0, width * 225, 225):
                for k in range(0, length * 130, 130):
                    result += f"c spawnactor \"Blueprint'/Game/Genesis2/Structures/LoadoutMannequin/Structure_LoadoutDummy_Hotbar.Structure_LoadoutDummy_Hotbar'\" {j} {k} {i} | \n"

        output_text.configure(state="normal")
        output_text.delete(1.0, "end")
        output_text.insert("end", result)
        output_text.configure(state="disabled")

    except ValueError:
        output_text.configure(state="normal")
        output_text.delete(1.0, "end")
        output_text.insert("end", "Please enter valid numbers.")
        output_text.configure(state="disabled")

def copy_text():
    window.clipboard_clear()
    window.clipboard_append(output_text.get("1.0", "end"))
    window.update()

def clear_text():
    output_text.configure(state="normal")
    output_text.delete(1.0, "end")
    output_text.configure(state="disabled")
    entry_width.delete(0, "end")
    entry_height.delete(0, "end")
    entry_length.delete(0, "end")
    entry_CCC.delete(0, "end")

def browse_path():
    path = filedialog.askdirectory()
    entry_path.delete(0, "end")
    entry_path.insert(0, path)

def save_output():
    file_path = entry_path.get()
    width = entry_width.get()
    height = entry_height.get()
    length = entry_length.get()

    if not file_path:
        entry_path.delete(0, "end")
        entry_path.insert(0, "Please select a save location")
        return

    file_name = f"{width}_{height}_{length}.txt"
    full_path = os.path.join(file_path, file_name)

    try:
        with open(full_path, "w") as file:
            file.write(output_text.get("1.0", "end-1c"))
        entry_path.delete(0, "end")
        entry_path.insert(0, full_path)

    except Exception:
        pass
    
def generate_and_copy_command(entry_CCC, output_text):
    try:
        values = entry_CCC.get().split() 
        
        if len(values) != 5:  
            raise ValueError("Please enter exactly 5 values for CCC.")
        
        
        x, y, z, yaw, _ = map(float, values)  
        
        command = f"c SPI {x} {y} {z} {yaw} 0"  
        
        final_command = f"{command} | {output_text}" 
        
        pyperclip.copy(final_command)  
        
        entry_CCC.delete(0, "end")  
        entry_CCC.insert(0, "Command copied to clipboard!")  

        entry_CCC.after(5000, lambda: entry_CCC.delete(0, "end") )
        
        return final_command  
    
    except ValueError as e:
        entry_CCC.delete(0, "end")  
        entry_CCC.insert(0, str(e))  
        return str(e) 

def on_copySPI_button_click():  
    entry_CCC_value = entry_CCC.get()  
    output_text_value = output_text.get("1.0", tk.END).strip() 
    
    final_command = generate_and_copy_command(entry_CCC, output_text_value)  
    
    pyperclip.copy(final_command)

def on_copyAOE_button_click():
    killaoe_value = dropdown_killaoe.get()  
    commandAOE = f"c KillAOE structures {killaoe_value}"  
    pyperclip.copy(commandAOE) 

def on_copy_1_3_button_click():
    output_text_value = output_text.get("1.0", tk.END).strip()  
    sections = output_text_value.split('|')  

    
    total_sections = len(sections)
    if total_sections > 1:
        
        first_third = '|'.join(sections[:total_sections//3])  
        pyperclip.copy(first_third.strip())  

def on_copy_2_3_button_click():
    output_text_value = output_text.get("1.0", tk.END).strip()  
    sections = output_text_value.split('|') 

    total_sections = len(sections)
    if total_sections > 1:
       
        second_third = '|'.join(sections[total_sections//3: 2*total_sections//3])
        pyperclip.copy(second_third.strip())  

def on_copy_3_3_button_click():
    output_text_value = output_text.get("1.0", tk.END).strip()  
    sections = output_text_value.split('|')  

    total_sections = len(sections)
    if total_sections > 1:
        
        third_third = '|'.join(sections[2*total_sections//3:])  
        pyperclip.copy(third_third.strip())  


# Buttons
btn_generate = customtkinter.CTkButton(window, text="Generate Command", command=generate_command, font=("Arial", 16), text_color="#000000", height=30, width=295, fg_color="#4f88e3")
btn_generate.place(x=30, y=280)

btn_copy = customtkinter.CTkButton(window, text="Copy", command=copy_text, font=("Arial", 15), text_color="#000000", height=30, width=95, fg_color="#d8da5d")
btn_copy.place(x=30, y=330)

btn_copyAOE = customtkinter.CTkButton(window, text="Copy", command=on_copyAOE_button_click, font=("Arial", 15), text_color="#000000", height=30, width=95, fg_color="#d8da5d")
btn_copyAOE.place(x=580, y=120)

btn_clear = customtkinter.CTkButton(window, text="Clear", command=clear_text, font=("Arial", 15), text_color="#000000", height=30, width=95, fg_color="#e64c4c")
btn_clear.place(x=130, y=330)

btn_save = customtkinter.CTkButton(window, text="Save", command=save_output, font=("Arial", 15), text_color="#000000", height=30, width=95, fg_color="#68cc3e")
btn_save.place(x=230, y=330)

btn_browse = customtkinter.CTkButton(window, text="Browse", command=browse_path, font=("Arial", 14), text_color="#000000", height=30, width=95, fg_color="#F0F0F0")
btn_browse.place(x=30, y=380)

btn_copy_3_3 = customtkinter.CTkButton(window, text="Copy 3/3", command=on_copy_3_3_button_click, font=("undefined", 15), text_color="#000000", height=30, width=95, fg_color="#7c4fa1",)
btn_copy_3_3.place(x=580, y=330)

btn_copy_2_3 = customtkinter.CTkButton(window, text="Copy 2/3",  command=on_copy_2_3_button_click, font=("undefined", 15), text_color="#000000", height=30, width=95, fg_color="#7c4fa1")
btn_copy_2_3.place(x=470, y=330)

btn_copy_1_3 = customtkinter.CTkButton(window, text="Copy 1/3", command=on_copy_1_3_button_click, font=("undefined", 15), text_color="#000000", height=30, width=95, fg_color="#7c4fa1")
btn_copy_1_3.place(x=360, y=330)

btn_copy_spi = customtkinter.CTkButton(window, text="Copy with SPI", command=on_copySPI_button_click, font=("undefined", 15), text_color="#000000", height=30, width=105, fg_color="#b59640")
btn_copy_spi.place(x=570, y=380)

btn_discord = customtkinter.CTkButton(window, text="Discord", command=lambda: os.system("start https://discord.gg/RtEYex2vmu"), font=("Arial", 15), text_color="#ffffff", height=30, width=105, fg_color="#5865f2")
btn_discord.place(x=570, y=40)

btn_Github = customtkinter.CTkButton(window, text="Github", command=lambda: os.system("start https://github.com/N38X/CCG"), font=("Arial", 15), text_color="#ffffff", height=30, width=105, fg_color="#333")
btn_Github.place(x=460, y=40)

# Start
window.mainloop()

