WITH transformed_data AS (
  SELECT
    title, url, source, date::DATE
  FROM raw

)

SELECT
  *
FROM
  transformed_data