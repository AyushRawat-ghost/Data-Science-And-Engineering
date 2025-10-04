**Assits** :
        Mentor : Alex, Learnit Training
        Honour To : *****i ***i
            Note : Name was not Disclosed due to privacy Concerns




**Column Creation Directories**:
    M language used to create new columns or DAX for creating calculated columns

        **Dim Customer**:
                Gender(Extracted) = if([GEN]=null) then [Gender] else [GEN]
                
                Country(Extracted) = if [Country] = "DE" then "Germany"
                                    else if [Country] = "US" or [Country] = "USA" then "United States"
                                    else [Country]

        **Dim Product**:
                Product Line(Extracted) = Value.Switch(
                                                [prd_line],
                                                {
                                                    {"M", "Mountain"},
                                                    {"R", "Road"},
                                                    {"S", "Other Sales"}
                                                },
                                                [prd_line]
                                            )
                Product Line(Extracted) = if [prd_line] = "M" then "Mountain"
                                            else if [prd_line] = "R" then "Road"
                                            else if [prd_line] = "S" then "Other Sales"
                                            else if [prd_line] = "T" then "Touring"
                                            else [prd_line]

                Product Cost (Extracted) = if [prd_cost] = null then 0
                                            else [prd_cost]

                Product End Date(Extracted) =
                                            VAR CurrentPrdStartDate = 'Dim Product'[prd_start_dt]
                                            VAR CurrentPrdKey = 'Dim Product'[prd_key]
                                            VAR NextPrdStartDate =
                                                CALCULATE (
                                                    MIN ( 'Dim Product'[prd_start_dt] ),
                                                    FILTER (
                                                        ALL ( 'Dim Product' ),
                                                        'Dim Product'[prd_key] = CurrentPrdKey && 'Dim Product'[prd_start_dt] > CurrentPrdStartDate
                                                    )
                                                )
                                            VAR LatestOverallDate = CALCULATE(MAX('Dim Product'[prd_start_dt]), ALL('Dim Product'))
                                            RETURN
                                                IF (
                                                    ISBLANK(NextPrdStartDate),
                                                    LatestOverallDate,
                                                    NextPrdStartDate - 1
                                                )

        **Fact Sales** :
                Sales Order Date(Extracted) = Date.FromText(Text.From([sls_order_dt]), [Format="yyyyMMdd"])
                Sales Ship Date(Extracted)  = Date.FromText(Text.From([[sls_ship_dt]]), [Format="yyyyMMdd"])
                Sales Due Date(Extracted)  = Date.FromText(Text.From([[sls_due_dt]]), [Format="yyyyMMdd"])

                Sales(Extracted) = if [sls_price] <> null then [sls_price]*[sls_quantity]
                                    else [sls_sales]

                Sales Price(Extracted) =if [#"Sales (Extracted)"] <> null then [#"Sales (Extracted)"]/[sls_quantity]
                                    else [sls_price]






**Measures**:


