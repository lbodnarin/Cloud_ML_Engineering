def CREATE_TABLE(table_name, logical_year=None):
    if table_name == 'CSV':
        return  '''
                CREATE TABLE IF NOT EXISTS
                "%s_%s"
                (
                "FL_DATE" date,
                "OP_CARRIER" char(2),
                "OP_CARRIER_FL_NUM" smallint,
                "ORIGIN" char(3),
                "DEST" char(3),
                "CRS_DEP_TIME" decimal,
                "DEP_TIME" decimal,
                "DEP_DELAY" decimal,
                "TAXI_OUT" decimal,
                "WHEELS_OFF" decimal,
                "WHEELS_ON" decimal,
                "TAXI_IN" decimal,
                "CRS_ARR_TIME" decimal,
                "ARR_TIME" decimal,
                "ARR_DELAY" decimal,
                "CANCELLED" decimal,
                "CANCELLATION_CODE" char,
                "DIVERTED" decimal,
                "CRS_ELAPSED_TIME" decimal,
                "ACTUAL_ELAPSED_TIME" decimal,
                "AIR_TIME" decimal,
                "DISTANCE" decimal,
                "CARRIER_DELAY" decimal,
                "WEATHER_DELAY" decimal,
                "NAS_DELAY" decimal,
                "SECURITY_DELAY" decimal,
                "LATE_AIRCRAFT_DELAY" decimal,
                "Unnamed: 27" decimal
                );
                ''' % (table_name, logical_year)
    else:
        return  '''
                CREATE TABLE IF NOT EXISTS
                "%s"
                (
                "FL_DATE" date,
                "ORIGIN" char(3),
                "FL_NUM" smallint,
                "DEP_DELAY" decimal,
                "INLIER" smallint
                );
                ''' % (table_name)