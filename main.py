import os
import time 
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import subprocess
from pathlib import Path
import traceback
from dataclasses import dataclass
import typing as t

from config_manager import ConfigManager
from main_version import VERSION
from konami_code import KonamiCodeDetector
from xmc_flash import XMCFlashSectors

JLINK_SCRIPT_FILEPATH = Path("jlink_script.jlink")

@dataclass
class ProcessorParams:
    name:str
    flash_memory_total_bytes:int
    flash_start_addr:int #hex()
    speed:int #kHz

XMC4700_2048 = ProcessorParams(
    name="XMC4700-2048",
    flash_memory_total_bytes=0x200000,
    flash_start_addr=0x08000000,
    speed=4000
)

class JLinkHandler:
    def __init__(self, jlink_path:Path, pparams:ProcessorParams):
        self.jlink_path = jlink_path
        self.pparams = pparams

    def load_firmware(self, firmware_filepath:Path, start_address:int=None):
        if firmware_filepath.suffix in [".hex"]:
            load_command = f'loadfile "{firmware_filepath}" {hex(start_address) if start_address else ""}'
        elif firmware_filepath.suffix in [".bin"]:
            load_command = f'loadbin "{firmware_filepath}", {hex(start_address) if start_address else ""}'

        print(f"Loading at {hex(start_address) if start_address else ''} : {firmware_filepath}")

        self.write_jlink_script(JLINK_SCRIPT_FILEPATH, [load_command])
        self.run_jlink_script(JLINK_SCRIPT_FILEPATH)

    def extract_firmware(self, save_path:Path):
        save_command = f'savebin "{save_path}", {hex(self.pparams.flash_start_addr)}, {hex(self.pparams.flash_memory_total_bytes)}'
        self.write_jlink_script(JLINK_SCRIPT_FILEPATH, commands=[save_command])
        self.run_jlink_script(JLINK_SCRIPT_FILEPATH)
    
    def erase_firmware(self):
        self.write_jlink_script(JLINK_SCRIPT_FILEPATH, ['erase'])
        self.run_jlink_script(JLINK_SCRIPT_FILEPATH)
    
    def write_jlink_script(self, out_path:Path, commands:list[str]) -> str:
        jlink_commands = (
        f"device {self.pparams.name}\n"
        f"speed {self.pparams.speed}\n"
        "if SWD\n"
        + "\n".join(commands) + "\n"
        "r\n"
        "g\n"
        "exit\n"
        )

        with open(out_path, "w") as script_file:
            script_file.write(jlink_commands)

    def run_jlink_script(self, jlink_script_path:Path):
        result = subprocess.run([str(self.jlink_path), "-CommanderScript", jlink_script_path], check=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)

