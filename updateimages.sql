BEGIN TRANSACTION;

BEGIN TRY
    UPDATE Books
    SET ImageSource = REPLACE(ImageSource, 
                              'https://www.libraff.az/images/from_1c/', 
                              'https://baghirli.net/assets/bookslibraff/')
    WHERE ImageSource LIKE 'https://www.libraff.az/images/from_1c/%';

    COMMIT TRANSACTION;
    PRINT 'Update completed successfully.';
END TRY
BEGIN CATCH
    -- Rollback if there's any error
    ROLLBACK TRANSACTION;

    -- Optionally print the error
    PRINT 'An error occurred:';
    PRINT ERROR_MESSAGE();
END CATCH
