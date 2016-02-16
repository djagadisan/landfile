import os
import csv
import datetime


class WriteCSV():

    def createCSVFile(self, csvdir, data):
        now = datetime.datetime.now()
        #filename = csvdir + '/allocation-' + now.strftime("%d%m%y%H") + ".csv"
        filename = csvdir + '/volume_report.csv'

        if os.path.exists(filename) is False:
            try:
                record = open(filename, 'w+')
                writer = csv.writer(record, delimiter=',',
                                    quoting=csv.QUOTE_ALL)
                writer.writerow(['Project Name', 'Volumes Allocated',
                                 'Volumes Used', 'Project Leader Name',
                                'Project Leader Email'])
                writer.writerow([data[0], data[1], data[2], data[3],
                                 data[4]])

            except IOError, e:
                print "File Error" % e
                raise SystemExit
        else:
            with open(filename, 'a') as w:
                writer = csv.writer(w, delimiter=',',
                                    quoting=csv.QUOTE_ALL)
                writer.writerow([data[0], data[1], data[2], data[3],
                                 data[4]])
