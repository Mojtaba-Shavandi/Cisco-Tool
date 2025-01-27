import tkinter as tk
from tkinter import ttk
from netmiko import ConnectHandler

def execute_config():
    # Getting user input
    ip = entry_ip.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    enable_secret = entry_enable_secret.get().strip()
    protocol = protocol_var.get().strip()

    # Check if fields are empty
    if not ip or not username or not password or not enable_secret:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Error: Please fill in all fields.")
        result_text.config(state=tk.DISABLED)
        return

    # Select device type based on protocol
    device_type = 'cisco_ios_ssh' if protocol == 'SSH' else 'cisco_ios_telnet'

    # Get configuration code from user input
    config_input = config_text.get("1.0", tk.END).strip()
    if not config_input:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Error: Please enter configuration code.")
        result_text.config(state=tk.DISABLED)
        return

    config_commands = config_input.splitlines()

    # Device connection information
    device = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'secret': enable_secret,
        'port': 22 if protocol == 'SSH' else 23,
    }

    try:
        # Connect to the device
        connection = ConnectHandler(**device)
        connection.enable()

        # Execute configuration
        output = connection.send_config_set(config_commands)

        # Display output
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Command Execution Result:\n")
        result_text.insert(tk.END, output)
        result_text.config(state=tk.DISABLED)

        # Save changes
        save_output = connection.send_command('write memory')
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, "\n\nSave Changes:\n")
        result_text.insert(tk.END, save_output)
        result_text.config(state=tk.DISABLED)

        # Disconnect
        connection.disconnect()

    except Exception as e:
        # Display errors
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")
        result_text.config(state=tk.DISABLED)

# Create window
window = tk.Tk()
window.title("Scorpion-Team - Cisco Device Configurator")
window.geometry("700x750")
window.configure(bg="#f0f0f0")

# Main title
title_label = tk.Label(window, text="Scorpion-Team: Cisco Configurator", font=("Arial", 18, "bold"), fg="#333", bg="#f0f0f0")
title_label.pack(pady=20)

# Connection information section
frame_connection = ttk.LabelFrame(window, text="Connection Information", padding=(10, 10))
frame_connection.pack(pady=15, padx=15, fill="x")

label_ip = tk.Label(frame_connection, text="IP Address:")
entry_ip = tk.Entry(frame_connection, width=30)

label_username = tk.Label(frame_connection, text="Username:")
entry_username = tk.Entry(frame_connection, width=30)

label_password = tk.Label(frame_connection, text="Password:")
entry_password = tk.Entry(frame_connection, show="*", width=30)

label_enable_secret = tk.Label(frame_connection, text="Enable Secret:")
entry_enable_secret = tk.Entry(frame_connection, show="*", width=30)

label_ip.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_ip.grid(row=0, column=1, padx=5, pady=5)

label_username.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_username.grid(row=1, column=1, padx=5, pady=5)

label_password.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_password.grid(row=2, column=1, padx=5, pady=5)

label_enable_secret.grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_enable_secret.grid(row=3, column=1, padx=5, pady=5)

# Protocol selection
frame_protocol = ttk.LabelFrame(window, text="Select Protocol", padding=(10, 10))
frame_protocol.pack(pady=15, padx=15, fill="x")

protocol_var = tk.StringVar(value="SSH")

radio_ssh = ttk.Radiobutton(frame_protocol, text="SSH", variable=protocol_var, value="SSH")
radio_telnet = ttk.Radiobutton(frame_protocol, text="Telnet", variable=protocol_var, value="Telnet")

radio_ssh.pack(side="left", padx=10, pady=5)
radio_telnet.pack(side="left", padx=10, pady=5)

# Configuration code section
frame_config = ttk.LabelFrame(window, text="Configuration Code", padding=(10, 10))
frame_config.pack(pady=15, padx=15, fill="both", expand=True)

config_text = tk.Text(frame_config, height=10, width=60)
config_text.pack(padx=5, pady=5, fill="both", expand=True)

# Execute button
button_execute = ttk.Button(window, text="Execute Configuration", command=execute_config)
button_execute.pack(pady=20)

# Output display section
frame_result = ttk.LabelFrame(window, text="Output", padding=(10, 10))
frame_result.pack(pady=15, padx=15, fill="both", expand=True)

result_text = tk.Text(frame_result, height=10, width=60, state=tk.DISABLED)
result_text.pack(padx=5, pady=5, fill="both", expand=True)

# Show window
window.mainloop()
