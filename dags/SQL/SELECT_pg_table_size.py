def SELECT_pg_table_size(table_name, logical_year):
    return  '''
            SELECT
            pg_table_size('"%s_%s"');
            ''' % (table_name, logical_year)