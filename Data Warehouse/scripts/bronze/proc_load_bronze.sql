use DataWarehouse;
go


CREATE OR ALTER PROCEDURE bronze.load_bronze AS
BEGIN
    DECLARE
        @start_time DATETIME,
        @end_time DATETIME,
        @batch_start_time DATETIME,
        @batch_end_time DATETIME,
        @file_path NVARCHAR(255);

    BEGIN TRY
        SET @batch_start_time = GETDATE();
        PRINT '================================================';
        PRINT 'Bronze Layer : Activated';
        PRINT '================================================';

        PRINT '------------------------------------------------';
        PRINT 'CRM Tables : Loaded';
        PRINT '------------------------------------------------';

        SET @file_path = 'C:\Users\Ayush\Git Repo\Data-Science-And-Engineering\Data Warehouse\datasets\source_crm\';

        SET @start_time = GETDATE();
        PRINT ' Deleting Content : bronze.crm_cust_info';
        TRUNCATE TABLE bronze.crm_cust_info;
        PRINT ' Inserting Data : bronze.crm_cust_info';
        EXEC ('
            BULK INSERT bronze.crm_cust_info
            FROM ''' + @file_path + 'cust_info.csv''
            WITH (
                FIRSTROW = 2,
                FIELDTERMINATOR = '','',
                TABLOCK
            );
        ');
        SET @end_time = GETDATE();
        PRINT ' Load Time : ' + CAST(DATEDIFF(millisecond, @start_time, @end_time) AS NVARCHAR) + ' milliseconds';
        PRINT ' -------------';

        SET @start_time = GETDATE();
        PRINT ' Deleting Content  : bronze.crm_prd_info';
        TRUNCATE TABLE bronze.crm_prd_info;

        PRINT ' Inserting Data : bronze.crm_prd_info';
        EXEC ('
            BULK INSERT bronze.crm_prd_info
            FROM ''' + @file_path + 'prd_info.csv''
            WITH (
                FIRSTROW = 2,
                FIELDTERMINATOR = '','',
                TABLOCK
            );
        ');
        SET @end_time = GETDATE();
        PRINT ' Load Time : ' + CAST(DATEDIFF(millisecond, @start_time, @end_time) AS NVARCHAR) + ' milliseconds';
        PRINT ' -------------';

        SET @start_time = GETDATE();
        PRINT ' Deleting Content  : bronze.crm_sales_details';
        TRUNCATE TABLE bronze.crm_sales_details;
        PRINT ' Inserting Data : bronze.crm_sales_details';
        EXEC ('
            BULK INSERT bronze.crm_sales_details
            FROM ''' + @file_path + 'sales_details.csv''
            WITH (
                FIRSTROW = 2,
                FIELDTERMINATOR = '','',
                TABLOCK
            );
        ');
        SET @end_time = GETDATE();
        PRINT 'Load Time ' + CAST(DATEDIFF(millisecond, @start_time, @end_time) AS NVARCHAR) + ' milliseconds';
        PRINT '';

        PRINT '------------------------------------------------';
        PRINT 'ERP Tables : Loaded';
        PRINT '------------------------------------------------';

        SET @file_path = 'C:\Users\Ayush\Git Repo\Data-Science-And-Engineering\Data Warehouse\datasets\source_erp\';

        SET @start_time = GETDATE();
        PRINT 'Deleting Content  : bronze.erp_loc_a101';
        TRUNCATE TABLE bronze.erp_loc_a101;
        PRINT 'Inserting Data : bronze.erp_loc_a101';
        EXEC ('
            BULK INSERT bronze.erp_loc_a101
            FROM ''' + @file_path + 'LOC_A101.csv''
            WITH (
                FIRSTROW = 2,
                FIELDTERMINATOR = '','',
                TABLOCK
            );
        ');
        SET @end_time = GETDATE();
        PRINT ' Load Time : ' + CAST(DATEDIFF(millisecond, @start_time, @end_time) AS NVARCHAR) + ' milliseconds';
        PRINT ' -------------';

        SET @start_time = GETDATE();
        PRINT ' Deleting Content  : bronze.erp_cust_az12';
        TRUNCATE TABLE bronze.erp_cust_az12;
        PRINT ' Inserting Data  : bronze.erp_cust_az12';
        EXEC ('
            BULK INSERT bronze.erp_cust_az12
            FROM ''' + @file_path + 'CUST_AZ12.csv''
            WITH (
                FIRSTROW = 2,
                FIELDTERMINATOR = '','',
                TABLOCK
            );
        ');
        SET @end_time = GETDATE();
        PRINT 'Load Time : ' + CAST(DATEDIFF(millisecond, @start_time, @end_time) AS NVARCHAR) + ' milliseconds';
        PRINT '-------------';

        SET @start_time = GETDATE();
        PRINT 'Deleting Content  : bronze.erp_px_cat_g1v2';
        TRUNCATE TABLE bronze.erp_px_cat_g1v2;
        PRINT 'Inserting Data  : bronze.erp_px_cat_g1v2';
        EXEC ('
            BULK INSERT bronze.erp_px_cat_g1v2
            FROM ''' + @file_path + 'PX_CAT_G1V2.csv''
            WITH (
                FIRSTROW = 2,
                FIELDTERMINATOR = '','',
                TABLOCK
            );
        ');
        SET @end_time = GETDATE();
        PRINT ' Load Time : ' + CAST(DATEDIFF(millisecond, @start_time, @end_time) AS NVARCHAR) + ' milliseconds';
        PRINT ' -------------';

        SET @batch_end_time = GETDATE();
        PRINT '=========================================='
        PRINT 'Bronze Layer : Completed';
        PRINT 'Total Load Time :  ' + CAST(DATEDIFF(millisecond, @batch_start_time, @batch_end_time) AS NVARCHAR) + ' milliseconds';
        PRINT '=========================================='
    END TRY
    BEGIN CATCH
        PRINT '=========================================='
        PRINT 'Fatal Error Need to Re-Configure'
        PRINT 'Error Message: ' + ERROR_MESSAGE();
        PRINT 'Error Number: ' + CAST(ERROR_NUMBER() AS NVARCHAR);
        PRINT 'Error State: ' + CAST(ERROR_STATE() AS NVARCHAR);

         INSERT INTO ErrorLog (ProcedureName, ErrorMessage, ErrorNumber, ErrorState, ErrorSeverity, ErrorLine, EventTime)
         VALUES ('bronze.load_bronze', ERROR_MESSAGE(), ERROR_NUMBER(), ERROR_STATE(), ERROR_SEVERITY(), ERROR_LINE(), GETDATE());
        THROW;
    END CATCH
END;
