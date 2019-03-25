import os
import xml.etree.ElementTree as ET

###Comment out the the code below to save the output to a file###
#import sys
#sys.stdout = open('log.txt', 'w')

for myfile in os.listdir(os.getcwd()+".\\input"):
    if myfile[-5:] == ".dtsx":
        print "\n\n" + myfile
        tree = ET.parse(".\\input\\" + myfile)
        root = tree.getroot()
        dictConn = {}
        for x in root:
            if x.tag == "{www.microsoft.com/SqlServer/Dts}ConnectionManagers":
                for y in x.getchildren():
                    dictConn[y.attrib['{www.microsoft.com/SqlServer/Dts}refId']] = y.attrib['{www.microsoft.com/SqlServer/Dts}DTSID']
        for x in root:
            if x.tag == "{www.microsoft.com/SqlServer/Dts}Executables":
                for y in x.getchildren():
                    if 'Microsoft.SqlServer.Dts.Tasks.ExecuteSQLTask.ExecuteSQLTask' in y.attrib['{www.microsoft.com/SqlServer/Dts}ExecutableType']:
                        elle2 = (varie for z in y.getchildren() for k in z.getchildren() for sqltask in y.getchildren() \
                                 if '{www.microsoft.com/SqlServer/Dts}ObjectData' in sqltask.tag for varie in sqltask.getchildren())
                        for varie in elle2:
                            db = dictConn.keys()[dictConn.values().index(varie.attrib['{www.microsoft.com/sqlserver/dts/tasks/sqltask}Connection'])]
                            print "\n\n\n"
                            print "[SQL TASK]     " + y.attrib['{www.microsoft.com/SqlServer/Dts}refId']
                            print "------------------------------------------------------------------------------------"
                            print varie.attrib['{www.microsoft.com/sqlserver/dts/tasks/sqltask}SqlStatementSource'] + ""
                            print "------------------------------------------------------------------------------------"
                            print "[CONNECTION]   " + db + "\n"
                    elif 'SSIS.Pipeline.3' in y.attrib['{www.microsoft.com/SqlServer/Dts}ExecutableType']:
                        connectionsss = []
                        conn_count = 0
                        elle = (l for z in y.getchildren() for k in z.getchildren() for g in k.getchildren() for h in g.getchildren() \
                            for j in h.getchildren() for l in j.getchildren())
                        query_pump = "***The table has been imported as a whole***"
                        for connne in elle:
                            if 'connectionManagerRefId' in connne.attrib:
                                conn_count += 1
                                connectionsss.append(connne.attrib['connectionManagerRefId'])
                            #print connne.attrib

                            if 'SqlCommand' == connne.attrib['name']:
                                if connne.text is not None:
                                    query_pump = connne.text
                                
                        print "\n\n\n"
                        print "[DATA PUMP TASK]      " + y.attrib['{www.microsoft.com/SqlServer/Dts}refId']
                        print "------------------------------------------------------------------------------------"
                        print query_pump
                        print "------------------------------------------------------------------------------------"
                        print "[INPUT CONNECTION]    " + connectionsss[1]
                        print "[OUTPUT CONNECTION]   " + connectionsss[0] + "\n"