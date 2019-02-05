#  This code uses historical price data from Yahoo! Finance and rewrites
#       the .csv files into a .txt file format
#
#  To use this code, change the file extension from .txt to .py
#   Note that this code is written in python 2.7, but can 
#   easily be converted to python 3 if needed
#
#  Then at the command line, enter: 
#       python Convert_Stock_Data.py
#
#  Note that the columns in the output are:
#
#  Decimal Date; Open; High; Low; Close; Adjusted Close; Analog Date; Volume
#

import sys 
import getopt
import write_stock_data
                                        
def main(argv=None):

    data_file = open('Stocks_List.txt', 'r')

    j_file=0
    for line in data_file:
        j_file += 1

    data_file.close()

    data_file = open('Stocks_List.txt', 'r')

    print('')
    print('Stock or ETF Data Downloads: ')

    j=0
    for line in data_file:
        j+=1
        items = line.strip().split(',')
    #
    #   percent_complete = 100.0*float(j)/float(j_file) 
    #   print '     Percent File Completed: ', "{0:.2f}".format(percent_complete),'%', "                                 \r",   

    #
    #   Both variables below are string variables
    #

        etf_name                = items[0]

        etf_output_file = etf_name + '.txt'

        print(etf_name, '(#', j, 'of ', j_file, ')')

#
        write_stock_data.get_etf(etf_output_file,etf_name)
#
    data_file.close()
    print('')
#

if __name__ == "__main__": 
	sys.exit(main())

