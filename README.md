# LogSearch
A simple python program to search PBS scheduler accounting logs.

### Keywords:
`submitted`: will filter for only submitted jobs.  
`finished`: will filter for only finished jobs.  
`restarted`: will filter for only restarted jobs.  
`array jobs`: will filter for only array jobs.  

## Current Supported Commands
#### [Number]:
`keywords: [many]`
This command will return the number of jobs submitted/restarted/finished during a given time frame.

#### [Average]:
`keywords: [average]`
This command will return the average number of jobs submitted/restarted/finished during a given time frame.

#### [Last]:
`keywords: [last]`
This command will re-query the system for the last command asked.

## Timeframes:
This program has been designed with the hopes of give a nearly natural language experience which means you can use the phrase "2 days ago" to get the begining search date to two days before the current day.
**Note: last week defaults to searching only the entry for 7 days ago. In order to search all the records for the last week you will need to use one of the special words.**  


### Special words:
Using the words `"since" or "in"` will set the time frame end date to the current day.

### Examples of Valid Commands:
`how many jobs have been submitted in the last week`
`what is the average daily number of finished jobs in this last week`
`how many jobs restarted yesterday`
`how many array jobs were submitted 4 days ago`