CREATE TABLE IF NOT EXISTS Chicago_Crimes_sample (
    `ID` INT,
    `CaseNumber` VARCHAR(8),
    `Date` DATETIME,
    `Block` VARCHAR(22),
    `IUCR` VARCHAR(10),
    `PrimaryType` VARCHAR(26),
    `Description` VARCHAR(32),
    `LocationDescription` VARCHAR(18),
    `Arrest` VARCHAR(5),
    `Domestic` VARCHAR(5),
    `Beat` INT,
    `District` NUMERIC(3, 1),
    `Ward` NUMERIC(3, 1),
    `CommunityArea` NUMERIC(3, 1),
    `FBICode` VARCHAR(3),
    `XCoordinate` INT,
    `YCoordinate` INT,
    `Year` INT,
    `UpdatedOn` DATETIME,
    `Latitude` INT,
    `Longitude` INT,
    `Location` VARCHAR(50)
);
 
INSERT INTO Chicago_Crimes_sample (ID, CaseNumber, Date, Block, IUCR, PrimaryType, Description, LocationDescription, Arrest, Domestic, Beat, District, Ward, CommunityArea, FBICode, XCoordinate, YCoordinate, Year, UpdatedOn, Latitude, Longitude, Location)
 
VALUES (10817834,  'JA117989' ,  '01/16/2017 02:45:00 PM' ,  '033XX W OGDEN AVE' ,  '0880' ,  'THEFT' ,  'PURSE-SNATCHING' ,  'SIDEWALK' ,  'False' ,  'False' , 1021,  '10.0' , '24.0',  '29.0' ,  '06' , NULL, NULL, 2017,  '01/23/2017 03:52:03 PM' , NULL, NULL, NULL),
       (10817835,  'JA118386' ,  '01/16/2017 04:30:00 PM' ,  '069XX S CORNELL AVE' ,  '0610' ,  'BURGLARY' ,  'FORCIBLE ENTRY' ,  'APARTMENT' ,  'False' ,  'False' , 332,  '3.0' , '5.0',  '43.0' ,  '05' , NULL, NULL, 2017,  '01/23/2017 03:52:03 PM' , NULL, NULL, NULL)