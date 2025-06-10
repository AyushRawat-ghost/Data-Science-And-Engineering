















**KPI's Requirements**:
    1.Total Sales: The overall revenue generated from all items sold.
    2.Average Sales: The average revenue per sale.
    3.Number of Items: The total count of different items sold.
    4.Average Rating: The average customer rating for items sold.



**Business Requirement**:
    1.Total Sales by Fat Content:
        Objective: Analyze the impact of fat content on total sales.
        Additional KPI Metrics: Assess how other KPIs (Average Sales, Number of Items, Average Rating) vary with fat content.
        Chart Type: Donut Chart.

    2.Total Sales by Item Type:
        Objective: Identify the performance of different item types in terms of total sales.
        Additional KPI Metrics: Assess how other KPIs (Average Sales, Number of Items, Average Rating) vary with fat content.
        Chart Type: Bar Chart.

    3.Fat Content by Outlet for Total Sales:
        Objective: Compare total sales across different outlets segmented by fat content.
        Additional KPI Metrics: Assess how other KPIs (Average Sales, Number of Items, Average Rating) vary with fat content.
        Chart Type: Stacked Column Chart.

    4.Total Sales by Outlet Establishment:
        Objective: Evaluate how the age or type of outlet establishment influences total sales.
        Chart Type: Line Chart.

     5.Sales by Outlet Size:
        Objective: Analyze the correlation between outlet size and total sales.
        Chart Type: Donut/ Pie Chart.

    6.Sales by Outlet Location:
        Objective: Assess the geographic distribution of sales across different locations.
        Chart Type: Funnel Map.

    7.All Metrics by Outlet Type:
        Objective: Provide a comprehensive view of all key metrics (Total Sales, Average Sales, Number of Items, Average Rating) broken down by different outlet types.
        Chart Type: Matrix Card.



**Power Query**:
    Item Fat Content (Extracted):
        if[Item Fat Content]="LF" then "Low Fat"
        else if [Item Fat Content]="reg" then "Regular"
        else [Item Fat Content]

    
**DAX Queries**:
    Total Sales = SUM('BlinkIT Grocery Data'[Sales])
    Average Sales = AVERAGE('BlinkIT Grocery Data'[Sales])
    No of Items = COUNTROWS('BlinkIT Grocery Data')
    Average Rating = AVERAGE('BlinkIT Grocery Data'[Rating])

    KPI Metrics = {
        ("Total Sales", NAMEOF('BlinkIT Grocery Data'[Total Sales]), 0),
        ("Average Sales", NAMEOF('BlinkIT Grocery Data'[Average Sales]), 1),
        ("No of Items", NAMEOF('BlinkIT Grocery Data'[No of Items]), 2),
        ("Average Rating", NAMEOF('BlinkIT Grocery Data'[Average Rating]), 3)
    }