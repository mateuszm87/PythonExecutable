import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import zipfile
from threading import Thread

class PyToExeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python to Executable Converter")
        self.file_path = ""
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Choose your .py file to make executable")
        self.label.pack(pady=10)

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.console_var = tk.IntVar()
        self.console_check = tk.Checkbutton(self.root, text="Use visible console?", variable=self.console_var)
        self.console_check.pack(pady=5)

        self.progress = tk.Label(self.root, text="")
        self.progress.pack(pady=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_step)
        self.next_button.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if self.file_path:
            self.progress.config(text=f"Selected: {self.file_path}")

    def next_step(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a .py file first")
            return

        self.root.withdraw()
        self.zip_window()

    def zip_window(self):
        zip_win = tk.Toplevel(self.root)
        zip_win.title("Zip Options")

        label = tk.Label(zip_win, text="Do you want to zip it?")
        label.pack(pady=10)

        yes_button = tk.Button(zip_win, text="Yes", command=lambda: self.create_exe(zip_win, zip_option="yes"))
        yes_button.pack(side=tk.LEFT, padx=10, pady=10)

        no_button = tk.Button(zip_win, text="No", command=lambda: self.create_exe(zip_win, zip_option="no"))
        no_button.pack(side=tk.LEFT, padx=10, pady=10)

        yes_pass_button = tk.Button(zip_win, text="Yes with password", command=lambda: self.create_exe(zip_win, zip_option="yes_pass"))
        yes_pass_button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_exe(self, zip_win, zip_option):
        zip_win.destroy()
        self.progress.config(text="Creating executable, please wait...")
        self.root.deiconify()

        def run_pyinstaller():
            console_flag = "" if self.console_var.get() else "--noconsole"
            subprocess.run(f"pyinstaller {console_flag} --onefile {self.file_path}", shell=True)
            exe_path = os.path.join("dist", os.path.basename(self.file_path).replace(".py", ".exe"))

            if zip_option == "yes":
                with zipfile.ZipFile(exe_path + ".zip", 'w') as zipf:
                    zipf.write(exe_path, os.path.basename(exe_path))
            elif zip_option == "yes_pass":
                password = "your_password"  # You can modify this to ask for a password
                with zipfile.ZipFile(exe_path + ".zip", 'w') as zipf:
                    zipf.setpassword(password.encode())
                    zipf.write(exe_path, os.path.basename(exe_path))

            self.final_window()

        Thread(target=run_pyinstaller).start()

    def final_window(self):
        final_win = tk.Toplevel(self.root)
        final_win.title("Operation Complete")

        label = tk.Label(final_win, text="Operation completed successfully!")
        label.pack(pady=10)

        close_button = tk.Button(final_win, text="Close", command=self.root.quit)
        close_button.pack(side=tk.LEFT, padx=10, pady=10)

        open_path_button = tk.Button(final_win, text="Open Path", command=lambda: os.startfile("dist"))
        open_path_button.pack(side=tk.LEFT, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PyToExeApp(root)
    root.mainloop()
