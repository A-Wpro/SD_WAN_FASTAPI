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

docker : https://docs.docker.com/docker-for-windows/install/

1. Clone le repo
   ```sh
   git clone https://github.com/A-Wpro/SD_WAN_FASTAPI.git
   ```
2.
   ```sh
   cd SD_WAN_FASTAP
   ```

3.
   ```sh
   docker build -t sdwanapi .
   ```

4.
   ```sh
   docker run -d --name sdwanapicontainer -p 80:80 sdwanapi
   ```

5.  aller sur http://127.0.0.1:8000/
 ou sur http://127.0.0.1:8000/docs


## Demarrage sur l'API

But : Mettre a disposition de une ou plusieurs features du projet SD WAN

sur le "/" on peux trouver les differentes features et leurs docus


### Versions
0.04

### Auteurs

A-Wpro, tompa97, thomas tranchet

