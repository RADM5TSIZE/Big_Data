# Big_Data

# Beschreibung Big Data Use Case
Unser Big Data Use Case stellt über eine Flask Web Anwendung, verschiedene Information zu Kriminalität in Chicago dar. Die Flask Anwendung greift für die benötigten Daten auf eine MySQL Datenbank zu. Des Weiteren werden die Daten durch Memcached für eine bestimmte Zeit im Cache gespeichert, um so eine bessere Performance zu ermöglichen. 

# Architektur
![alt text](./bigdata_platform.png)

# Komponenten
### Webapp
Die Webapp ist eine Flask und stellt auf verschiedenen Seiten, erreichbar über die Menübar am oberen Bildschirmrand, Information in Form von Diagrammen dar. 
### Cache
Der Cache ist über Memcached realisiert und speichert die Daten nach dem ersten Zugriff für die nächsten 30 Sekunden. Nach dieser Zeit werden die Daten wieder neu geladen. 
### Datenbank
Die Datenbank ist realsiert mit einer MySQL Datenbank und läuft in einem eigenen Container und ist über den mysql-service und dem Port 3306 erreichbar. 
### Data Lake
Der Data Lake ist über ein HDFS realisiert. 
### Big Data Messaging
- [ ] Infos Miguel

# Daten
Die originalen Daten zu diesem Projekt sind unter folgendem [Link](https://www.kaggle.com/currie32/crimes-in-chicago) zu finden.

# Installation
- [ ] Miguel - Installation Steps/ Startup procedure

