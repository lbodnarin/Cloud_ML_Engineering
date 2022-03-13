def INSERT_TABLE(table_name, FL_DATE, ORIGIN, FL_NUM, DEP_DELAY, INLIER):
    return  '''
            INSERT INTO
            "%s"
            (
            "FL_DATE",
            "ORIGIN",
            "FL_NUM",
            "DEP_DELAY",
            "INLIER"
            )
            VALUES
            (
            '%s',
            '%s',
            %s,
            %s,
            %s
            );
            ''' % (table_name, FL_DATE, ORIGIN, FL_NUM, DEP_DELAY, INLIER)