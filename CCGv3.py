import os
import sys
import tkinter as tk
import customtkinter
import pyperclip
import webbrowser
import keyboard
from tkinter import filedialog
from tkinter import messagebox

settings_data = {
    "blueprint_type": "mannequin",  
    "custom_blueprint": "",
    "width_spacing": 225,
    "length_spacing": 130,
    "height_spacing": 278
}

default_spacing_x = 225
default_spacing_y = 130
default_spacing_z = 278

window =tk.Tk()
window.title("CustomCavesGenerator | v3")
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

window_visible = True

def toggle_window():
    global window_visible
    if window_visible:
        window.withdraw()  
    else:
        window.deiconify() 
    window_visible = not window_visible

keyboard.add_hotkey("F2", toggle_window)

label_title = customtkinter.CTkLabel(window, text="CCG - v3", font=("Arial", 36), text_color="#ffffff", bg_color="#242424")
label_title.place(x=30, y=30)

label_width = customtkinter.CTkLabel(window, text="Width -", font=("Arial", 17), text_color="#ffffff", bg_color="#242424")
label_width.place(x=30, y=120)

label_height = customtkinter.CTkLabel(window, text="Height -", font=("Arial", 17), text_color="#ffffff", bg_color="#242424")
label_height.place(x=30, y=170)

label_length = customtkinter.CTkLabel(window, text="Length -", font=("Arial", 17), text_color="#ffffff", bg_color="#242424")
label_length.place(x=30, y=220)

label_killaoe = customtkinter.CTkLabel(window, text="KillAOE -", font=("Arial", 14), text_color="#ffffff", bg_color="#242424")
label_killaoe.place(x=360, y=120)

entry_width = customtkinter.CTkEntry(window, placeholder_text="Enter Width", font=("Arial", 14),  height=30, width=195 )
entry_width.place(x=130, y=120)

entry_height = customtkinter.CTkEntry(window, placeholder_text="Enter Height", font=("Arial", 14), height=30, width=195)
entry_height.place(x=130, y=170)

entry_length = customtkinter.CTkEntry(window, placeholder_text="Enter Length", font=("Arial", 14), height=30, width=195 )
entry_length.place(x=130, y=220)

entry_CCC = customtkinter.CTkEntry(window, placeholder_text="Enter CCC", font=("Arial", 14), height=30, width=200 )
entry_CCC.place(x=360, y=380)

dropdown_killaoe = customtkinter.CTkComboBox(window, values=["100", "500", "1000", "5000", "10000"], font=("Arial", 14), width=100, height=30, state="readonly")
dropdown_killaoe.place(x=470, y=120)
dropdown_killaoe.set("100")

dropdown_Shape = customtkinter.CTkComboBox(window, values=["None", "Cube", "Hollow Cube", "Frame Cube", "Pyramid", "Hollow Pyramid", "Sphere", "Hollow Sphere"], font=("Arial", 14), width=295, height=30, state="readonly")
dropdown_Shape.place(x=30, y=380)
dropdown_Shape.set("None")

output_text = customtkinter.CTkTextbox(window, width=315, height=160, font=("Arial", 14), border_width=2, corner_radius=6, border_color="#565B5E", fg_color="#343638")
output_text.place(x=360, y=160)
output_text.configure(state="disabled")

