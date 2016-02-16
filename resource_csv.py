import os
import csv
import datetime


class ResourceWriteCSV():

    def createCSVFileNode(self, csvdir, data_w,):
        now = datetime.datetime.now()
        filename_node = csvdir + '/r_data-' + ".csv"
        date_write = now.strftime("%d%m%Y%H%M")

        if os.path.exists(filename_node) is False:

                try:
                    record = open(filename_node, 'w+')
                    writer = csv.writer(record, delimiter=',',
                                    quoting=csv.QUOTE_ALL)
                    writer.writerow(['date', 'node', 'total_nodes',
                                 'total_cores', 'total_mem', 'used_cores',
                                 'used_mem', 'free_cores', 'free_mem',
                                 'ts', 'tm', 'tl', 'txl', 'txxl',
                                 'others'])
                    for i in data_w:
                        writer.writerow(
                                        [date_write, i.get('node_name'),
                                         i.get('node_count'), i.get('nac'),
                                         i.get('nam'), i.get('nuc'),
                                         i.get('num'), i.get('nfc'),
                                         i.get('nfm'), i.get('t_s'),
                                         i.get('t_m'), i.get('t_l'),
                                         i.get('t_xl'), i.get('t_xxl'),
                                         i.get('oth')]
                                        )
                except IOError, e:
                    print "File Error" % e
                    raise SystemExit
        else:
            with open(filename_node, 'a') as w:
                writer = csv.writer(w, delimiter=',',
                                    quoting=csv.QUOTE_ALL)
                for i in data_w:
                    writer.writerow(
                                    [date_write, i.get('node_name'),
                                    i.get('node_count'), i.get('nac'),
                                    i.get('nam'), i.get('nuc'),
                                    i.get('num'), i.get('nfc'),
                                    i.get('nfm'), i.get('t_s'),
                                    i.get('t_m'), i.get('t_l'),
                                    i.get('t_xl'), i.get('t_xxl'),
                                    i.get('oth')]
                                        )

    def createCSVFileCloud(self, csvdir, data_w,):
        now = datetime.datetime.now()
        filename_all = csvdir + '/all_data-' + ".csv"
        date_write = now.strftime("%d%m%Y%H%M")

        if os.path.exists(filename_all) is False:

                try:
                    record = open(filename_all, 'w+')
                    writer = csv.writer(record, delimiter=',',
                                    quoting=csv.QUOTE_ALL)
                    writer.writerow(['date', 'total_nodes',
                                 'total_cores', 'total_mem', 'used_cores',
                                 'used_mem', 'free_cores', 'free_mem',
                                 'ts', 'tm', 'tl', 'txl', 'txxl',
                                 'others'])

                    writer.writerow(
                                    [date_write,
                                     data_w.get('total_nodes'),
                                     data_w.get('total_cores'),
                                     data_w.get('total_mem'),
                                     data_w.get('used_cores'),
                                     data_w.get('used_mem'),
                                     data_w.get('free_cores'),
                                     data_w.get('free_mem'),
                                     data_w.get('total_small'),
                                     data_w.get('total_medium'),
                                     data_w.get('total_large'),
                                     data_w.get('total_xl'),
                                     data_w.get('total_xxl'),
                                     data_w.get('oth')]
                                        )
                except IOError, e:
                    print "File Error" % e
                    raise SystemExit
        else:
            with open(filename_all, 'a') as w:
                writer = csv.writer(w, delimiter=',',
                                    quoting=csv.QUOTE_ALL)

                writer.writerow([date_write,
                                 data_w.get('total_nodes'),
                                 data_w.get('total_cores'),
                                 data_w.get('total_mem'),
                                 data_w.get('used_cores'),
                                 data_w.get('used_mem'),
                                 data_w.get('free_cores'),
                                 data_w.get('free_mem'),
                                 data_w.get('total_small'),
                                 data_w.get('total_medium'),
                                 data_w.get('total_large'),
                                 data_w.get('total_xl'),
                                 data_w.get('total_xxl'),
                                 data_w.get('oth')]
                                )
