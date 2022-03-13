def t2_create_table(secret, dbname, **context):

    from SQL.CREATE_TABLE import CREATE_TABLE
    import psycopg2

    logical_year = int(context['ds'][:4])
    conn = psycopg2.connect(host=secret['host'], dbname=dbname, user=secret['username'], password=secret['password'])
    cur = conn.cursor()
    cur.execute(CREATE_TABLE('CSV', logical_year))
    cur.execute(CREATE_TABLE('DASHBOARD'))
    conn.commit()
    cur.close()
    conn.close()