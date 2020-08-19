# DAIN Studios - Data Engineering challenge
This is my solution repository for the DAIN data engineering challenge. The Data engineering challenge had two parts to it - Architecture and Pipeline. 


## Part - 1 Architecture

For the first part of the data engineering challenge, an Architecture for a recommender system was to be drafted that could cover all the requirements. You can find the architecture along with my detailed comments [here](https://github.com/rtspeaks360/dain-de-challenge/blob/rec_engine_architecture/RecommendationSystem.MD) or you can use the following command to initialize a server that hosts the target - RecommendationSystem.MD file.
```
> grip RecommendationSystem.MD
```

Make sure you have alredy gone through the setup process and have successfully installed the requirements before doing this.

## Part - 2 Pipeline

For the second part of the data engineering challenge we needed to analyse the logs from an IOT system and get the daily median values for all available sensors. The target data pipeline is encapsulated  within a command line application. 

The solution is served using the functionality in the module - `get_median` for the IOT Logs analyzer application

### Instructions for using the solution application
To set up the application on your machine
* Initialize a python 3 virtual environment in the working directory
  ```
  > virtualenv env -p python3
  ```
  And enter into the environment using `source env/bin/activate` command.
* Once in virtual environment, install the dependencies using `pip install -r requirements.txt`
* Now you can start interacting with the CMD application. Use `python main.py -h` to have a look at the help message and the description.
  <img src=''>
* Once you have an input JSONL log file, note that you can run the application to analyze the logs in two modes. `--mode full` and `--mode chunked`. In the full mode, the entire file is read into the memory at once. 
  ```
  > python main.py --mode full --input dain-challenge-data.jsonl
  ```
  Use this if you have a really small input file. In this case the memory used depends on the total size of the file.
* For larger input files it is better to use the `chunked` mode, where we read the data from the file in chunks, parse the data into pandas and compute medians by day. Through this approach at any given time, the data for only one date is stored into memory.
  ```
  > python main.py --mode chunked --input dain-challenge-data.jsonl
  ```
 In this case the memory used depends on the numebr of observations per day, and the memory used doesn't increase as the size of the file increases, assuming it has similar daily observations and has data for more dates.
  





