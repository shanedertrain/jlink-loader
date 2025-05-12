from typing import Final
from dataclasses import dataclass
import typing as t

XMC_FLASH_UNCACHED_BASE: Final[int] = 0x08000000


@dataclass
class XMCFlashSectorData:
    name: str
    start_address: int
    length: int
    end_address: t.Optional[int] = None

    def __post_init__(self):
        self.end_address = self.start_address + self.length

class XMCFlashSectors:
    SECTOR_0            = XMCFlashSectorData(name="SECTOR_0", start_address=XMC_FLASH_UNCACHED_BASE + 0x00000, length=0x04000)
    SECTOR_1            = XMCFlashSectorData(name="SECTOR_1", start_address=XMC_FLASH_UNCACHED_BASE + 0x04000, length=0x04000)
    SECTOR_2            = XMCFlashSectorData(name="SECTOR_2", start_address=XMC_FLASH_UNCACHED_BASE + 0x08000, length=0x04000)
    SECTOR_3            = XMCFlashSectorData(name="SECTOR_3", start_address=XMC_FLASH_UNCACHED_BASE + 0x0C000, length=0x04000)
    SECTOR_4            = XMCFlashSectorData(name="SECTOR_4", start_address=XMC_FLASH_UNCACHED_BASE + 0x10000, length=0x04000)
    SECTOR_5            = XMCFlashSectorData(name="SECTOR_5", start_address=XMC_FLASH_UNCACHED_BASE + 0x14000, length=0x04000)
    SECTOR_6            = XMCFlashSectorData(name="SECTOR_6", start_address=XMC_FLASH_UNCACHED_BASE + 0x18000, length=0x04000)
    SECTOR_7            = XMCFlashSectorData(name="SECTOR_7", start_address=XMC_FLASH_UNCACHED_BASE + 0x1C000, length=0x04000)
    SECTOR_8            = XMCFlashSectorData(name="SECTOR_8", start_address=XMC_FLASH_UNCACHED_BASE + 0x20000, length=0x04000)
    SECTOR_9            = XMCFlashSectorData(name="SECTOR_9", start_address=XMC_FLASH_UNCACHED_BASE + 0x40000, length=0x04000)
    SECTOR_10           = XMCFlashSectorData(name="SECTOR_10", start_address=XMC_FLASH_UNCACHED_BASE + 0x80000, length=0x04000)
    SECTOR_11           = XMCFlashSectorData(name="SECTOR_11", start_address=XMC_FLASH_UNCACHED_BASE + 0xC0000, length=0x04000)
    SECTOR_12           = XMCFlashSectorData(name="SECTOR_12", start_address=XMC_FLASH_UNCACHED_BASE + 0x100000, length=0x04000)
    SECTOR_13           = XMCFlashSectorData(name="SECTOR_13", start_address=XMC_FLASH_UNCACHED_BASE + 0x140000, length=0x04000)
    SECTOR_14           = XMCFlashSectorData(name="SECTOR_14", start_address=XMC_FLASH_UNCACHED_BASE + 0x180000, length=0x04000)
    SECTOR_15           = XMCFlashSectorData(name="SECTOR_15", start_address=XMC_FLASH_UNCACHED_BASE + 0x1C0000, length=0x04000)
    PSRAM1              = XMCFlashSectorData(name="PSRAM1", start_address=0x1FFE8000, length=0x18000)
    DSRAM_1_SYSTEM      = XMCFlashSectorData(name="DSRAM_1_SYSTEM", start_address=0x20000000, length=0x20000)
    DSRAM_2_COMM        = XMCFlashSectorData(name="DSRAM_2_COMM", start_address=0x20020000, length=0x20000)
    EXTERNAL_SRAM       = XMCFlashSectorData(name="EXTERNAL_SRAM", start_address=0x64000000, length=0x200000)
# Usage example
if __name__ == "__main__":
    # Example: accessing the address of SECTOR_5
    sector = XMCFlashSectors.SECTOR_0
    print(f"Address of {sector.name}: {hex(sector.start_address)}")