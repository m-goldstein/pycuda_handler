"""
    Wrapper class for InfluxDBClient
    Used to establish database connection and handle I/O
"""
from influxdb import InfluxDBClient
########################### Connection Info ###################################
HOST     = '192.168.2.41'
PORT     = 8086
USER     = ''
PASSWORD = ''
DB_NAME  = 'cryptix'
###############################################################################
class DBClient:
    host     = HOST
    port     = PORT
    user     = USER
    password = PASSWORD
    db_name  = DB_NAME
    session   = None
    
    def init_session(self, host=HOST, port=PORT, user=None, password=None):
	    if (user is not None and password is not None):
		    try:
			    self.session = InfluxDBClient(host=host, port=port, username=user, \
			    password=password, ssl=True, verify_ssl=True)
			    return self.session
		    except:
			    print("[init_session] Error establishing InfluxDB session with username %s\n"%(user))
			    pass
	    else:
		    try:
			    self.session = InfluxDBClient(host=host, port=port)
			    return self.session
		    except:
			    print("[init_session] Error establishing InfluxDB session\n")
			    pass

    def switch_database(self, db_name=DB_NAME):
	    if self.session is None:
		    print('[switch_database] Error: no client specified')
	    elif db_name is None:
		    print('[switch_database] Warning: no database specified. Using default.\n')
		    try:
			    self.session.switch_database('_internal')
		    except:
			    print("[switch_database] Error: cannot switch to default database.\n")		    
	    try:
		    self.session.switch_database(db_name)
	    except:
		    print("[switch_database] Error: cannot switch to database '%s'.\n"%(db_name))
		    pass
    
    def make_query(self, measurement="execution_time", is_ordered=True, limit=100):
	    results = []
	    query_statement = ''
	    if (self.session is None):
		    print("[make_query] Error: DBClient session is not initialized.\n")
		    return []
	    if (is_ordered is True):
		    query_statement = 'SELECT *	FROM "%s" ORDER BY time LIMIT %d'%(measurement, limit)
	    else:
		    query_statement = 'SELECT * FROM "%s" LIMIT %d'%(measurement, limit)
	    try:
		    results = self.session.query(query_statement)
		    return results.raw
	    except:
		    print("[make_query] Error: could not make query: %s.\n"%(query_statement))
		    return []
