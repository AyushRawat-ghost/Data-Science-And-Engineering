# 1. Safety Widget
dbutils.widgets.text("safety_pin", "", "Enter Launch Code")
entered_code = "Omnitrix Overide Code 6342" 
SECRET_LAUNCH_CODE = "Omnitrix Overide Code 6342"

if entered_code != SECRET_LAUNCH_CODE:
    dbutils.widgets.remove("safety_pin") 
    dbutils.notebook.exit("❌ Access Denied: Standing down.")

print("🚀 Launch Code Verified. Initiating Total System Purge...")

# 2. Purge Core Layers (Bronze & Silver)
core_tables = [
    "instagram.realbronzelayer.instagram_usage_lifestyle",
    "instagram.silverlayer.silver_instagram_users",
    "instagram.silverlayer.quarantine_instagram_users"
]

for table in core_tables:
    try:
        spark.sql(f"DROP TABLE IF EXISTS {table}")
        print(f"✅ Purged Core Table: {table}")
    except Exception as e:
        print(f"⚠️ Failed to drop {table}: {str(e)}")

# 3. Dynamic Purge for the Gold Layer (Handles Tables & Views)
try:
    # Get all objects currently in the gold layer
    gold_objects = spark.sql("SHOW TABLES IN instagram.goldlayer").collect()
    
    for row in gold_objects:
        obj_name = f"instagram.goldlayer.{row['tableName']}"
        
        try:
            # Attempt to drop as a table
            spark.sql(f"DROP TABLE IF EXISTS {obj_name}")
            print(f"✅ Purged Gold Table: {obj_name}")
        except Exception as err:
            # If Spark complains it's a view, drop it correctly
            if "is a VIEW" in str(err):
                spark.sql(f"DROP VIEW IF EXISTS {obj_name}")
                print(f"✅ Purged Gold View: {obj_name}")
            else:
                print(f"⚠️ Error on {obj_name}: {str(err)}")
except Exception as e:
    print(f"⚠️ Gold Layer access skipped (may already be empty): {str(e)}")

print("\n🔥 TOTAL RESET COMPLETE. Your environment is sparkling clean, bro!")
dbutils.widgets.remove("safety_pin")