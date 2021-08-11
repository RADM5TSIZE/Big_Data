CREATE TABLE IF NOT EXISTS Chicago_Crimes_test_sample (
    `ID` INT,
    `Case_Number` VARCHAR(8) CHARACTER SET utf8,
    `Date` DATETIME,
    `Block` VARCHAR(22) CHARACTER SET utf8,
    `IUCR` INT,
    `Primary_Type` VARCHAR(26) CHARACTER SET utf8,
    `Description` VARCHAR(32) CHARACTER SET utf8,
    `Location_Description` VARCHAR(18) CHARACTER SET utf8,
    `Arrest` VARCHAR(5) CHARACTER SET utf8,
    `Domestic` VARCHAR(5) CHARACTER SET utf8,
    `Beat` INT,
    `District` NUMERIC(3, 1),
    `Ward` NUMERIC(3, 1),
    `Community_Area` NUMERIC(3, 1),
    `FBI_Code` VARCHAR(3) CHARACTER SET utf8,
    `X_Coordinate` INT,
    `Y_Coordinate` INT,
    `Year` INT,
    `Updated_On` DATETIME,
    `Latitude` INT,
    `Longitude` INT,
    `Location` VARCHAR(50) CHARACTER SET utf8
);



INSERT INTO Chicago_Crimes_sample (ID, Case Number, Date, Block, IUCR, Primary Type, Description, Location Description, Arrest, Domestic, Beat, District, Ward, Community Area, FBI Code, X Coordinate, Y Coordinate, Year, Updated On, Latitude, Longitude, Location)

VALUES (4786321, 'HM399414', '01/01/2004 12:01:00 AM', '082XX S COLES AVE', 0840, 'THEFT', 'FINANCIAL ID THEFT: OVER $300', 'RESIDENCE', 'False', 'False', 424, '4.0', '7.0', '46.0', '06', NULL, NULL, 2004.0, '08/17/2015 03:03:40 PM', NULL, NULL, NULL);
