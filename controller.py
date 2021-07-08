from tabulate import tabulate
from repository import *
from models import Consumable
import datetime
import re

art_types = {'book':'Book', 'series':'Series', 'movie':'Movie'}

class Controller:
   
    @staticmethod
    ### --- Take a (new) Consumable input from user and save record in db
    def create(art_type):
        print('Adding a new '+art_type+'...')
        
        consumable = Controller.inputConsumAttrs(art_type)
        Repository.create(consumable=consumable)
        
        print(art_type+' added succesfully')

    @staticmethod
    ### --- Get all Consumable (for a type) and shows them in a table 
    def readAll(art_type):
        print('Fetching all '+art_type+'(s)...')

        consum_tuples = Repository.readAllUndeleted(art_type=art_type)

        print(str(len(consum_tuples))+' '+art_type+'(s) found'+'\n')
        consum_coll = {}
        table = []
        if len(consum_tuples)>0:
            consum_serial = 1
            for id, art_type, name, start_date, end_date, \
                    consum_time_hrs, rating, consum_days  in consum_tuples:
                table.append([consum_serial, name, consum_days, consum_time_hrs, rating])
                consum_coll[id] = name
                consum_serial+=1

        ## Showing BOOK / SERIES / MOVIE table
        print(Controller.getStarPadding() +' '+ art_types[art_type] +' List ' \
                + Controller.getStarPadding())
        print(tabulate(table, \
                    headers=['No.','Name', 'Total Consumption Days', 
                        'Total Consumption Hours', 'Rating'], 
                    tablefmt='pretty') )
        return consum_coll

    @staticmethod
    ### --- Get a specific Consumable and show its details in a table
    def readDetails(art_type, id, printDetails=True):
        if printDetails:
            print('Fetching the desired '+art_type+'...')

        consum_tuple = Repository.readById(id=id)

        table = []
        if consum_tuple:
            if printDetails:
                print('1 '+art_type+' found'+'\n')
            table.append([consum_tuple.name, consum_tuple.consum_days, consum_tuple.consum_time_hrs,
                 consum_tuple.rating, consum_tuple.start_date, consum_tuple.end_date ])
        else:
            print('No such record found')
        
        if printDetails:
            ## Showing a specific BOOK / SERIES / MOVIE's details
            print(Controller.getStarPadding() +' '+ art_types[art_type] +' Details ' \
                    + Controller.getStarPadding())
            print(tabulate(table, \
                        headers=['Name', 'Total Consumption Days', 'Total Consumption Hours',
                            'Rating', 'Starting Date', 'Ending Date'], 
                        tablefmt='pretty') )
        
        return consum_tuple

    @staticmethod
    ### --- Delete a Consumable i.e. update-> consumable.delete = True
    def delete(art_type, id):
        print('Deleting a '+art_type+'...')
        
        Repository.deleteById(id=id)
        
        print('Selected '+art_type+' deleted succesfully')
 
    @staticmethod
    ### --- Edit a Consumable and update it into db
    def edit(consumable):
        print('<<< Editing '+consumable.art_type+': '+consumable.name+ ' >>>')

        validTime = False
        while not validTime:
            time = input('i. Add more consumption time (in hours): ')
            if not time:
                time = 0
                break
            else:
                # if bool(re.match(r'^\d+(\.\d+)?$', time)):
                #     time = round(float(time), 2)
                #     break
                if bool(re.match(r'^0$|[1-9]\d*$', time)):
                    time = int(time)
                    break
                elif bool(re.match(r'^\d+(\.\d+)?$', time)):
                    print('Please enter a whole number of hours (e.g. 1,5,..)')
                else:
                    print('Please enter a valid amount of hours')        

        validNumOfDays = False
        while not validNumOfDays:
            numOfDays = input('ii. Add more consumption days: ')
            if not numOfDays:
                numOfDays = 0
                break
            else:
                if bool(re.match(r'^0$|[1-9]\d*$', numOfDays)):
                    numOfDays = int(numOfDays)
                    break
                else:
                    print('Please enter a valid number of days')

        validRating = False
        while not validRating:
            rating = input('iii. Update rating: ')
            if not rating:
                break
            else:
                if bool(re.match(r'[0-9]*(\.[0-9]{1,2})?$', rating)):
                    rating = round(float(rating), 2)
                    if rating <= 10:
                        break
                    else:
                        print('Rating cannot be greater than 10')
                else:
                    print('Please enter a valid amount of rating (e.g. 9, 9.5, 9.75)')

        validEndDate = False
        while not validEndDate:
            end_date = input('iv. Consumption Ending date (YYYY-MM-DD): ')
            if not end_date:
                break
            else:
                try:
                    datetime.datetime.strptime(end_date, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Incorrect data format, should be YYYY-MM-DD")        

        # Updating the Consumable object/record
        consumable.consum_time_hrs = consumable.consum_time_hrs + time
        consumable.consum_days = consumable.consum_days + numOfDays
        if rating:
            consumable.rating = rating
        if end_date:
            consumable.end_date = end_date

        Repository.update(consumable)
        print('Updated '+consumable.art_type+" '"+consumable.name+"' successfully")

    @staticmethod
    ### Below method (when invoked) takes from User, all the valid.. 
    ### ..attribute values (e.g. Name, Start Day, Rating..) of a Consumable..
    ### ..and returns a Consumable object/record
    def inputConsumAttrs(art_type):
        validName = False
        while not validName:
            name = input('i. Name: ').strip()
            if name:
                break
            else:
                print(art_type+' name cannot be empty')

        validStartDate = False
        while not validStartDate:
            start_date = input('ii. Consumption Starting date (YYYY-MM-DD): ')
            if not start_date:
                break
            else:
                try:
                    datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Incorrect data format, should be YYYY-MM-DD")
                    # raise ValueError("Incorrect data format, should be YYYY-MM-DD")

        validEndDate = False
        while not validEndDate:
            end_date = input('iii. Consumption Ending date (YYYY-MM-DD): ')
            if not end_date:
                break
            else:
                try:
                    datetime.datetime.strptime(end_date, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Incorrect data format, should be YYYY-MM-DD")

        validTime = False
        while not validTime:
            time = input('iv. Total consumption time (in hours): ')
            if not time:
                time = 0
                break
            else:
                # if bool(re.match(r'^\d+(\.\d+)?$', time)):
                #     time = round(float(time), 2)
                #     break
                if bool(re.match(r'^0$|[1-9]\d*$', time)):
                    time = int(time)
                    break
                elif bool(re.match(r'^\d+(\.\d+)?$', time)):
                    print('Please enter a whole number of hours (e.g. 1,5,..)')
                else:
                    print('Please enter a valid amount of hours')

        validRating = False
        while not validRating:
            rating = input('v. Rate the '+art_type+' (out of 10): ')
            if not rating:
                break
            else:
                if bool(re.match(r'[0-9]*(\.[0-9]{1,2})?$', rating)):
                    rating = round(float(rating), 2)
                    if rating <= 10:
                        break
                    else:
                        print('Rating cannot be greater than 10')
                else:
                    print('Please enter a valid amount of rating (e.g. 9, 9.5, 9.75)')

        validNumOfDays = False
        while not validNumOfDays:
            numOfDays = input('vi. Total days of consumption: ')
            if not numOfDays:
                numOfDays = 0
                break
            else:
                if bool(re.match(r'^0$|[1-9]\d*$', numOfDays)):
                    numOfDays = int(numOfDays)
                    break
                else:
                    print('Please enter a valid number of days')

        # Creating the Consumable object/record
        consumable = Consumable()
        consumable.art_type = art_type
        consumable.name = name
        if start_date:
            consumable.start_date = start_date
        if end_date:
            consumable.end_date = end_date
        consumable.consum_time_hrs = time
        if rating:
            consumable.rating = rating
        consumable.consum_days = numOfDays
        return consumable

    @staticmethod
    ### Below method displays to an user 'a list of options' to choose from.. 
    ### ..and returns user's selected option
    def selectFromDict(options, option_type, printOptions=True):
        if printOptions:
            print('Select a/an ' + option_type + ':')
        index = 1
        indexValidList = []
        for optionName in options:
            if printOptions:
                print(str(index) + ') ' + options[optionName])
            indexValidList.extend([optionName])
            index+=1
        inputValid = False
        while not inputValid:
            inputRaw = input(option_type + ' no. : ')
            if not inputRaw or not bool(re.match(r'^0$|[1-9]\d*$', inputRaw)):
                print('Please select a valid ' + option_type + ' number')
                continue
            inputNo = int(inputRaw) - 1
            if inputNo > -1 and inputNo < len(indexValidList):
                selected = indexValidList[inputNo]
                print('Selected ' + option_type + ': ' + options[selected])
                print('-------------------') 
                inputValid = True
                break
            else:
                print('Please select a valid ' + option_type + ' number')
        return selected

    @staticmethod
    def getStarPadding():
        return '**********************************'
        # return '* * * * * * * * * * * * * * * * * *'


    