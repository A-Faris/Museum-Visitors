-- psql -h c11-faris-museum-db.c57vkec7dkkx.eu-west-2.rds.amazonaws.com -p 5432 -d museum -U username -W -f query.sql
SELECT * FROM review
ORDER BY created_at DESC