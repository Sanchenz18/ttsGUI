import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import ttk
import configparser

CONFIG_FILE = "config.ini"

def load_config():
    config = configparser.ConfigParser()
    if config.read(CONFIG_FILE):
        return config['DEFAULT']
    return {}

def save_config(config):
    config = configparser.ConfigParser()
    config['DEFAULT'] = config_data
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def send_request():
    url = "http://yurun.fun:5050/v1/audio/speech"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + entry_auth.get()
    }
    data = {
        "input": entry_input.get("1.0", tk.END).strip(),
        "voice": entry_voice.get(),
        "response_format": "mp3",
        "speed": scale_speed.get() / 100
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            with open(entry_output.get() + ".mp3", "wb") as f:
                f.write(response.content)
            messagebox.showinfo("Success", "Response saved")
        else:
            messagebox.showerror("Error", f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", str(e))
    
    save_config_callback()

# 加载配置
config_data = load_config()

# 创建主窗口
root = tk.Tk()
root.title("TTS文生语音")

# Authorization
label_auth = tk.Label(root, text="Authorization:")
label_auth.grid(row=0, column=0, padx=10, pady=5)
entry_auth = tk.Entry(root, width=50)
entry_auth.insert(0, config_data.get('auth', ""))
entry_auth.grid(row=0, column=1, padx=10, pady=5)

# Input
label_input = tk.Label(root, text="Input:")
label_input.grid(row=1, column=0, padx=10, pady=5)
entry_input = tk.Text(root, height=5, width=50)
entry_input.insert(tk.END, config_data.get('input', "我是你的ai助手，有什么可以帮助你？"))
entry_input.grid(row=1, column=1, padx=10, pady=5)

# Voice
label_voice = tk.Label(root, text="Voice:")
label_voice.grid(row=2, column=0, padx=10, pady=5)
entry_voice = tk.Entry(root, width=50)
entry_voice.insert(0, config_data.get('voice', "zh-CN-YunyangNeural"))
entry_voice.grid(row=2, column=1, padx=10, pady=5)

# Output
label_output = tk.Label(root, text="Output:")
label_output.grid(row=3, column=0, padx=10, pady=5)
entry_output = tk.Entry(root, width=50)
entry_output.insert(0, config_data.get('output', "out"))
entry_output.grid(row=3, column=1, padx=10, pady=5)

# Speed
label_speed = tk.Label(root, text="Speed:")
label_speed.grid(row=4, column=0, padx=10, pady=5)
scale_speed = ttk.Scale(root, from_=80, to=150, orient=tk.HORIZONTAL, length=200)
scale_speed.set(int(float(config_data.get('speed', "1.0")) * 100))
scale_speed.grid(row=4, column=1, padx=10, pady=5)

# Save Config
def save_config_callback():
    config_data['auth'] = entry_auth.get()
    config_data['input'] = entry_input.get("1.0", tk.END).strip()
    config_data['voice'] = entry_voice.get()
    config_data['output'] = entry_output.get()
    config_data['speed'] = str(scale_speed.get() / 100)
    save_config(config_data)

# Send Button
send_button = tk.Button(root, text="Send Request", command=send_request)
send_button.grid(row=6, column=0, columnspan=2, pady=10)

# 运行主循环
root.mainloop()