def generate_command():
    try:
        width = int(entry_width.get())
        height = int(entry_height.get())
        length = int(entry_length.get())
        shape = dropdown_Shape.get()

        blueprint_type = settings_data["blueprint_type"]
        if blueprint_type == "mannequin":
            blueprint = ' "Blueprint\'/Game/Genesis2/Structures/LoadoutMannequin/Structure_LoadoutDummy_Hotbar.Structure_LoadoutDummy_Hotbar\'" '
        elif blueprint_type == "tribute termial":
            blueprint = ' "Blueprint\'/Game/PrimalEarth/Structures/TributeTerminal_Base.TributeTerminal_Base\'" '
        elif blueprint_type == "custom-blueprint":
            blueprint = settings_data["custom_blueprint"]
        else:
            blueprint = ""

        spacing_x = settings_data["width_spacing"]
        spacing_y = settings_data["length_spacing"]
        spacing_z = settings_data["height_spacing"]

        coords = []

        if shape == "None":
    
            for i in range(0, height * spacing_z, spacing_z):
                for j in range(0, width * spacing_x, spacing_x):
                    for k in range(0, length * spacing_y, spacing_y):
                        coords.append((j, k, i))

        elif shape == "Cube":
            for i in range(0, height * spacing_z, spacing_z):
                for j in range(0, width * spacing_x, spacing_x):
                    for k in range(0, length * spacing_y, spacing_y):
                        coords.append((j, k, i))

        elif shape == "Hollow Cube":
            for i in range(0, height * spacing_z, spacing_z):
                for j in range(0, width * spacing_x, spacing_x):
                    for k in range(0, length * spacing_y, spacing_y):
                    
                        if i == 0 or i == (height-1)*spacing_z or \
                           j == 0 or j == (width-1)*spacing_x or \
                           k == 0 or k == (length-1)*spacing_y:
                            coords.append((j, k, i))

        elif shape == "Frame Cube":
            for i in range(0, height * spacing_z, spacing_z):
                for j in range(0, width * spacing_x, spacing_x):
                    for k in range(0, length * spacing_y, spacing_y):
                        edges = sum([i == 0, i == (height-1)*spacing_z,
                                     j == 0, j == (width-1)*spacing_x,
                                     k == 0, k == (length-1)*spacing_y])
                        if edges >= 2:
                            coords.append((j, k, i))

        elif shape == "Pyramid":
          
            for i in range(height):
                layer_width = width - 2*i
                layer_length = length - 2*i
                if layer_width <= 0 or layer_length <= 0:
                    break
                z = i * spacing_z
                for j in range(layer_width):
                    for k in range(layer_length):
                        x = (j + i) * spacing_x
                        y = (k + i) * spacing_y
                        coords.append((x, y, z))

        elif shape == "Hollow Pyramid":
            for i in range(height):
                layer_width = width - 2*i
                layer_length = length - 2*i
                if layer_width <= 0 or layer_length <= 0:
                    break
                z = i * spacing_z
                for j in range(layer_width):
                    for k in range(layer_length):
                        x = (j + i) * spacing_x
                        y = (k + i) * spacing_y
                        
                        if j == 0 or j == layer_width-1 or k == 0 or k == layer_length-1:
                            coords.append((x, y, z))

        elif shape == "Sphere" or shape == "Hollow Sphere":
            
            cx = (width - 1) * spacing_x / 2
            cy = (length - 1) * spacing_y / 2
            cz = (height - 1) * spacing_z / 2
            radius_x = (width - 1) * spacing_x / 2
            radius_y = (length - 1) * spacing_y / 2
            radius_z = (height - 1) * spacing_z / 2

            for i in range(height):
                for j in range(width):
                    for k in range(length):
                        x = j * spacing_x
                        y = k * spacing_y
                        z = i * spacing_z
                        dx = (x - cx) / radius_x if radius_x else 0
                        dy = (y - cy) / radius_y if radius_y else 0
                        dz = (z - cz) / radius_z if radius_z else 0
                        dist = dx*dx + dy*dy + dz*dz
                        if shape == "Sphere":
                            if dist <= 1.0:
                                coords.append((x, y, z))
                        else:  
                            if 0.9 <= dist <= 1.0:
                                coords.append((x, y, z))

        else:
            coords = []  

       
        result = ""
        for (x, y, z) in coords:
            result += f'c spawnactor {blueprint} {x} {y} {z} | \n'

        output_text.configure(state="normal")
        output_text.delete(1.0, "end")
        output_text.insert("end", result)
        output_text.configure(state="disabled")

        window.clipboard_clear()
        window.clipboard_append(result)
        window.update()

    except ValueError:
        output_text.configure(state="normal")
        output_text.delete(1.0, "end")
        output_text.insert("end", "Please enter valid numbers.")
        output_text.configure(state="disabled")

def copy_text():
    window.clipboard_clear()
    window.clipboard_append(output_text.get("1.0", "end"))
    window.update()

def clear_all():
    entry_width.delete(0, 'end')
    entry_height.delete(0, 'end')
    entry_length.delete(0, 'end')

    output_text.configure(state="normal")  
    output_text.delete(1.0, 'end')
    output_text.configure(state="disabled") 

def browse_path():
    global entry_path_var  
    path = filedialog.askdirectory()
    if path:
        entry_path_var.set(path)

