#!env python
# vim: set fileencoding=UTF8 :
# Taken from https://github.com/dergachev/redmine-reconcile
"""
See http://code.google.com/p/google-refine/wiki/ReconciliationServiceApi.
See https://github.com/mikejs/reconcile-demo
"""
import re, yaml, ldap, sys, logging
import __builtin__

from flask import Flask, request, jsonify, json
app = Flask(__name__)

class string_tricks(str):
    def replace_umlauts (self):
        chars = {'ö': 'oe','ä': 'ae','ü': 'ue', 'ß': 'ss'} 
        for char in chars:
            self = self.replace(char,chars[char])
        return str
        
# Add methods, that you want to use in the configuration YAML file as operations here.

__builtin__.str = string_tricks

def ldap_search (con, base, scope, filter, attrs):
    logger.debug('Searching for ' + filter + ' in ' + base)
    try:
        result = con.search_s(base, scope, filter, attrs)
        logger.debug('Got ' + str(len(result)) + ' result(s)')
    except ldap.LDAPError, error_message:
        print "Couldn't search. %s " % error_message
        result = []
    return result

def ldap_connection(server, binddn, password):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    try:
        con = ldap.initialize(server)
        con.simple_bind_s(binddn, password)
        logger.debug('connected to ' + server +' as user ' + binddn)
    except ldap.LDAPError, error_message:
        print "Couldn't connect. %s " % error_message
    return con

def evaluate_operation(operation, str):
    cmd = "map(lambda x: x.{0}, [str])".format(operation)
    logger.debug("Evaluating " + cmd)
    r = eval(cmd)[0]
    logger.debug("Result: " + r)
    return r

def format_results(results, query, score, name):
    def filter_entries (str):
        if search_attrs is not None and search_attrs not in ["*"]:
            return True
        if str in ["sambaSID", "objectClass", "cocom", "userServices", "platforms", "disableReason"]:
            return False
        elif str in ["goesternQuellSystem", "mailHost", "mailboxServer", "userType"]: 
            return False
        elif str.startswith('exchange'):
            return False
        elif str in "Cloud" or str in "cloud":
            return False
        elif str.endswith('Shell') or str.endswith('Status') or str.endswith('Number'):
            return False
        elif str.endswith('Date') or str.endswith('Modified'):
            return False
        elif str.endswith('Directory'):
            return False
        else:
            return True
    
    matches = []
    if (len(results) > 0):
        if type(results) == list:
            for item in results:
                (dn, attrs) = item
                logger.debug("Got match in DN: " + dn)
                match = {}
                if (attrs.has_key(name)):
                    name = attrs[name][0]
                else:
                    name = query
                match.update({
                    "id": attrs[id][0],
                    "name": name,
                    "score": score,
                    "match": True,
                    "type": [
                        {"id": "/goefis/ldap",
                         "name": "GoeFIS LDAP Entry"}]})
                for k, v in attrs.iteritems():
                    if filter_entries(k):
                        if type(v) == list and len (v) == 1:
                            match[k] = v[0]
                        else: 
                            match[k] = v
            matches.append(match)
    return matches

def filter_false_positives(matches, score = 95):
    filtered_matches = []
    #get highest score
    high_score = 0
    for match in matches:
        if match["score"] > high_score:
            high_score = match["score"]
    logger.debug("Highest score is " + str(high_score))
    if high_score >= score:
        for match in matches:
            if match["score"] >= score:
                filtered_matches.append(match)
            else:
                logger.debug("Dropping entry with score " + str(match["score"]))
        return filtered_matches
    else:
        return matches

