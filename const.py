"""Constants for the HWAM integration."""
from homeassistant.const import Platform

DOMAIN = "hwam"
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.FAN]

# Default values
DEFAULT_NAME = "HWAM Poêle"
DEFAULT_SCAN_INTERVAL = 15

# Config and attributes
CONF_DEVICE_ID = "device_id"
ATTR_START_TIME = "start_time"
ATTR_END_TIME = "end_time"
ATTR_ENABLED = "enabled"

# Device info
DEVICE_INFO = {
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

# Maintenance alarms
MAINTENANCE_ALARMS = {
    0: "Batterie faible poêle",
    1: "Défaut capteur O2",
    2: "Décalage capteur O2",
    3: "Défaut capteur température poêle",
    4: "Défaut capteur température pièce",
    5: "Défaut communication",
    6: "Batterie faible capteur température"
}

# Safety alarms
SAFETY_ALARMS = {
    0: "Défaut valve 1",
    1: "Défaut valve 2",
    2: "Défaut valve 3",
    3: "Mauvaise configuration",
    4: "Déconnexion valve 1",
    5: "Déconnexion valve 2",
    6: "Déconnexion valve 3",
    7: "Erreur calibration valve 1",
    8: "Erreur calibration valve 2",
    9: "Erreur calibration valve 3",
    10: "Surchauffe",
    11: "Porte ouverte trop longtemps",
    12: "Alarme manuelle",
    13: "Défaut capteur poêle"
}
