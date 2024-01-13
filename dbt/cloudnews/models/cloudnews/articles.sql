WITH transformed_data AS (
      SELECT
        title, url, source, date::DATE, query_date::DATE
      FROM raw
      WHERE date::DATE >= query_date::DATE - INTERVAL '30' DAY
      ORDER BY date::DATE DESC
    )

    SELECT
      *
    FROM
      transformed_data