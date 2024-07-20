import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import pylink

class JLinkLoaderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("J-Link Firmware Loader")

        self.label_firmware = tk.Label(root, text="Firmware File:")
        self.label_firmware.grid(row=0, column=0, padx=10, pady=10)

        self.entry_firmware = tk.Entry(root, width=50)
        self.entry_firmware.grid(row=0, column=1, padx=10, pady=10)

        self.button_browse = tk.Button(root, text="Browse", command=self.browse_file)
        self.button_browse.grid(row=0, column=2, padx=10, pady=10)

        self.button_load = tk.Button(root, text="Load Firmware", command=self.load_firmware)
        self.button_load.grid(row=1, column=1, padx=10, pady=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("HEX files", "*.hex"), ("All files", "*.*")])
        if filename:
            self.entry_firmware.delete(0, tk.END)
            self.entry_firmware.insert(0, filename)

    def load_firmware(self):
        firmware_path = Path(self.entry_firmware.get())
        if not firmware_path.is_file():
            messagebox.showerror("Error", "Please select a valid firmware file.")
            return

        try:
            self.run_jlink(firmware_path)
            messagebox.showinfo("Success", "Firmware loaded successfully.")
        except pylink.errors.JLinkException as e:
            messagebox.showerror("Error", f"Failed to load firmware: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def run_jlink(self, firmware_path: Path):
        device = "XMC4700-2048"
        speed = 4000

        jlink = pylink.JLink()
        jlink.open()
        jlink.connect(device, iface=pylink.enums.JLinkInterfaces.SWD, speed=speed)

        try:
            jlink.flash_file(str(firmware_path), 0x00000000)
            jlink.reset()
            jlink.go()
        finally:
            jlink.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = JLinkLoaderApp(root)
    root.mainloop()
