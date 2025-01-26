import tkinter as tk
from netmiko import ConnectHandler

def execute_config_telnet():
    # گرفتن اطلاعات از ورودی کاربر
    ip = entry_ip.get()
    username = entry_username.get()
    password = entry_password.get()
    enable_secret = entry_enable_secret.get()

    # گرفتن کد کانفیگ از ورودی کاربر
    config_input = config_text.get("1.0", tk.END)
    config_commands = config_input.splitlines()

    # اطلاعات اتصال به دستگاه سیسکو
    device = {
        'device_type': 'cisco_ios_telnet',  # استفاده از Telnet
        'ip': ip,
        'username': username,
        'password': password,
        'secret': enable_secret,
        'port': 23,  # پورت تلنت
    }

    # اتصال به دستگاه
    connection = ConnectHandler(**device)
    connection.enable()

    # اجرای تغییرات
    output = connection.send_config_set(config_commands)

    # نمایش خروجی
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)
    result_text.config(state=tk.DISABLED)

    # ذخیره تغییرات
    connection.send_command('write memory')

    # قطع اتصال
    connection.disconnect()

# ایجاد پنجره
window = tk.Tk()
window.title("تنظیمات دستگاه سیسکو با Telnet")

# ایجاد ویدجت‌ها
label_ip = tk.Label(window, text="آدرس IP:")
entry_ip = tk.Entry(window)

label_username = tk.Label(window, text="نام کاربری:")
entry_username = tk.Entry(window)

label_password = tk.Label(window, text="رمز عبور:")
entry_password = tk.Entry(window, show="*")

label_enable_secret = tk.Label(window, text="رمز عبور مدیر:")
entry_enable_secret = tk.Entry(window, show="*")

label_config = tk.Label(window, text="کد کانفیگ:")
config_text = tk.Text(window, height=10, width=50)

button_execute = tk.Button(window, text="اجرای تنظیمات", command=execute_config_telnet)

result_text = tk.Text(window, height=10, width=50, state=tk.DISABLED)

# پوزیشن دادن ویدجت‌ها در پنجره
label_ip.grid(row=0, column=0)
entry_ip.grid(row=0, column=1)

label_username.grid(row=1, column=0)
entry_username.grid(row=1, column=1)

label_password.grid(row=2, column=0)
entry_password.grid(row=2, column=1)

label_enable_secret.grid(row=3, column=0)
entry_enable_secret.grid(row=3, column=1)

label_config.grid(row=4, column=0)
config_text.grid(row=4, column=1)

button_execute.grid(row=5, column=0, columnspan=2)

result_text.grid(row=6, column=0, columnspan=2)

# نمایش پنجره
window.mainloop()
