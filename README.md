# Readme

## Beschreibung Big Data Use Case
Unser Big Data Use Case stellt über eine Flask Web-Anwendung verschiedene Information zur Kriminalität in Chicago (USA) dar.
<br/>Die Flask Anwendung greift für die benötigten Daten auf eine MySQL Datenbank zu. Des Weiteren werden die Daten durch Memcached für eine bestimmte Zeit im Cache gespeichert, um so eine bessere Performance zu ermöglichen. 

## Daten
Die originalen Daten zu diesem Projekt sind unter folgendem [Link](https://www.kaggle.com/currie32/crimes-in-chicago) zu finden.

## Erforderliche Software
1. spark v3.0.0
2. minikube v1.22.0 mit Kubernetes v1.21.2
3. kubectl v1.21.4
4. kafka v2.6
5. docker v20.10.8
6. mysql v1.22.1
7. flask v2.0.1

## Leitfaden
1. Terminal öffnen und 

minikube addons enable ingress (wenn es nicht funktioniert, minikube löschen und noch mal neu mit sudo minikube start --addons=ingress --driver=none --memory 4096 --cpus 2 installieren)

eval $(minikube docker-env)

skaffold dev

## Screencast
[Link]()

# Dokumentation

## Aufgabenstellung
Im Rahmen der Gruppenarbeit soll eine Anwendung erarbeitet werden, welche unter Berücksichtigung der in der Vorlesung vorgestellten Komponenten konzipiert und aufgebaut wird. Die Anwendungsidee und der Datensatz werden von der Gruppe selbst ausgewählt.

## Idee
Die Anwendungsidee besteht in der Verarbeitung und Visualisierung von polizeilich erfassten Verbrechen in Chicago (USA). Der Datensatz umfasst alle von dem Chicago Police Department erfassten Verbrechen im Zeitraum von 2001 bis 2017 und wurde dem System CLEAR (Citizen Law Enforcement Analysis and Reporting) entnommen. Für die Visualisierung werden ausgewählte Merkmale in Zusammenhang gebracht und graphisch in geeigneten Plots in einer Webanwendung dargestellt.

## Entwurf
Zu Beginn liegen die Rohdaten im Data Lake. Über ein Big Data Messaging Dienst werden diese Daten an eine Big Data Processing Applikation gestreamt. Diese Applikation stellt Berechnungen auf diesen Daten an und speichert diese in der Datenbank. Wenn Nutzer dann auf die Webapp zugreifen möchten, wird dieser zur Lastverteilung über einen Load Balancer geschickt. Danach überprüft die Webapp zuerst, ob es die benötigten Daten im Cache vorliegen hat. Ist dies nicht der Fall, greift die Webapp auf die Datenbank zu und lädt die Daten und speichert sie ebenfalls im Cache.
<br/>
<br/>
![alt text](/bigdata_platform.png)

## Architektur
### Webapp
Die Webapp ist eine Flask und stellt auf verschiedenen Seiten, erreichbar über die Menübar am oberen Bildschirmrand, Information in Form von Diagrammen dar. 
### Cache
Der Cache ist über Memcached realisiert und speichert die Daten nach dem ersten Zugriff für die nächsten 30 Sekunden. Nach dieser Zeit werden die Daten wieder neu geladen. 
Innerhalb der Webapp wird das Python-Modul pymemcache genutzt. Dort wird gecheckt, ob ein Wert im Cache vorhanden ist. Falls der Wert vorhanden ist, wird er sofort aus dem Cache gezogen, falls nicht, wird die Berechnungs-Funktion aufgerufen, der Wert berechnet und aufgerufen, und auserdem im Cache gespeichert.
### Datenbank
Die Datenbank ist realsiert mit einer MySQL Datenbank und läuft in einem eigenen Container und ist über den mysql-service und dem Port 3306 erreichbar. 
### Data Lake
Der Data Lake ist über ein HDFS realisiert. 
### Big Data Messaging
Text



