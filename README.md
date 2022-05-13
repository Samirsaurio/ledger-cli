# ledger-cli implemented with python

This is a smaller implementation of the ledger-cli using python.


You will need two python libraries: 
+ ```pip3 install typer```
+ ```pip3 install colorama```

The first step is have both drewr3.dat and ledger.py in the same directory.


## COMMANDS
This implementations supports two commands:
+ print: Print the full file and transaction without comments, just the needed information.
+ register: To show all transactions and a running total

## ARGUMENTS
--f: Write the name of your file next to it so it can be opened and read by ledger.py

## USAGE
```python3 ledger.py [command] --f [filename]```
