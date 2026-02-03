
nuke_confirmed = False

if not nuke_confirmed:
    dbutils.notebook.exit("Nuke not confirmed. Skipping reset.")


print("🔥 Nuking the 'instagram' database...")
spark.sql("DROP TABLE IF EXISTS instagram.realbronzelayer.instagram_usage_lifestyle")
spark.sql("DROP TABLE IF EXISTS instagram.bronzelayer.instagram_usage_lifestyle")
spark.sql("DROP TABLE IF EXISTS instagram.silverlayer.silver_instagram_users")
spark.sql("DROP TABLE IF EXISTS instagram.silverlayer.quarantine_instagram_users")

print("Database has been purged")