def save_output():
    path = settings_data.get("save_path", "")
    if not path:
        print("missing Save Path")
        return

    try:
        width = int(entry_width.get())
        height = int(entry_height.get())
        length = int(entry_length.get())
    except ValueError:
        print("no valid number for Width, Height or Length.")
        return

    
    blueprint_type = settings_data.get("blueprint_type", "unknown")
    if blueprint_type == "custom":
        blueprint_label = "custom"
    elif blueprint_type.startswith("tribute"):
        blueprint_label = "tribute"
    else:
        blueprint_label = blueprint_type  

   
    shape_label = dropdown_Shape.get() 

    
    filename = f"{width}x_{height}x_{length}x_{blueprint_label}_{shape_label}.txt"
    full_path = os.path.join(path, filename)

    try:
        with open(full_path, "w") as f:
            f.write(output_text.get("1.0", "end").strip())
        print(f"File Saved {full_path}")
    except Exception as e:
        print(f"Error while saving {e}")

entry_path_var = tk.StringVar()
entry_path_var.set(settings_data.get("save_path", ""))

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

btn_generate = customtkinter.CTkButton(window, text="Generate Command & Copy", command=generate_command, font=("Arial", 16), text_color="#000000", height=30, width=295, fg_color="#0092ff")
btn_generate.place(x=30, y=280)

btn_copyAOE = customtkinter.CTkButton(window, text="Copy", command=on_copyAOE_button_click, font=("Arial", 15), text_color="#000000", height=30, width=95, fg_color="#ffd041")
btn_copyAOE.place(x=580, y=120)

btn_clear = customtkinter.CTkButton(window, text="Clear",  font=("Arial", 15), text_color="#000000", height=30, width=145, fg_color="#ff1706", command=clear_all)
btn_clear.place(x=30, y=330)

btn_save = customtkinter.CTkButton(window, text="Save", command=save_output, font=("Arial", 15), text_color="#000000", height=30, width=145, fg_color="#43dc00")
btn_save.place(x=180, y=330)

btn_copy_3_3 = customtkinter.CTkButton(window, text="Copy 3/3", command=on_copy_3_3_button_click, font=("undefined", 15), text_color="#000000", height=30, width=95, fg_color="#ac53ff",)
btn_copy_3_3.place(x=580, y=330)

btn_copy_2_3 = customtkinter.CTkButton(window, text="Copy 2/3",  command=on_copy_2_3_button_click, font=("undefined", 15), text_color="#000000", height=30, width=95, fg_color="#ac53ff")
btn_copy_2_3.place(x=470, y=330)

btn_copy_1_3 = customtkinter.CTkButton(window, text="Copy 1/3", command=on_copy_1_3_button_click, font=("undefined", 15), text_color="#000000", height=30, width=95, fg_color="#ac53ff")
btn_copy_1_3.place(x=360, y=330)

btn_copy_spi = customtkinter.CTkButton(window, text="Copy with SPI", command=on_copySPI_button_click, font=("undefined", 15), text_color="#000000", height=30, width=105, fg_color="#ffd041")
btn_copy_spi.place(x=570, y=380)

btn_discord = customtkinter.CTkButton(window, text="Discord", command=lambda: os.system("start https://discord.gg/RtEYex2vmu"), font=("Arial", 15), text_color="#000000", height=30, width=100, fg_color="#ffffff")
btn_discord.place(x=580, y=30)

btn_Github = customtkinter.CTkButton(window, text="Github", command=lambda: os.system("start https://github.com/N38X/CCG"), font=("Arial", 15), text_color="#000000", height=30, width=100, fg_color="#ffffff")
btn_Github.place(x=470, y=30)

btn_settings = customtkinter.CTkButton(window, text="Settings", command=lambda: open_settings(), font=("Arial", 15), text_color="#000000", height=30, width=100, fg_color="#ffffff")
btn_settings.place(x=360, y=30)

