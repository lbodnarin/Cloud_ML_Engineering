def t3_copy_from(bucket, secret, dbname, **context):

    from SQL.SELECT_pg_table_size import SELECT_pg_table_size
    import psycopg2

    logical_year = int(context['ds'][:4])
    key = '.CSV/%s.csv' % (logical_year)
    obj = bucket.Object(key)
    if obj.content_length:
        body = obj.get(Range='bytes=329-')['Body']
        conn = psycopg2.connect(host=secret['host'], dbname=dbname, user=secret['username'], password=secret['password'])
        cur = conn.cursor()
        cur.execute(SELECT_pg_table_size('CSV', logical_year))
        if cur.fetchone()[0] == 8192:
            cur.copy_from(body, 'CSV_%s' % (logical_year), sep=',', null='')
            conn.commit()
        cur.close()
        conn.close()