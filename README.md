# Intégration HWAM pour Home Assistant

Cette intégration personnalisée permet de contrôler et surveiller les poêles à bois HWAM équipés du système Smart Control™ depuis Home Assistant.

## Fonctionnalités

Cette intégration ajoute les fonctionnalités suivantes à Home Assistant :

- **Contrôle de puissance** : Contrôlez la puissance de combustion (niveaux 0-5) via une liste déroulante
- **Démarrage** : Bouton de démarrage du poêle
- **Capteurs** :
  - Température du poêle
  - Température ambiante
  - Niveau d'oxygène
  - Position des valves
  - État du poêle (phases et modes)
  - Temps avant rechargement
  - Date de maintenance
  - Alarmes (maintenance, sécurité et remplissage)

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

### Bouton
- `button.hwam_start`: Démarrage du poêle

### Sélecteur
- `select.hwam_niveau_de_combustion`: Contrôle de la puissance (niveaux 0-5)

### Capteurs
- `sensor.hwam_temperature_du_poele`: Température du poêle (°C)
- `sensor.hwam_temperature_ambiante`: Température ambiante (°C)
- `sensor.hwam_niveau_d_oxygene`: Niveau d'oxygène (%)
- `sensor.hwam_mode_de_fonctionnement`: Mode de fonctionnement
- `sensor.hwam_phase`: Phase actuelle
- `sensor.hwam_valve1_position`: Position valve 1 (%)
- `sensor.hwam_valve2_position`: Position valve 2 (%)
- `sensor.hwam_valve3_position`: Position valve 3 (%)
- `sensor.hwam_time_to_refill`: Temps avant rechargement
- `sensor.hwam_refill_alarm`: Alarme de remplissage
- `sensor.hwam_maintenance_alarms`: Alarmes maintenance
- `sensor.hwam_safety_alarms`: Alarmes sécurité
- `sensor.hwam_service_date`: Date de maintenance

## Carte suggérée

```yaml
type: vertical-stack
cards:
  # En-tête avec état principal
  - type: custom:mushroom-title-card
    title: HWAM Poêle à bois
  
  - type: horizontal-stack
    cards:
      - type: custom:mushroom-template-card
        primary: "{{ states('sensor.hwam_phase') }}"
        secondary: Phase
        icon: mdi:fire
        icon_color: >-
          {% if states('sensor.hwam_phase') == 'Combustion' %}
            red
          {% elif states('sensor.hwam_phase') == 'Braises' %}
            orange
          {% elif states('sensor.hwam_phase') == 'Veille' %}
            gray
          {% else %}
            amber
          {% endif %}
      
      - type: custom:mushroom-button-card
        entity: button.hwam_start
        icon: mdi:power
        icon_color: >-
          {% if states('sensor.hwam_phase') != 'Veille' %}
            red
          {% else %}
            green
          {% endif %}

      - type: custom:mushroom-select-card
        entity: select.hwam_hwam_niveau_de_combustion
        icon: mdi:fire-circle
        icon_color: amber

  # Températures et oxygène
  - type: horizontal-stack
    cards:
      - type: custom:mushroom-template-card
        primary: "{{ states('sensor.hwam_temperature_du_poele') }}°C"
        secondary: Poêle
        icon: mdi:thermometer
        icon_color: red
        
      - type: custom:mushroom-template-card
        primary: "{{ states('sensor.hwam_temperature_ambiante') }}°C"
        secondary: Pièce
        icon: mdi:home-thermometer
        icon_color: blue
        
      - type: custom:mushroom-template-card
        primary: "{{ states('sensor.hwam_niveau_d_oxygene') }}%"
        secondary: O₂
        icon: mdi:gas-cylinder
        icon_color: cyan
        
  # Graphique
  - type: custom:plotly-graph
    entities:
      - entity: sensor.hwam_temperature_du_poele
      - entity: sensor.hwam_niveau_d_oxygene
      - entity: sensor.sonde_salon_temperature
    hours_to_show: 8
    refresh_interval: 10
    title: Températures et Oxygène
```

## Dépendance cartes personnalisées
Cette intégration nécessite les cartes personnalisées suivantes (HACS) :
- mushroom-cards
- plotly-graph-card

## Dépannage

### Le poêle n'est pas détecté
- Vérifiez que le poêle est bien alimenté et connecté au réseau
- Vérifiez que l'adresse IP est correcte
- Vérifiez que le poêle est accessible depuis Home Assistant

### Erreurs de connexion
- Vérifiez la connectivité réseau
- Augmentez l'intervalle d'actualisation si nécessaire
- Vérifiez les logs de Home Assistant pour plus de détails

## Licence

Ce projet est sous licence MIT.
