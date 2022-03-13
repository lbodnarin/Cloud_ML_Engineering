def t1_create_database(secret, dbname, OWNER, **context):

    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    from SQL.CREATE_DATABASE import CREATE_DATABASE
    from SQL.SELECT_EXISTS import SELECT_EXISTS
    import psycopg2

    logical_year = int(context['ds'][:4])
    conn = psycopg2.connect(host=secret['host'], dbname='postgres', user=secret['username'], password=secret['password'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(SELECT_EXISTS('database', dbname))
    if cur.fetchone()[0] == False:
        cur.execute(CREATE_DATABASE(dbname, OWNER))
    cur.close()
    conn.close()