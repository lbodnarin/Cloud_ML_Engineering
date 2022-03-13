def SELECT_TABLE(table_name, logical_year, aggregate_functions=None):
    if aggregate_functions != None:
        return  '''
                SELECT
                "FL_DATE",
                "ORIGIN",
                %s(*) AS "FL_NUM",
                CAST(%s("DEP_DELAY") AS DECIMAL(6,2)) AS "DEP_DELAY"
                FROM
                "%s_%s"
                GROUP BY
                "FL_DATE",
                "ORIGIN"
                ORDER BY
                "FL_DATE",
                "ORIGIN";
                ''' % (aggregate_functions[0], aggregate_functions[1], table_name, logical_year)
    else:
        return  '''
                SELECT
                "FL_DATE",
                "ORIGIN",
                "FL_NUM",
                "DEP_DELAY",
                "INLIER"
                FROM
                "%s"
                WHERE
                TO_CHAR("FL_DATE", 'YYYY') = '%s'
                ORDER BY
                "FL_DATE",
                "ORIGIN";
                ''' % (table_name, logical_year)