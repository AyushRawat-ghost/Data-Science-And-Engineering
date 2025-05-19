/*
Script Purpose :
    This Script create a Database and Create 3 schemas that Resonates to Medallion Model

Warning :
    If Database exist drop it and re run  the script
*/


USE Master;
go

-- Data base Creation
CREATE DATABASE DataWarehouse;

-- Switching to the Data Base
use DataWarehouse;
go

-- Creating the Schemas
create schema bronze;
go
create schema silver;
go
create schema gold;
