#!/usr/bin/env bash
# Docker for holbi hackaton
echo '********************************************************************************'
echo '* Script for creating the volume and manage the holbi hack container container *'
echo '********************************************************************************'
options=("Create volume"
	"Download container"
	"Run container"
	"List containers"
	"Connect to the container"
	"Stop container"
	"Exit")
select opt in "${options[@]}"
do                                                                                                                                                                       case $opt in                                                                                                                                                         	"Create volume")
echo 'creating docker volume'
docker volume create holbihack
echo 'volume created'
break
;;

"Download container")
echo "Downloading container"
docker pull fermec28/flask-mysql-ready
echo "Container downloaded"
break
;;

"Run container")
echo "starting container"
sudo docker run -p 5000:5000 -p 5001:5001 -d -it -v holbihack:/root/holbihack fermec28/flask-mysql-ready
echo "Container running"
break
;;

"List containers")
echo "active containers"
docker ps
break
;;

"Connect to the container")
echo "connecting to container"
docker exec -it $(docker ps | tail -1 | rev | cut -d " " -f 1 | rev) /bin/bash
echo "detached from container"
break
;;

"Stop container")
echo "Stopping container"
docker stop $(docker ps | tail -1 | rev | cut -d " " -f 1 | rev)
echo "Container stopped"
break
;;

"Exit")
    break
    ;;
*) echo invalid option;;
    esac
done

