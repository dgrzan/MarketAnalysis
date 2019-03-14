import csv
import dateutil
import dateutil.parser
import urllib

#   Example:
#       Ticker = 'SPY'
#       filename = Ticker + '.txt'

def get_etf(filename, Ticker):
    data = {}
    
    #------------------------------------------------------------------
    #
    #   We assume data is form Yahoo Finance and is in the format of
    #   Ticker.csv, where "Ticker" is the ticker symbol for the stock or ETF

       #
       # Open the stream and account for the header

    input_file = Ticker + '.csv'
    data_stream = open(input_file,"r")

#
       # Parse the data
       
    j=-1
    for row in csv.reader(data_stream):
        j += 1
        if j>0: 
            date = dateutil.parser.parse(row[0])
            key = date.strftime('%Y/%m/%d')
#           print row[:]
            if key not in data:
                if '-' not in row[1:5] and 0 not in map(float,row[1:5]):
                    row[0] = date.year+int(date.strftime('%j'),10)/365.0
                    row[5] = float(row[5])
                    data[key] = str(row[0]) + '\t' + str(row[1]) + '\t' +str(row[2]) + '\t' +str(row[3]) + \
                            '\t' +str(row[4]) + '\t' +str(row[5]) + '\t' + str(key) + '\t' +str(row[6])
    #------------------------------------------------------------------#
   # Write output to file --------------------------------------------#
    with open(filename, 'w') as output:
        for key in sorted(data.keys()):
            output.write("%s\n" % data[key])

   #------------------------------------------------------------------#
    return None

if __name__ == "__main__":
    filename = 'GSPC.txt'
    Ticker = 'GSPC'
    get_etf(filename, Ticker)
