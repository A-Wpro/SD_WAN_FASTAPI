# SD_WAN_FASTAPI
#### API made on fastAPI (python) to start our API sharing our features form our SD wan project

WIP : 
remplir la GenerateOnosStruc

chercher d'autre features

## Pour commencer


Pre-requis

Ubuntu

docker


## Installation

docker : https://docs.docker.com/engine/install/ubuntu/

1. Clone le repo
   ```sh
   git clone https://github.com/A-Wpro/SD_WAN_FASTAPI.git
   ```
2.
   ```sh
   cd SD_WAN_FASTAPI
   ```

3.
   ```sh
   docker build -t sdwanapi .
   ```

4.
   ```sh
   docker run -d --name sdwanapicontainer -p 80:80 sdwanapi
   ```

5.  aller sur http://127.0.0.1:80/
 ou sur http://127.0.0.1:80/docs

#### Probléme récurrent
   Verifier que le port 80 soit libre, le docker pourrais ne  pas se lancer
   Pour verifier le lancement de l'API  : 
   ```
   docker logs sdwanapicontainer 
   ```
   si il y a un "FILE ERROR" ou similaire voici les commandes pour relancer le docker 
   ```
   docker kill $(docker ps -q)
   ```
   ```
   docker rm $(docker ps -a -q)
   ```
   puis retourner à l'étape 3 après corrections 
   
   lien vers la docu fastAPI docker
   https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

## Demarrage sur l'API

3 boutons : 

-Deploy ONOS (wip) : prochaine feature 

-Deploy RL : affiches le chemin le + cours ( et bientôt l'image du reseau) en 2 points choisit à l'avance : return JSON ou RAW

-DOCS : lien vers le docs fastAPI du projet

#### Pour le dévelopement 
Voici la ligne de commande qui permet de déveloper des features et d'auto reload pour ne pas avoir à relancer le contenaire à chaque changement des fichiers
```
docker run -d --name sdwanapicontainer -p 80:80 sdwanapi /start-reload.sh
```

### Versions
0.12

### Auteurs

A-Wpro, tompa97, Thomas92330


