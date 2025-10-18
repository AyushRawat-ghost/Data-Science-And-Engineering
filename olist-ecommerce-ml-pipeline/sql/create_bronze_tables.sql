-- DDL for the 9 Olist tables for BRONZE schema

-- 1. OLIST CUSTOMERS DATASET
IF OBJECT_ID('bronze.customers_raw', 'U') IS NOT NULL DROP TABLE bronze.customers_raw;
CREATE TABLE bronze.customers_raw (
    customer_id             VARCHAR(50),
    customer_unique_id      VARCHAR(50),
    customer_zip_code_prefix VARCHAR(10),
    customer_city           VARCHAR(100),
    customer_state          VARCHAR(10)
);
GO

-- 2. OLIST ORDERS DATASET
IF OBJECT_ID('bronze.orders_raw', 'U') IS NOT NULL DROP TABLE bronze.orders_raw;
CREATE TABLE bronze.orders_raw (
    order_id                        VARCHAR(50),
    customer_id                     VARCHAR(50),
    order_status                    VARCHAR(50),
    order_purchase_timestamp        VARCHAR(50),
    order_approved_at               VARCHAR(50),
    order_delivered_carrier_date    VARCHAR(50),
    order_delivered_customer_date   VARCHAR(50),
    order_estimated_delivery_date   VARCHAR(50)
);
GO

-- 3. OLIST ORDER ITEMS DATASET
IF OBJECT_ID('bronze.order_items_raw', 'U') IS NOT NULL DROP TABLE bronze.order_items_raw;
CREATE TABLE bronze.order_items_raw (
    order_id                    VARCHAR(50),
    order_item_id               INT,
    product_id                  VARCHAR(50),
    seller_id                   VARCHAR(50),
    shipping_limit_date         VARCHAR(50),
    price                       DECIMAL(10, 2),
    freight_value               DECIMAL(10, 2)
);
GO

-- 4. OLIST ORDER REVIEWS DATASET
IF OBJECT_ID('bronze.reviews_raw', 'U') IS NOT NULL DROP TABLE bronze.reviews_raw;
CREATE TABLE bronze.reviews_raw (
    review_id                   VARCHAR(50),
    order_id                    VARCHAR(50),
    review_score                INT,
    review_comment_title        VARCHAR(MAX),
    review_comment_message      VARCHAR(MAX),
    review_creation_date        VARCHAR(50),
    review_answer_timestamp     VARCHAR(50)
);
GO

-- 5. OLIST PRODUCTS DATASET
IF OBJECT_ID('bronze.products_raw', 'U') IS NOT NULL DROP TABLE bronze.products_raw;
CREATE TABLE bronze.products_raw (
    product_id                      VARCHAR(50),
    product_category_name           VARCHAR(100),
    product_name_lenght             INT,
    product_description_lenght      INT,
    product_photos_qty              INT,
    product_weight_g                DECIMAL(10, 2),
    product_length_cm               DECIMAL(10, 2),
    product_height_cm               DECIMAL(10, 2),
    product_width_cm                DECIMAL(10, 2)
);
GO

-- 6. PRODUCT CATEGORY NAME TRANSLATION
IF OBJECT_ID('bronze.category_trans_raw', 'U') IS NOT NULL DROP TABLE bronze.category_trans_raw;
CREATE TABLE bronze.category_trans_raw (
    product_category_name           VARCHAR(100),
    product_category_name_english   VARCHAR(100)
);
GO

-- 7. OLIST ORDER PAYMENTS DATASET
IF OBJECT_ID('bronze.payments_raw', 'U') IS NOT NULL DROP TABLE bronze.payments_raw;
CREATE TABLE bronze.payments_raw (
    order_id                    VARCHAR(50),
    payment_sequential          INT,
    payment_type                VARCHAR(50),
    payment_installments        INT,
    payment_value               DECIMAL(10, 2)
);
GO

-- 8. OLIST SELLERS DATASET
IF OBJECT_ID('bronze.sellers_raw', 'U') IS NOT NULL DROP TABLE bronze.sellers_raw;
CREATE TABLE bronze.sellers_raw (
    seller_id                   VARCHAR(50),
    seller_zip_code_prefix      VARCHAR(10),
    seller_city                 VARCHAR(100),
    seller_state                VARCHAR(10)
);
GO

-- 9. OLIST GEOLOCATION DATASET
IF OBJECT_ID('bronze.geolocation_raw', 'U') IS NOT NULL DROP TABLE bronze.geolocation_raw;
CREATE TABLE bronze.geolocation_raw (
    geolocation_zip_code_prefix VARCHAR(10),
    geolocation_lat             DECIMAL(12, 8),
    geolocation_lng             DECIMAL(12, 8),
    geolocation_city            VARCHAR(100),
    geolocation_state           VARCHAR(10)
);
GO