class JLinkLoaderApp:
    config_manager = ConfigManager()
    jlink_handler:t.Optional[JLinkHandler] = None

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"J-Link Firmware Loading Utility | Version {VERSION[0]}.{VERSION[1]}.{VERSION[2]}")

        self.config = self.config_manager.get_config()

        row_index = 0

        root.columnconfigure(1, weight=1)

        # JLINK PATH FRAME
        self.jlink_path_frame = ttk.LabelFrame(root, text="JLink.exe Path")
        self.jlink_path_frame.grid(row=row_index, column=0, padx=10, pady=10, sticky='ew')

        self.entry_jlink = tk.Entry(self.jlink_path_frame, width=90)
        self.entry_jlink.grid(row=row_index, column=0, padx=10, pady=10)
        self.entry_jlink.insert(0, self.config.jlink_exe_path)

        self.button_browse_firmware = tk.Button(self.jlink_path_frame, text="Browse", command=lambda: self.browse_files(self.entry_jlink, [("EXE files", "*.exe")]))
        self.button_browse_firmware.grid(row=0, column=1, padx=10, pady=10)

        row_index += 1

        # FIRMWARE PATH FRAME
        self.firmware_path_frame = ttk.LabelFrame(root, text="Firmware Path")
        self.firmware_path_frame.grid(row=row_index, column=0, padx=10, pady=10, sticky='ew')

        self.entry_firmware = tk.Entry(self.firmware_path_frame, width=100)
        self.entry_firmware.grid(row=row_index, column=0, padx=10, pady=10, sticky='ew')
        self.entry_firmware.insert(0, self.config.firmware_path)

        row_index += 1

        # BUTTONS FRAME
        buttons_frame = ttk.LabelFrame(root)
        buttons_frame.grid(row=row_index, column=0, padx=10, pady=10, sticky='ew')
        buttons_frame_row_index = 0

        for i in range(3):
            buttons_frame.grid_columnconfigure(i, weight=1)

        self.load_bootloader_button = tk.Button(buttons_frame, text="Load Bootloader", command=self.on_load_bootloader_btn_clicked)
        self.load_bootloader_button.grid(row=buttons_frame_row_index, column=0, padx=10, pady=10, sticky='ew')
        self.load_bootloader_button.grid_remove()  # Initially hidden

        self.button_load = tk.Button(buttons_frame, text="Load Firmware", command=self.load_firmware)
        self.button_load.grid(row=buttons_frame_row_index, column=0, padx=10, pady=10, sticky='ew', columnspan=3)

        self.clear_firmware_button = tk.Button(buttons_frame, text="Clear Firmware", command=self.on_clear_firmware_btn_clicked)
        self.clear_firmware_button.grid(row=buttons_frame_row_index, column=2, padx=10, pady=10, sticky='ew')
        self.clear_firmware_button.grid_remove()  # Initially hidden

        buttons_frame_row_index += 1

        self.load_bootloaded_app_button = tk.Button(buttons_frame, text="Load Flashloaded App", command=self.on_load_flashloaded_app_btn_clicked)
        self.load_bootloaded_app_button.grid(row=buttons_frame_row_index, column=0, padx=10, pady=10, sticky='ew')
        self.load_bootloaded_app_button.grid_remove()  # Initially hidden

        self.extract_firmware_button = tk.Button(buttons_frame, text="Extract Firmware", command=self.on_extract_firmware_btn_clicked)
        self.extract_firmware_button.grid(row=buttons_frame_row_index, column=1, padx=10, pady=10, sticky='ew')
        self.extract_firmware_button.grid_remove()  # Initially hidden

        row_index += 1

        # Initialize KonamiCodeDetector with a callback to show the hidden button
        self.konami_detector = KonamiCodeDetector(self.root, self.show_hidden_buttons)
        
    def show_hidden_buttons(self):
        self.button_load.grid(row=0, column=1, padx=10, pady=10, sticky='ew', columnspan=1)
        self.extract_firmware_button.grid()
        self.clear_firmware_button.grid()
        self.load_bootloader_button.grid()
        self.load_bootloaded_app_button.grid()

    def on_extract_firmware_btn_clicked(self):
        self.jlink_handler = JLinkHandler(Path(self.entry_jlink.get()), pparams=XMC4700_2048)

        save_path = Path(filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin")]))

        self.jlink_handler.extract_firmware(save_path)
        
        os.startfile(save_path.parent)

    def on_clear_firmware_btn_clicked(self):
        self.jlink_handler = JLinkHandler(Path(self.entry_jlink.get()), pparams=XMC4700_2048)

        if messagebox.askyesno("Confirmation", "Are you sure you want to clear the processor memory?"):
            self.jlink_handler.erase_firmware()

    def on_load_bootloader_btn_clicked(self):
        BOOTLOADER_PARTITION_START = XMCFlashSectors.PSRAM1.start_address
        self.jlink_handler = JLinkHandler(Path(self.entry_jlink.get()), pparams=XMC4700_2048)
        
        bootloader_filepath = Path(filedialog.askopenfilename(filetypes=[("Hex files", "*.hex")], initialdir=Path(self.entry_firmware.get()).parent,
                                                        title="Select Bootloader"))
        
        self.jlink_handler.load_firmware(bootloader_filepath, BOOTLOADER_PARTITION_START)

    def on_load_flashloaded_app_btn_clicked(self):
        FLASHLOADER_PARITION_START  = XMCFlashSectors.SECTOR_0.start_address
        FLASHLOADER_PARTITION_SIZE  = XMCFlashSectors.SECTOR_8.start_address - FLASHLOADER_PARITION_START
        APP_PARITION_START = FLASHLOADER_PARITION_START + FLASHLOADER_PARTITION_SIZE

        self.jlink_handler = JLinkHandler(Path(self.entry_jlink.get()), pparams=XMC4700_2048)
        
        flashloader_filepath = Path(filedialog.askopenfilename(filetypes=[("Hex files", "*.hex")], initialdir=Path(self.entry_firmware.get()).parent,
                                                        title="Select Flashloader"))
        app_filepath = Path(filedialog.askopenfilename(filetypes=[("Hex files", "*.hex")], initialdir=Path(self.entry_firmware.get()).parent,
                                                title="Select Application"))
        
        self.jlink_handler.load_firmware(flashloader_filepath, FLASHLOADER_PARITION_START)
        self.jlink_handler.load_firmware(app_filepath, APP_PARITION_START)

    def browse_files(self, entry: tk.Entry, filetypes: list[tuple[str, str]], initialdir:Path=None):
        base_types = [("All files", "*.*")]
        filetypes = filetypes + base_types  # Concatenate the base types with the provided filetypes

        try:
            filepath = filedialog.askopenfilename(filetypes=filetypes, initialdir=initialdir)
        except Exception as e:
            filepath = filedialog.askopenfilename(filetypes=filetypes)

        if filepath:
            entry.delete(0, tk.END)
            entry.insert(0, filepath)

    def load_firmware(self):
        jlink_filepath = Path(self.entry_jlink.get())

        firmware_filepath = Path(filedialog.askopenfilename(filetypes=[("Hex files", "*.hex")], initialdir=Path(self.entry_firmware.get()).parent,
                                                title="Select Application"))

        self.save_config()

        if not firmware_filepath.is_file():
            messagebox.showerror("Error", "Please select a valid firmware file.")
            return
        elif not jlink_filepath.is_file() or jlink_filepath.suffix != ".exe" :
            messagebox.showerror("Error", "Please select a valid exe file.")
            return False
        
        self.entry_firmware.delete(0, tk.END)
        self.entry_firmware.insert(0, firmware_filepath)
        
        try:
            self.jlink_handler = JLinkHandler(jlink_filepath, pparams=XMC4700_2048)
            
            self.jlink_handler.load_firmware(firmware_filepath)
            messagebox.showinfo("Success", "Firmware loaded successfully!")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to load firmware: {e.stderr}")
            traceback.print_exc()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            traceback.print_exc()

    def save_config(self):
        self.config.firmware_path = Path(self.entry_firmware.get())
        self.config.jlink_exe_path = Path(self.entry_jlink.get())
        self.config_manager.save_config()

if __name__ == "__main__":
    root = tk.Tk()
    app = JLinkLoaderApp(root)
    root.mainloop()
