# Dokumentation
Vorliegende Doku dient bla bla

## Aufgabenstellung
Micha

## Idee
Micha

## Architektur
![alt text](/bigdata_platform.png)
<br/>Bild einmal beschreiben (allgemein)

## Komponenten
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

## Funktion
wie spielt das zusammen...wer gibt was an wen weiter etc