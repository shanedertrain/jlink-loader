from pathlib import Path
import json
from dataclasses import dataclass
from typing import Optional

DEFAULT_JLINK_EXE_PATH = Path(r"C:\Program Files\SEGGER\JLink\JLink.exe")
CONFIG_FILEPATH = Path("config.json")

@dataclass
class Config:
    jlink_exe_path: Optional[Path] = Path()
    firmware_path: Path = Path()

class ConfigManager:
    def __init__(self, config_file: Path = CONFIG_FILEPATH):
        self.config_file = config_file
        self.config_data: Config = Config()

        if self.config_file.exists():
            self.config_data = self._load_config()
        else:
            self.save_config()
            self.config_data = self._load_config()

    def _load_config(self) -> Config:
        with self.config_file.open("r") as f:
            data = json.load(f)

            jlink_exe_path = Path(data.get("jlink_exe_path", Path()))
            if jlink_exe_path == Path():
                jlink_exe_path = find_jlink_exe()

                if jlink_exe_path == Path():
                    raise ValueError("Could not find JLink EXE!")

            return Config(
                jlink_exe_path=jlink_exe_path,
                firmware_path=Path(data.get("firmware_path", Path()))
            )

    def save_config(self) -> None:
        data = {
            "jlink_exe_path": str(self.config_data.jlink_exe_path),
            "firmware_path": str(self.config_data.firmware_path)
        }
        with self.config_file.open("w") as f:
            json.dump(data, f, indent=4)

    def get_config(self) -> Config:
        return self.config_data

def find_jlink_exe() -> Optional[Path]:
    PROGRAM_FILES_DIRS = (Path(r'C:\Program Files\SEGGER'), Path(r'C:\Program Files (x86)\SEGGER'))

    for base_dir in PROGRAM_FILES_DIRS:
        if not base_dir.exists():
            continue
        for path in base_dir.rglob('JLink.exe'):
            return path
    return None

if __name__ == "__main__":
    config_manager = ConfigManager()

    # Accessing the configuration
    config = config_manager.get_config()
    print("JLink Path:", config.jlink_exe_path)
    print("Firmware Path:", config.firmware_path)
