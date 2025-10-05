
CREATE SCHEMA bronze;
GO

-- Create the Bronze Layer table
CREATE TABLE bronze.flights_raw (
    FlightDate               VARCHAR(20) NULL,  -- Keep as string for raw ingestion
    CarrierCode              VARCHAR(10) NULL,
    Origin                   VARCHAR(5) NULL,
    Destination              VARCHAR(5) NULL,
    ScheduledDepartureTime   INT NULL,
    DepartureDelay           FLOAT(53) NULL,
    ArrivalDelay             FLOAT(53) NULL,
    CancelledFlag            FLOAT(53) NULL,
    Distance                 FLOAT(53) NULL,
    CarrierDelay             FLOAT(53) NULL,
    NASDelay                 FLOAT(53) NULL,
    SourceYear               VARCHAR(4) NULL    -- The new column for auditability!
);
GO