def open_settings():
    settings_win = tk.Toplevel(window)
    settings_win.title("Settings")
    settings_win.geometry("600x250")
    settings_win.resizable(False, False)
    settings_win.configure(bg="#242424")

    global entry_path_var 

    entry_path_var = tk.StringVar()
    entry_path_var.set(settings_data.get("save_path", ""))

    label_SavePath = customtkinter.CTkLabel(settings_win, text="Save Path", font=("Arial", 14), text_color="#ffffff")
    label_SavePath.place(x=20, y=140)

    entry_path_var = tk.StringVar()
    entry_path_var.set(settings_data.get("save_path", ""))  

    entry_path = customtkinter.CTkEntry(settings_win, textvariable=entry_path_var, width=170)
    entry_path.place(x=160, y=140)

    btn_browse = customtkinter.CTkButton(settings_win, text="Browse", command=browse_path, width=95, border_width=2, corner_radius=6, border_color="#565B5E", fg_color="#343638" )
    btn_browse.place(x=350, y=140)
    
    label_Settings = customtkinter.CTkLabel(settings_win, text="CCG - v3 - Settings", font=("Arial", 24), text_color="#ffffff", bg_color="#242424")
    label_Settings.place(x=20, y=15)

    label_SpacingInfo = customtkinter.CTkLabel(settings_win, text="Width,       Length,       Height", font=("Arial", 14), text_color="#ffffff", bg_color="#242424")
    label_SpacingInfo.place(x=375, y=100)

    label_bp = customtkinter.CTkLabel(settings_win, text="Edit Type:", font=("Arial", 14), text_color="#ffffff", bg_color="#242424")
    label_bp.place(x=20, y=60)

    blueprint_var = tk.StringVar(value=settings_data["blueprint_type"])

    bp_dropdown = customtkinter.CTkComboBox(settings_win, values=["mannequin", "tribute termial", "custom-blueprint"], variable=blueprint_var, width=170, height=30, state="readonly")
    bp_dropdown.place(x=160, y=60)

    custom_blueprint_value = settings_data.get("custom_blueprint", "")

    if custom_blueprint_value:
        custom_bp_entry = customtkinter.CTkEntry(settings_win, width=250)
        custom_bp_entry.insert(0, custom_blueprint_value)
    else:
        custom_bp_entry = customtkinter.CTkEntry(settings_win, width=250, placeholder_text="Enter Blueprint Path")

    def update_custom_bp_visibility(*args):
        if blueprint_var.get() == "custom-blueprint":
            custom_bp_entry.place(x=340, y=60)
            custom_bp_entry.configure(state="normal")
        else:
            custom_bp_entry.place_forget()

    blueprint_var.trace("w", update_custom_bp_visibility)
    update_custom_bp_visibility()  

    label_spacing = customtkinter.CTkLabel(settings_win, text="Spacing: (X, Y, Z)", font=("Arial", 14), text_color="#ffffff", bg_color="#242424")
    label_spacing.place(x=20, y=100)

    entry_spacing_x = customtkinter.CTkEntry(settings_win, width=50)
    entry_spacing_x.place(x=160, y=100)
    entry_spacing_x.insert(0, str(settings_data["width_spacing"]))

    entry_spacing_y = customtkinter.CTkEntry(settings_win, width=50)
    entry_spacing_y.place(x=220, y=100)
    entry_spacing_y.insert(0, str(settings_data["length_spacing"]))

    entry_spacing_z = customtkinter.CTkEntry(settings_win, width=50)
    entry_spacing_z.place(x=280, y=100)
    entry_spacing_z.insert(0, str(settings_data["height_spacing"]))

    def update_custom_bp_state(*args):

        if blueprint_var.get() == "custom":
            custom_bp_entry.configure(state="normal")
        else:
            custom_bp_entry.configure(state="disabled")

    blueprint_var.trace("w", update_custom_bp_state)
    update_custom_bp_state()

    def reset_spacing():
        entry_spacing_x.delete(0, "end")
        entry_spacing_x.insert(0, str(default_spacing_x))
        entry_spacing_y.delete(0, "end")
        entry_spacing_y.insert(0, str(default_spacing_y))
        entry_spacing_z.delete(0, "end")
        entry_spacing_z.insert(0, str(default_spacing_z))

    def save_settings():
        try:
            settings_data["blueprint_type"] = blueprint_var.get()
            settings_data["custom_blueprint"] = custom_bp_entry.get()
            settings_data["width_spacing"] = int(entry_spacing_x.get())
            settings_data["length_spacing"] = int(entry_spacing_y.get())
            settings_data["height_spacing"] = int(entry_spacing_z.get())
            settings_data["save_path"] = entry_path_var.get() 
            settings_win.destroy()
        except ValueError:
           
            error_label.configure(text="Please enter valid numbers.", text_color="red")

   
    save_btn = customtkinter.CTkButton(settings_win, text="Save", command=save_settings,  fg_color="#68cc3e", text_color="#242424", font=("Arial", 14) )
    save_btn.place(x=20, y=200)

    reset_btn = customtkinter.CTkButton(settings_win, text="Reset Spacing", command=reset_spacing)
    reset_btn.place(x=170, y=200)

   
    error_label = customtkinter.CTkLabel(settings_win, text="", font=("Arial", 12), text_color="red", bg_color="#242424")
    error_label.place(x=350, y=200)

window.mainloop()