def search(query):
    logger.debug("Got request for " + query)
    con = ldap_connection(server, binddn, password)
    scope = ldap.SCOPE_SUBTREE
    if search_attrs is not None and len(search_attrs) > 0:
        attrs = search_attrs
    else:
        attrs = ["*"]
    matches = []
    for filter in filters.keys():
    	score = filters[filter]['score']
    	if filters[filter].has_key('devide_by_matches') and filters[filter]['devide_by_matches'] is not None:
    	    devide_by_matches = filters[filter]['devide_by_matches']
    	else:
    	    devide_by_matches = False

    	if (filters[filter]['operation'] is not None and filters[filter]['operation'] != ''):
    	    logger.debug("Got filter " + filter + " with operation " + filters[filter]['operation'] + " and score " + str(filters[filter]['score']))
    	    modified_query = evaluate_operation(filters[filter]['operation'], query)
    	    search = filter.format(modified_query.encode('utf-8'))
    	else: 
            logger.debug("Got filter " + filter + " without operation and score " + str(filters[filter]['score']))
            search = filter.format(query.encode('utf-8'))

    	if filters[filter].has_key('name') and filters[filter]['name'] is not None:
    	    name = name
    	else:
    	    name = re.search('.*?(\w+).*', filter).group(0)

        logger.debug("Search filter evaluated to " + search)
        results = ldap_search(con, base, scope, search, attrs)
    
        if (len(results) > 0):
            if devide_by_matches:
                score = score / len(results)
            matches.extend(format_results(results, query, score, name))
    if (len(results) == 0):
        matches.append({
                    "id": '',
                    "name": query,
                    "score": 0,
                    "match": False,
                    "type": [
                        {"id": "/goefis/ldap",
                         "name": "GoeFIS LDAP Entry"}]})  
    
    if exact_match_score == 0:
        return matches
    else:
        return filter_false_positives(matches, exact_match_score)

def jsonpify(obj):
    """
    Like jsonify but wraps result in a JSONP callback if a 'callback'
    query param is supplied.
    """
    try:
        callback = request.args['callback']
        response = app.make_response("%s(%s)" % (callback, json.dumps(obj)))
        response.mimetype = "text/javascript"
        return response
    except KeyError:
        return jsonify(obj)


@app.route("/ldap-reconcile", methods=['POST', 'GET'])
def reconcile():
    # If a single 'query' is provided do a straightforward search.
    query = request.form.get('query')
    if query:
        # If the 'query' param starts with a "{" then it is a JSON object
        # with the search string as the 'query' member. Otherwise,
        # the 'query' param is the search string itself.
        if query.startswith("{"):
            query = json.loads(query)['query']
        results = search(query)
        logger.debug(json.dumps(results))
        return jsonpify({"result": results})

    # If a 'queries' parameter is supplied then it is a dictionary
    # of (key, query) pairs representing a batch of queries. We
    # should return a dictionary of (key, results) pairs.
    queries = request.form.get('queries')
    if queries:
        queries = json.loads(queries)
        results = {}
        for (key, query) in queries.items():
            results[key] = {"result": search(query['query'])}
        logger.debug(json.dumps(results))
        return jsonpify(results)

    # If neither a 'query' nor 'queries' parameter is supplied then
    # we should return the service metadata.
    return jsonpify(metadata)

if __name__ == '__main__':
# TODO allow user to specify a subclass of TestAnalyzer to use
    from sys import argv
    import argparse
    logger = logging.getLogger('ldap reconciler')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    parser = argparse.ArgumentParser(description='Reconcile LDAP users into IDs')
    parser.add_argument('config_file', metavar='config_file', help='Configuration to use for LDAP connection')
    args = parser.parse_args()
    config_file = args.config_file
    
    logger.debug('Reading configuration file ' + config_file)
    with open(config_file, 'r') as f:
         config = yaml.load(f)
    # Service settings
    port = config['self_port']
    
    # Connection settings
    server = config['host']
    binddn = config['base']
    password = config['password']

    # Read search settings
    base = config['search_base']
    filters = config['search_filter']
    exact_match_score = config['exact_match_score']
    search_attrs = config['search_attrs']
    id = config['id']

    # Basic service metadata. There are a number of other documented options
    # but this is all we need for a simple service.
    metadata = {
        "name": "LDAP Reconciliation Service",
        "defaultTypes": [{"id": "/goefis/ldap", "name": "GoeFIS LDAP Entry"}],
        "view": { "url" : server }
    }

    if port is None:
        logger.debug("Listining on http://locahost:5000")
        app.run(debug = True)
    else:
        logger.debug("Listining on http://locahost:" + str(port))
        app.run(debug = True, port = port)