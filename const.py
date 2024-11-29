"""Constants for the HWAM integration."""
from homeassistant.const import Platform

DOMAIN = "hwam"
PLATFORMS = [Platform.SENSOR]

# Default values
DEFAULT_NAME = "HWAM Poêle"
DEFAULT_SCAN_INTERVAL = 15

# Device info
DEVICE_INFO = {
    "identifiers": {("hwam", "stove")},
    "manufacturer": "HWAM",
    "model": "IHS Smart Control™",
    "sw_version": "3.20.0",
}

# Operation modes
OPERATION_MODES = {
    2: "Éteint",
    9: "En marche",
}

# Phase states
PHASE_STATES = {
    1: "Allumage",
    2: "Démarrage",
    3: "Combustion", 
    4: "Braises",
    5: "Veille"
}
