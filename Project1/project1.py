import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == "__main__":

    with PdfPages("Project1_David_Grzan.pdf") as pdf:

        #SPX (GSPC.txt) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("GSPC.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for the SPX", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #VIX ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("VIX.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for the VIX", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #KO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("KO.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for Coca Cola", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #PEP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("PEP.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for Pepsi", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #TGT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("TGT.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for Target", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #WMT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("WMT.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for Walmart", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #F ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("F.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for Ford", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #GE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("GE.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for General Electric", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #CVX ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("CVX.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for Chevron", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig

        #COST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        with open("COST.txt") as tsv:
            for line in csv.reader(tsv,delimiter="\t"):
                time.append(float(line[0]))
                value.append(float(line[4]))
                
            for i in range(len(time)):
                if (i>252):
                    time12.append(time[i])
                    value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                if (i>63):
                    time3.append(time[i])
                    value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

            fig = plt.figure()
            plt.plot(time12,value12,"r",linewidth=0.5, label="12 month returns")
            plt.plot(time3,value3,"b",linewidth=0.5, label="3 month returns")
            plt.legend()
            plt.ylabel("Percent Return", weight = "light")
            plt.xlabel("Time (years)", weight = "light")
            plt.title("Trailing Returns for Costco", fontsize = 18, weight = "bold")

            plt.text(0.03,0.04,"Max Drawdown (12mo): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
            plt.text(0.03,0.02,"Max Drawdown (3mo): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
            pdf.savefig()
            plt.close()
        
        del time, value, time3, value3, time12, value12, fig


        #SPX VIX comparison ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        time = []
        value = []
        value12 = []
        time12 = []
        value3 = []
        time3 = []
        time2 = []
        value2 = []
        value122 = []
        time122 = []
        value32 = []
        time32 = []
        with open("GSPC.txt") as tsv:
            with open("VIX.txt") as tsv2:
                for line in csv.reader(tsv,delimiter="\t"):
                    time.append(float(line[0]))
                    value.append(float(line[4]))
                
                for i in range(len(time)):
                    if (i>252) and (time[i]>1990):
                        time12.append(time[i])
                        value12.append(((value[i]-value[i-252])/(value[i-252]))*100)
                    if (i>63) and (time[i]>1990):
                        time3.append(time[i])
                        value3.append(((value[i]-value[i-63])/(value[i-63]))*100)

                for line in csv.reader(tsv2,delimiter="\t"):
                    time2.append(float(line[0]))
                    value2.append(float(line[4]))
                
                for i in range(len(time2)):
                    if (i>252):
                        time122.append(time2[i])
                        value122.append(((value2[i]-value2[i-252])/(value2[i-252]))*100)
                    if (i>63):
                        time32.append(time2[i])
                        value32.append(((value2[i]-value2[i-63])/(value2[i-63]))*100)

                fig = plt.figure()
                plt.plot(time122,value122,"g",linewidth=0.5, label="VIX")
                plt.plot(time12,value12,"orange",linewidth=0.5, label="SPX")
                plt.legend()
                plt.ylabel("Percent Return", weight = "light")
                plt.xlabel("Time (years)", weight = "light")
                plt.title("SPX VIX Comparison for 12mo Trailing Returns", fontsize = 16, weight = "bold")
                
                plt.text(0.03,0.04,"Max Drawdown (SPIX): "+"{:.1f}".format(min(value12))+"%",transform=fig.transFigure,size=5,color="green")
                plt.text(0.03,0.02,"Max Drawdown (VIX): "+"{:.1f}".format(min(value122))+"%",transform=fig.transFigure,size=5,color="green")
                plt.text(0.15,0.7,"They are inversely related",transform=fig.transFigure,size=16,color="red")
                pdf.savefig()
                plt.close()

                del fig
                
                fig = plt.figure()
                plt.plot(time32,value32,"g",linewidth=0.5, label="VIX")
                plt.plot(time3,value3,"orange",linewidth=0.5, label="SPX")
                plt.legend()
                plt.ylabel("Percent Return", weight = "light")
                plt.xlabel("Time (years)", weight = "light")
                plt.title("SPX VIX Comparison for 3mo Trailing Returns", fontsize = 16, weight = "bold")
                
                plt.text(0.03,0.04,"Max Drawdown (SPX): "+"{:.1f}".format(min(value3))+"%",transform=fig.transFigure,size=5,color="green")
                plt.text(0.03,0.02,"Max Drawdown (VIX): "+"{:.1f}".format(min(value32))+"%",transform=fig.transFigure,size=5,color="green")
                plt.text(0.15,0.7,"They are inversely related",transform=fig.transFigure,size=16,color="red")
                pdf.savefig()
                plt.close()
                
                del time, value, time3, value3, time12, value12, fig
