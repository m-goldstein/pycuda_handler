"""
    Raw database data parser and interface for CUDA kernels
"""
from handler import DBClient
from handler import HOST, PORT, USER, PASSWORD, DB_NAME
def init_client():
    client = DBClient()
    print("Client created.")
    client.init_session(HOST, PORT)
    print("Client session initialized.")
    client.switch_database(DB_NAME)
    print("Client session database set.")
    return client

def vectorize_by_exchange(results=None):
    if (results is None):
	    print("[vectorize_by_exchange] Error: result set is None!\n")
	    return []
    result_dict = {}
    data_set = results['series'][0]['values']
    for i in range(len(data_set)):
	    exchange = data_set[i][4]
	    if exchange in result_dict.keys():
		    result_dict[exchange].append(data_set[i][5])
	    elif exchange not in result_dict.keys():
		    result_dict[exchange] = []
		    result_dict[exchange].append(data_set[i][5])
    return result_dict
