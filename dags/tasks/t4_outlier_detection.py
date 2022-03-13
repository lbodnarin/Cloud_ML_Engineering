def t4_outlier_detection(secret, dbname, **context):

    from sklearn.neighbors import LocalOutlierFactor
    from SQL.INSERT_TABLE import INSERT_TABLE
    from SQL.SELECT_EXISTS import SELECT_EXISTS
    from SQL.SELECT_TABLE import SELECT_TABLE
    import numpy as np
    import pandas as pd
    import psycopg2

    logical_year = int(context['ds'][:4])
    conn = psycopg2.connect(host=secret['host'], dbname=dbname, user=secret['username'], password=secret['password'])
    cur = conn.cursor()
    cur.execute(SELECT_EXISTS('any_rows', 'DASHBOARD', logical_year))
    if cur.fetchone()[0] == False:
        df = pd.read_sql_query(SELECT_TABLE('CSV', logical_year, ['COUNT', 'AVG']), conn)
        ORIGIN = np.unique(df['ORIGIN'])
        for value in ORIGIN:
            X = df.loc[(df['ORIGIN']==value)&(df['DEP_DELAY'].notnull()), ['FL_NUM', 'DEP_DELAY']].to_numpy()
            n_samples = len(X)
            if n_samples > 1:
                n_neighbors = (lambda xx: 1 if xx<6 else round(xx*0.1))(n_samples)
                clf = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=0.01)
                df.loc[(df['ORIGIN']==value)&(df['DEP_DELAY'].notnull()), 'INLIER'] = clf.fit_predict(X)
        for index, row in df.replace({np.nan:'NULL'}).iterrows():
            INLIER = (lambda xx: (row['INLIER'] + 1) // 2 if xx!='NULL' else row['INLIER'])(row['INLIER'])
            cur.execute(INSERT_TABLE('DASHBOARD', row['FL_DATE'], row['ORIGIN'], row['FL_NUM'], row['DEP_DELAY'], INLIER))
        conn.commit()
    cur.close()
    conn.close()