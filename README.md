# Intégration HWAM pour Home Assistant

Cette intégration personnalisée permet de contrôler et surveiller les poêles à bois HWAM équipés du système Smart Control™ depuis Home Assistant.

## Fonctionnalités

Cette intégration ajoute les fonctionnalités suivantes à Home Assistant :

- **Contrôle de puissance** : Contrôlez la puissance de combustion (niveaux 1-5) via une entité fan
- **Capteurs** :
  - Température du poêle
  - Température ambiante
  - Niveau d'oxygène
  - Position des valves
  - État du poêle (phases et modes)
  - Alarmes de maintenance et de sécurité
- **Mode nuit** : Configuration et contrôle du mode nuit
- **Alarmes** : Surveillance des alarmes de remplissage et de sécurité

## Installation

1. Copiez le dossier `hwam` dans le répertoire `custom_components` de votre installation Home Assistant
2. Redémarrez Home Assistant
3. Allez dans Paramètres > Appareils et Services > Ajouter une intégration
4. Recherchez "HWAM"
5. Suivez les instructions de configuration

## Configuration

L'intégration nécessite :
- L'adresse IP du poêle HWAM
- Un nom pour le poêle (optionnel)
- L'intervalle d'actualisation (par défaut : 15 secondes)

## Entités

### Fan
- `fan.hwam_burn_level`: Contrôle de la puissance de combustion (niveaux 1-5)

### Capteurs
- `sensor.hwam_stove_temperature`: Température du poêle (°C)
- `sensor.hwam_room_temperature`: Température ambiante (°C)
- `sensor.hwam_oxygen_level`: Niveau d'oxygène (%)
- `sensor.hwam_operation_mode`: Mode de fonctionnement
- `sensor.hwam_phase`: Phase actuelle
- `sensor.hwam_valve1_position`: Position valve 1 (%)
- `sensor.hwam_valve2_position`: Position valve 2 (%)
- `sensor.hwam_valve3_position`: Position valve 3 (%)
- `sensor.hwam_refill_alarm`: Alarme de remplissage
- `sensor.hwam_maintenance_alarms`: Alarmes maintenance
- `sensor.hwam_safety_alarms`: Alarmes sécurité

### Capteurs binaires
- `binary_sensor.hwam_door_open`: État de la porte
- `binary_sensor.hwam_night_mode`: État du mode nuit

## Services

### Mode nuit
- `hwam.set_night_mode_hours`: Configure les heures du mode nuit
  ```yaml
  service: hwam.set_night_mode_hours
  data:
    device_id: "votre_device_id"
    start_time: "23:00"
    end_time: "06:00"
  ```

- `hwam.enable_night_mode`: Active le mode nuit
  ```yaml
  service: hwam.enable_night_mode
  data:
    device_id: "votre_device_id"
  ```

- `hwam.disable_night_mode`: Désactive le mode nuit
  ```yaml
  service: hwam.disable_night_mode
  data:
    device_id: "votre_device_id"
  ```

## Cartes suggérées

### Carte de contrôle principal
```yaml
type: vertical-stack
cards:
  - type: entities
    title: "HWAM Poêle"
    entities:
      - entity: fan.hwam_burn_level
        name: "Puissance"
      - entity: sensor.hwam_stove_temperature
      - entity: sensor.hwam_room_temperature
      - entity: sensor.hwam_oxygen_level
      - entity: sensor.hwam_phase
      - entity: binary_sensor.hwam_night_mode
  
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.hwam_valve1_position
        name: "Valve 1"
        min: 0
        max: 100
      - type: gauge
        entity: sensor.hwam_valve2_position
        name: "Valve 2"
        min: 0
        max: 100
      - type: gauge
        entity: sensor.hwam_valve3_position
        name: "Valve 3"
        min: 0
        max: 100
```

## Dépannage

### Le poêle n'est pas détecté
- Vérifiez que le poêle est bien alimenté et connecté au réseau
- Vérifiez que l'adresse IP est correcte
- Vérifiez que le poêle est accessible depuis Home Assistant

### Erreurs de connexion
- Vérifiez la connectivité réseau
- Augmentez l'intervalle d'actualisation si nécessaire
- Vérifiez les logs de Home Assistant pour plus de détails

## Aide et Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs de Home Assistant
2. Ouvrez une issue sur GitHub avec :
   - La description du problème
   - Les logs pertinents
   - Votre configuration
   - Les étapes pour reproduire le problème

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
