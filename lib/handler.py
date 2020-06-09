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
			    self.session = InfluxDBClient(host=host, port=port, username=user, password=password, ssl=True, verify_ssl=True)
			    return self.session
		    except:
			    print("Error establishing InfluxDB session with username %s\n"%(user))
			    pass
	    else:
		    try:
			    self.session = InfluxDBClient(host=host, port=port)
			    return self.session
		    except:
			    print("Error establishing InfluxDB session\n")
			    pass

    def switch_database(self, db_name=DB_NAME):
	    if self.session is None:
		    print('Error: no client specified')
	    elif db_name is None:
		    print('Warning: no database specified. Using default.\n')
		    try:
			    self.session.switch_database('_internal')
		    except:
			    print("Error: cannot switch to default database.\n")		    
	    try:
		    self.session.switch_database(db_name)
	    except:
		    print("Error: cannot switch to database '%s'.\n"%(db_name))
		    pass

"""
def make_client_session(host=HOST, port=PORT, user=None, password=None):
    if (user is not None and password is not None):
	    try:
		    client = InfluxDBClient(host=host, port=port, username=user, password=password, ssl=True, verify_ssl=True)
		    return client
	    except:
		    print("Error establishing InfluxDB session with username %s\n"%(user))
		    pass
    else:
	    try:
		    client = InfluxDBClient(host=host, port=port)
		    return client
	    except:
		    print("Error establishing InfluxDB session\n")
		    pass


def switch_database(client=None, db_name=DB_NAME):
    if client is None:
	    print('Error: no client specified')
    elif db_name is None:
	    print('Warning: no database specified. Using default.\n')
	    try:
		    client.switch_database('_internal')
	    except:
		    print("Error: cannot switch to default database.\n")
		    
    try:
	    client.switch_database(db_name)
    except:
	    print("Error: cannot switch to database '%s'.\n"%(db_name))
	    pass
"""
def make_query(measurement="execution_time", is_ordered=True, limit=100):
    try:
	    pass
    except:
	    pass
	
## main function ##
def main():
    client = DBClient() 
    client.init_session(HOST, PORT)
    client.switch_database(DB_NAME)
main()

