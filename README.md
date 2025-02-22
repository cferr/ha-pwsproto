# (Tentative d')Intégration Home Assistant du protocole PWS

# Description

Ce paquet Python contient une implémentation d'un serveur suivant le protocole
Personal Weather Station (PWS), dont une documentation peut être trouvée sur
[cette page](https://support.weather.com/s/article/PWS-Upload-Protocol?language=en_US).

Son développement est en cours. Il permet de:
* récupérer les données en provenance d'une station météo utilisant le protocole
PWS,
* envoyer ces données à Home Assistant via son API HTTP.

Ce module est appelé à devenir une intégration Home Assistant, ne nécessitant
plus le recours à l'API HTTP Home Assistant.

# Installation

Ce paquet s'installe à l'aide de `pip`:

```
pip install git+https://github.com/cferr/ha-pwsproto.git
```

# Utilisation

Deux modules sont disponibles à l'utilisation:
  * Le module de test `pwsproto.probe`,
  * Le module de mise à jour `pwsproto.server`.

## Module de test

Le module de test est utilisé pendant la phase de développement de ce paquet. Il
permet de vérifier si une station est correctement reconnue, et affiche les
valeurs relevées par celle-ci.

Ce module crée un serveur HTTP qui écoute sur le port donné (par défaut 80).

L'exécution du module de test se fait comme suit:

```
python -m pwsproto.probe [--pws-listen LISTEN_IP] [--pws-port LISTEN_PORT]
```

Les paramètres `--pws-listen` et `--pws-port` sont optionnels; par défaut, le
serveur écoute à l'adresse `127.0.0.1` sur le port `8080`.



Exemple:

```
> python -m pwsproto.probe --pws-listen 127.0.0.1 --pws-port 8080
Bottle v0.13.2 server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:8080/
Hit Ctrl-C to quit.

INFO:root:[22296]: *** Begin Station Update ***
INFO:root:[22296]: Station ID = TEST, Station Key = KEY
INFO:root:[22296]: Recognized sensors:
INFO:root:[22296]:   Sensor name = date; Value = 2025-02-15 17:30:20; Unit = None
INFO:root:[22296]:   Sensor name = wind_direction; Value = 230; Unit = wind_direction
INFO:root:[22296]:   Sensor name = wind_speed; Value = 12.0; Unit = mph
INFO:root:[22296]:   Sensor name = wind_gust_speed; Value = 12.0; Unit = mph
INFO:root:[22296]:   Sensor name = outdoor_temperature; Value = 70.0; Unit = °F
INFO:root:[22296]:   Sensor name = rain_hourly; Value = 0.0; Unit = in
INFO:root:[22296]:   Sensor name = barometric_pressure; Value = 29.1; Unit = inHg
INFO:root:[22296]:   Sensor name = dew_temperature; Value = 68.2; Unit = °F
INFO:root:[22296]:   Sensor name = outdoor_humidity; Value = 40.0; Unit = %
INFO:root:[22296]:   Sensor name = weather_text; Value = Sonnig; Unit = None
INFO:root:[22296]:   Sensor name = clouds; Value = ; Unit = None
INFO:root:[22296]:   Sensor name = software_type; Value = vws versionxx; Unit = None
INFO:root:[22296]: Unrecognized parameters:
INFO:root:[22296]:   action=updateraw
INFO:root:[22296]: *** End Station Update ***
```

## Module de mise à jour

Ce module écoute les requêtes provenant d'une station météo, et communique à
Home Assistant les valeurs relevées. Il nécessite pour cela un jeton donné par
Home Assistant, qui doit se trouver dans la variable d'environnement `LLT`.

L'exécution du module de mise à jour se fait comme suit:

```
python -m pwsproto.server --ha-host [HA_HOST] --pws-listen [LISTEN_IP] --pws-port [LISTEN_PORT] --pws-station-id [STATION_ID] --pws-station-password [STATION_KEY]
```

Le paramètre `HA_HOST` correspond au nom d'hôte ou à l'adresse IP sur laquelle
se trouve le serveur Home Assistant; `LISTEN_IP` correspond à l'adresse IP sur
laquelle ce module doit écouter, et `LISTEN_PORT` le port TCP sur lequel ce
module doit écouter.

Exemple:
```
> python -m pwsproto.server --ha-host 127.0.0.1 --pws-listen 127.0.0.1 --pws-port 8080 --pws-station-id TEST --pws-station-password KEY
Bottle v0.13.2 server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:8080/
Hit Ctrl-C to quit.

WARNING:root:Unknown parameter: action=updateraw
127.0.0.1 - - [22/Feb/2025 16:10:49] "GET /weatherstation/updateweatherstation.php?ID=TEST&PASSWORD=KEY&dateutc=2025-02-15+17%3A30%3A20&winddir=230&windspeedmph=12&windgustmph=12&tempf=70&rainin=0&baromin=29.1&dewptf=68.2&humidity=40&weather=Sonnig&clouds=&softwaretype=vws%20versionxx&action=updateraw HTTP/1.1" 200 0
```

## Configuration

### Port d'écoute

Le port par défaut utilisé par ce module est 8080.

Les stations météo utilisent les ports 80 (pour le protocole HTTP) et 443 (pour
le protocole HTTPS). Ces ports privilégiés nécessitent une configuration
spéciale pour être utilisés. Vous pouvez:
* Utiliser un proxy inversé (voir cette section),
* Utiliser une redirection de port, si le serveur est derrière un routeur; le
port 80 doit être renvoyé vers le port sur lequel écoute le serveur, par exemple
8080.
* Utiliser le port 80 directement, avec l'option `--pws-port 80`. Il peut être
nécessaire d'utiliser un compte administrateur ou super-utilisateur:
```
sudo python -m pwsproto.server --pws-port 80 [OPTIONS]
```
Il n'est pas recommandé d'exécuter ce module en tant que super-utilisateur.


### Jeton Home Assistant

Ce jeton permet d'utiliser l'API HTTP de Home Assistant. Il s'agit pour
l'instant de la seule manière de communiquer avec Home Assistant dont dispose ce
module.

Il doit se trouver dans la variable d'environnement `LLT`.

[Cette page](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token)
explique comment créer ce jeton.

L'erreur suivante apparaîtra si le jeton n'existe pas:
```
ERROR:root:Set the LLT environment variable
```

### Proxy inversé

Si votre serveur est exposé à Internet, il est recommandé d'utiliser ce module
derrière un proxy inversé, qui permet d'utiliser le protocole chiffré HTTPS.

[Documentation à compléter]
