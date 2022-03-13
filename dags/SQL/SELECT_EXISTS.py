def SELECT_EXISTS(obj, obj_name, logical_year=None):
    if obj == 'database':
        return  '''
                SELECT EXISTS
                (
                SELECT
                datname
                FROM
                pg_database
                WHERE
                datname = '%s'
                 );
                 ''' % (obj_name)
    else:
        return  '''
                SELECT EXISTS
                (
                SELECT
                TO_CHAR("FL_DATE", 'YYYY')
                FROM
                "%s"
                WHERE
                TO_CHAR("FL_DATE", 'YYYY') = '%s'
                GROUP BY
                TO_CHAR("FL_DATE", 'YYYY')
                );
                ''' % (obj_name, logical_year)