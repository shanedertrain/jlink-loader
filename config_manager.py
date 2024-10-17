from pathlib import Path
import json
from dataclasses import dataclass

CONFIG_FILEPATH = Path("config.json")


@dataclass
class Config:
    jlink_exe_path: Path
    firmware_path: Path


class ConfigManager:
    def __init__(self, config_file: Path = CONFIG_FILEPATH):
        self.config_file = config_file
        self.config_data: Config = Config(jlink_exe_path=Path(r"C:\Program Files\SEGGER\JLink\JLink.exe"), firmware_path=Path())
        if self.config_file.exists():
            self.config_data = self._load_config()

    def _load_config(self) -> Config:
        with self.config_file.open("r") as f:
            data = json.load(f)
            return Config(
                jlink_exe_path=Path(data.get("jlink_exe_path", "")),
                firmware_path=Path(data.get("firmware_path", ""))
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


if __name__ == "__main__":
    config_manager = ConfigManager()

    # Example usage:
    if not CONFIG_FILEPATH.exists():
        config_manager.save_config()

    # Accessing the configuration
    config = config_manager.get_config()
    print("JLink Path:", config.jlink_exe_path)
    print("Firmware Path:", config.firmware_path)
