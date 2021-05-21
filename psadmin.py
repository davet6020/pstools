#// argv[0] is the name of the program and not used.
#// argv[1] is option on/off
#// argv[2] is IP Address of Replica
#// argv[3] is the vdb cluster nanme for the agent to log
import json
import mysql.connector
import sys



proxysqlserverip = open('ip_proxysql.us', 'r')

for psip in proxysqlserverip:
  data = psip.split()

if not psip:
  print('There was no IP for the ProxySQL env.')
  exit()
else:
  proxyip = data[0]
  print('ProxySQL Server IP:', proxyip)

cnx = mysql.connector.connect(user='api', 
                              password='W3akPa$$word',
                              host=proxyip,
                              database='proxysql')

cursor = cnx.cursor()

primary = 3
replica = 13

if len(sys.argv) == 2 and sys.argv[1] == 'ALL':
  query = ("SELECT hostgroup, host_id, status FROM proxy ")
  cursor.execute(query)
else:
  query = ("SELECT hostgroup, host_id, status FROM proxy "
         "WHERE hostgroup in(%s, %s)")
  cursor.execute(query, (primary, replica))

print('hostgroup\thost_id\t\tstatus')
for (hostgroup, host_id, status) in cursor:
  print("{}\t\t{}\t{}".format(
    hostgroup, host_id, status))

cursor.close()
cnx.close()

exit()
