import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from pathlib import Path
import traceback

from config_manager import ConfigManager

class JLinkLoaderApp:
    config_manager = ConfigManager()
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("J-Link Firmware Loader")

        self.config = self.config_manager.get_config()

        row_index = 0

        self.label_jlink = tk.Label(root, text="JLink.exe Path:")
        self.label_jlink.grid(row=row_index, column=0, padx=10, pady=10)

        self.entry_jlink = tk.Entry(root, width=50)
        self.entry_jlink.grid(row=row_index, column=1, padx=10, pady=10)
        self.entry_jlink.insert(0, self.config.jlink_exe_path)

        self.button_browse_firmware = tk.Button(root, text="Browse", command=lambda: self.browse_files([("EXE files", "*.exe")]))
        self.button_browse_firmware.grid(row=0, column=2, padx=10, pady=10)

        row_index += 1

        self.label_firmware = tk.Label(root, text="Firmware File:")
        self.label_firmware.grid(row=row_index, column=0, padx=10, pady=10)

        self.entry_firmware = tk.Entry(root, width=50)
        self.entry_firmware.grid(row=row_index, column=1, padx=10, pady=10)
        self.entry_firmware.insert(0, self.config.firmware_path)

        self.button_browse_firmware = tk.Button(root, text="Browse", command=lambda: self.browse_files([("HEX files", "*.hex")]))
        self.button_browse_firmware.grid(row=row_index, column=2, padx=10, pady=10)

        row_index += 1

        self.button_load = tk.Button(root, text="Load Firmware", command=self.load_firmware)
        self.button_load.grid(row=row_index, column=1, padx=10, pady=10)

        row_index += 1

    def browse_files(self, filetypes:list[tuple[str, str]]):
        base_types = [("All files", "*.*")]
        filetypes.append(base_types)

        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.entry_firmware.delete(0, tk.END)
            self.entry_firmware.insert(0, filename)

    def load_firmware(self):
        firmware_path = Path(self.entry_firmware.get())

        self.save_config()

        if not firmware_path.is_file():
            messagebox.showerror("Error", "Please select a valid firmware file.")
            return
        
        try:
            if self.run_jlink(firmware_path):
                messagebox.showinfo("Success", "Firmware loaded successfully.")

            traceback.print_exc()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to load firmware: {e.stderr}")
            traceback.print_exc()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()

    def run_jlink(self, firmware_path: Path) -> bool:
        jlink_path_str = self.entry_jlink.get()

        if not Path(jlink_path_str).is_file():
            messagebox.showerror("Error", "Please select a valid exe file.")
            return False

        device = "XMC4700-2048"
        speed = 4000

        jlink_commands = f"""
        device {device}
        speed {speed}
        if SWD
        loadfile "{firmware_path}"
        r
        g
        exit
        """

        with open("jlink_script.jlink", "w") as script_file:
            script_file.write(jlink_commands)

        result = subprocess.run([jlink_path_str, "-CommanderScript", "jlink_script.jlink"], capture_output=True, text=True, check=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)

        return True

    def save_config(self):
        self.config.firmware_path = Path(self.entry_firmware.get())
        self.config.jlink_exe_path = Path(self.entry_jlink.get())
        self.config_manager.save_config()

if __name__ == "__main__":
    root = tk.Tk()
    app = JLinkLoaderApp(root)
    root.mainloop()
