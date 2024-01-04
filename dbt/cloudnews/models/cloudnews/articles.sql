WITH transformed_data AS (
      SELECT
        title, url, source, date::DATE, query_date::DATE
      FROM raw
    )

    SELECT
      *
    FROM
      transformed_data