def CREATE_DATABASE(dbname, OWNER):
    return  '''
            CREATE DATABASE
            "%s"
            OWNER "%s";
            ''' % (dbname, OWNER)