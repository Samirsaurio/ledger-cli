from distutils.command.clean import clean
import typer
app = typer.Typer()
from colorama import Fore
from colorama import Style
#import datetime



class Register:
    date = ""
    companyName = ""
    branches = [] #Tupla<List<Branch>, Double>
    amount = 0.0


"""""
    def __init__(self, date, companyName, transaction):
        self.date = date
        self.companyName = companyName
        self.transaction = transaction
"""""

def getDate(strline): 
    """
    Get the date and show it with the ledger format
    """
    if strline.startswith("2"):
            year = strline[2:4]
            month = strline[5:7]
            day = strline[8:10]
            formatyear = f"{year}-{mts(month)}-{day}"
            return formatyear 

def getTransactionName(strline): 
    """
    Get the name of the whole movement
    """
    if strline.startswith("2"):
        switch = False
        words = []
        for l in strline:
            if l in allowed and l != " ":
                switch = True
            if switch == True:
                words.append(l)
        tname = ''.join(words).strip("\n") 
        return tname
        

#A list of allowed characters for the Transaction Name
allowed = ["-", " ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ":",
"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", 
"m", "n", "o", "p", "q", "r", "s", "t", "u", 
"v", "w", "x", "y", "z"]

#A list of allowed characters for the amounts of money
numberAllowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]

#Translates numbers to months strings, example = 01 = January = Jan
def mts(month: str):
    if month == "01":
        return "Jan"
    if month == "02":
        return "Feb"
    if month == "03":
        return "Mar"
    if month == "04":
        return "Apr"
    if month == "05":
        return "May"
    if month == "06":
        return "Jun"
    if month == "12":
        return "Dec"


@app.command() #This command print the file without comments
def print(f: typer.FileText = typer.Option(...)):
    for line in f:
        strline = str(line)
        if strline.startswith(";") or strline.startswith("=") or strline.startswith("  ;") or strline.startswith("end") or strline.startswith("apply") or strline.startswith("\n"):
            pass
        elif strline.startswith("2"):
            typer.echo(strline)
        else: 
            strlinesplit = strline.split(";")
            strline = ''.join(strlinesplit[0])
            typer.echo(strline)


@app.command()
def register(f: typer.FileText = typer.Option(...)):
    listTransactions = []
    sum = 0.0
    auxheader = ""

    register = Register()
    for line in f:
        aux = 0.0
        strline = str(line)
        #If the line is a comment, do not use it
        if strline.startswith(";") or strline.startswith("=") or strline.startswith("  (") or strline.startswith("  ;") or strline.startswith("end") or strline.startswith("apply") or strline.startswith("\n"):
            pass
        #If the line starts with 2 it means is a date
        elif strline.startswith("2"):
            register.date = getDate(strline)
            register.companyName = getTransactionName(strline)
            pass
        else: #Otherwise, the line is an Asset or Expense or any other movement

            strlinesplit = strline.split(";")
            strline = ''.join(strlinesplit[0])
            refactorLine = [] #This is the line without comments with ; on the right
            refactorLineNumbers = [] #Same for numbers

            
            for l in strline: #This for saves the amounts of money and the movements strings in two different lists
                
                if l in allowed and l != "-":
                    refactorLine.append(l)
                elif l in numberAllowed:
                    refactorLineNumbers.append(l)
                    
            if not refactorLineNumbers: #If the line does not have an amount of money let the default be zero
                refactorLineNumbers.append("0.0")

            cleanLine = ''.join(refactorLine) #Convert that line(list) to a string
            cleanLineNumber = ''.join(refactorLineNumbers) #Same for numbers
            cleanLine = cleanLine.strip(" ") #Delete useless spaces at string
            floatCleanLineNumber = float(cleanLineNumber) #Converts the string to a float type

            if floatCleanLineNumber == 0.0:
                floatCleanLineNumber = sum*-1
                sum = 0
            else:
                sum = sum + floatCleanLineNumber
                aux = sum

            register.amount = floatCleanLineNumber
            register.branches = cleanLine.strip(" ").strip("\n").split(":") #Delete other useless characters
            refactorLine = [] #Reboots the list
            refactorLineNumbers = []

            header = register.date + register.companyName
            
            if header != auxheader:
                typer.echo(f"{register.date} {Style.BRIGHT}{register.companyName}{Style.RESET_ALL}")
                auxheader = header
            else:
                pass
            typer.echo(f"{' '*30}{Fore.MAGENTA}{'%-32s' %cleanLine}", nl=False)
            typer.echo(f"{Fore.WHITE if floatCleanLineNumber > 0 else Fore.RED}${'%-10s' %floatCleanLineNumber}${aux}{Style.RESET_ALL}")
            
        listTransactions.append(register)
    
    #for i, reg in enumerate(listTransactions):
    #    typer.echo(listTransactions[i].date)




if __name__== "__main__":
    app()
