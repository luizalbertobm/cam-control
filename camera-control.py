#!/usr/bin/env python3

import subprocess
import tkinter as tk
from subprocess import call
from tkinter import messagebox


# Variáveis globais
dispositivos = {}
dispositivo_var = None

def listar_dispositivos():
    global dispositivos
    try:
        cmd = "v4l2-ctl --list-devices"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode != 0:
            raise Exception("Erro ao listar dispositivos: " + str(error.decode()))

        devices = {}
        output = output.decode().split('\n')
        device_name = None
        for line in output:
            if ':' in line:
                device_name = line.split('(')[0].strip()
            elif '/dev/video' in line:
                if device_name:
                    devices[device_name] = line.strip()
        dispositivos = devices
        return devices
    except Exception as e:
        messagebox.showerror("Erro", str(e))
        return {}

def atualizar_dispositivo(event):
    global dispositivos, dispositivo_var
    selected_device = dispositivo_var.get()
    print("Dispositivo selecionado:", selected_device, dispositivos[selected_device])

def criar_interface():
    global dispositivo_var, dispositivos
    root = tk.Tk()
    root.title("Painel de Controle da Câmera")

    dispositivo_var = tk.StringVar(root)
    dispositivos = listar_dispositivos()
    if dispositivos:
        dispositivo_var.set(next(iter(dispositivos)))  # default to the first device

    frame_dispositivo = tk.Frame(root)
    tk.Label(frame_dispositivo, text="Escolha o Dispositivo:").pack(side=tk.LEFT)
    dispositivo_menu = tk.OptionMenu(frame_dispositivo, dispositivo_var, *dispositivos.keys())
    dispositivo_menu.pack(fill=tk.X, expand=True)
    frame_dispositivo.pack(fill=tk.X, expand=True)

    dispositivo_var.trace("w", atualizar_dispositivo)

    # Aqui você pode adicionar os outros controles da sua interface...

def update_control(control, value):
    command = f"v4l2-ctl -d /dev/video2 -c {control}={value}"
    call(command, shell=True)

def create_slider(parent, label, control, min_val, max_val, step, default_val):
    frame = tk.Frame(parent)
    tk.Label(frame, text=label).pack(side=tk.LEFT)
    slider = tk.Scale(frame, from_=min_val, to=max_val, resolution=step, orient='horizontal',
                      command=lambda value, c=control: update_control(c, value))
    slider.set(default_val)
    slider.pack(fill=tk.X, expand=True)
    frame.pack(fill=tk.X, expand=True)

root = tk.Tk()
root.title("Camera Control Panel")

# Create sliders for each control
create_slider(root, "Brightness", "brightness", 0, 255, 1, 128)
create_slider(root, "Contrast", "contrast", 0, 255, 1, 128)
create_slider(root, "Saturation", "saturation", 0, 255, 1, 128)
create_slider(root, "Gain", "gain", 0, 255, 1, 0)
create_slider(root, "Sharpness", "sharpness", 0, 255, 1, 128)
create_slider(root, "Backlight Compensation", "backlight_compensation", 0, 1, 1, 0)
create_slider(root, "Zoom", "zoom_absolute", 100, 140, 10, 100)
create_slider(root, "Pan", "pan_absolute", -36000, 36000, 3600, 0)
create_slider(root, "Tilt", "tilt_absolute", -36000, 36000, 3600, 0)

# Special handling for menu and boolean types
power_line_frequency_options = {0: 'Disabled', 1: '50 Hz', 2: '60 Hz'}
auto_exposure_options = {0: 'Manual', 1: 'Auto', 2: 'Shutter Priority', 3: 'Aperture Priority'}

def create_option_menu(parent, label, control, options, default_val):
    frame = tk.Frame(parent)
    tk.Label(frame, text=label).pack(side=tk.LEFT)
    variable = tk.StringVar(frame)
    variable.set(options[default_val])
    option_menu = tk.OptionMenu(frame, variable, *options.values(),
                                command=lambda value: update_control(control, list(options.keys())[list(options.values()).index(value)]))
    option_menu.pack(fill=tk.X, expand=True)
    frame.pack(fill=tk.X, expand=True)

create_option_menu(root, "Power Line Frequency", "power_line_frequency", power_line_frequency_options, 1)
create_option_menu(root, "Auto Exposure", "auto_exposure", auto_exposure_options, 3)

def create_checkbox(parent, label, control, default_val):
    var = tk.IntVar(value=default_val)
    checkbox = tk.Checkbutton(parent, text=label, variable=var,
                              command=lambda: update_control(control, var.get()))
    checkbox.pack()

create_checkbox(root, "White Balance Automatic", "white_balance_automatic", 1)
create_checkbox(root, "Exposure Dynamic Framerate", "exposure_dynamic_framerate", 0)
create_checkbox(root, "Focus Automatic Continuous", "focus_automatic_continuous", 1)

if __name__ == "__main__":
    criar_interface()
root.mainloop()