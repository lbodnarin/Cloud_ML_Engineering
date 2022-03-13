def t5_matplotlib(bucket, secret, dbname, **context):

    from SQL.SELECT_TABLE import SELECT_TABLE
    import io
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import psycopg2

    logical_year = int(context['ds'][:4])
    key = '.PNG/%s/' % (logical_year)
    if sum(1 for _ in bucket.objects.filter(Prefix=key)) == 0:
        conn = psycopg2.connect(host=secret['host'], dbname=dbname, user=secret['username'], password=secret['password'])
        df = pd.read_sql_query(SELECT_TABLE('DASHBOARD', logical_year), conn)
        conn.close()
        ORIGIN = np.unique(df['ORIGIN'])
        for value in ORIGIN:
            X = df.loc[df['ORIGIN']==value, ['FL_DATE', 'FL_NUM', 'INLIER']].to_numpy()
            fig, ax = plt.subplots(figsize=(10.24,7.68), constrained_layout=True)
            ax.set_title('%s-%s-Flights per day' % (logical_year, value), fontweight=1000)
            ax.set_ylabel('Flights', fontweight=1000)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.plot(X[:, 0], X[:, 1], 'c', linewidth=1, label='Flights', zorder=1)
            ax.scatter(X[X[:, 2]==False, 0], X[X[:, 2]==False, 1], s=75, facecolors='none', edgecolors='k', linewidth=2.0, label='Outliers: %s' % ([x.strftime('%d-%b') for x in X[X[:, 2]==False, 0]]), zorder=2)
            legend = ax.legend(loc='upper left')
            legend.legendHandles[0]._sizes = [10]
            legend.legendHandles[1]._sizes = [20]
            for label in ax.get_xticklabels(which='major'):
                label.set(rotation=30, horizontalalignment='right', fontweight=1000)
            f = io.BytesIO()
            fig.savefig(f, format='png')
            body = f.getvalue()
            bucket.put_object(Key='.PNG/%s/%s.png' % (logical_year, value), Body=body)
            plt.close(fig=fig)