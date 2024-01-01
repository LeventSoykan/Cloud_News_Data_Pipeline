WITH transformed_data AS (
  SELECT
    title, url, source, date::DATE
  FROM
    {{ ref('raw') }}
)

SELECT
  *
FROM
  transformed_data;