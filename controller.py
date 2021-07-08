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
        
        consumable = Controller.inputConsumCreateAttrs(art_type)
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
    def readDetailsById(art_type, id, printDetails=True):
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

        consumableUpdt = Controller.inputConsumEditAttrs(consumable)
        Repository.update(consumableUpdt)
        print('Updated '+consumable.art_type+" '"+consumable.name+"' successfully")


    @staticmethod
    ### --- Edit a Consumable and update it into db
    def readOverall():
        print('Fetching overall info...')

        consumables = Repository.readAll()
        return consumables


    ### --- Generates overall report
    @staticmethod
    def generateReport(consumables):
        # --------- Calculating values for across each type
        consum_time_hrs_by_type = {}
        consum_days_by_type = {}
        consum_rating_by_type = {}
        count_rated_consumable_by_type = {}
        consumable_count_by_type = {}

        for consumable in consumables:
            # -- Generating dict for each type's consum_timer_hrs
            if consumable.art_type in consum_time_hrs_by_type:
                consum_time_hrs_by_type[consumable.art_type] = \
                    consum_time_hrs_by_type[consumable.art_type] + consumable.consum_time_hrs
            else:
                consum_time_hrs_by_type[consumable.art_type] = consumable.consum_time_hrs

            # -- Generating dict for each type's consum_days
            if consumable.art_type in consum_days_by_type:
                consum_days_by_type[consumable.art_type] = \
                    consum_days_by_type[consumable.art_type] + consumable.consum_days
            else:
                consum_days_by_type[consumable.art_type] = consumable.consum_days

            # -- Generating dict for each type of cosumable's ratings
            if consumable.rating:
                if consumable.art_type in consum_rating_by_type:
                    consum_rating_by_type[consumable.art_type] = \
                        consum_rating_by_type[consumable.art_type] + consumable.rating
                else:
                    consum_rating_by_type[consumable.art_type] = consumable.rating
                # -- Generating dict for counting each type of rated consumables
                if consumable.art_type in count_rated_consumable_by_type:
                    count_rated_consumable_by_type[consumable.art_type] = \
                        count_rated_consumable_by_type[consumable.art_type] + 1
                else:
                    count_rated_consumable_by_type[consumable.art_type] = 1

            # -- Generating dict for each type of consumable count
            if consumable.art_type in consumable_count_by_type:
                consumable_count_by_type[consumable.art_type] = consumable_count_by_type[consumable.art_type]+1
            else:
                consumable_count_by_type[consumable.art_type] = 1

        # print(consum_time_hrs_by_type)
        # print(consum_days_by_type)
        # print(consum_rating_by_type)
        # print(count_rated_consumable_by_type)
        # print(consumable_count_by_type)


        # -------- Calculating the values for across all types        
        sum_all_type_consum_time_hrs = sum([consumable.consum_time_hrs for consumable in consumables])            
        
        sum_all_type_consum_days = sum([consumable.consum_days for consumable in consumables])
        
        all_valid_consum_rating_list = []
        for consumable in consumables:
            if consumable.rating:
                all_valid_consum_rating_list.append(consumable.rating)
        avg_all_type_consum_rating = round(float(sum(all_valid_consum_rating_list)) 
                                        / max(len(all_valid_consum_rating_list), 1), 2)
        
        count_all_type_consumable = len(consumables)


        # -- Printing overall info in table
        table = []
        for art_type in art_types:
            if art_type not in consum_time_hrs_by_type:
                consum_time_hrs_by_type[art_type] = '-'
            if art_type not in consum_days_by_type:
                consum_days_by_type[art_type] = '-'
            if art_type not in consum_rating_by_type:
                consum_rating_by_type[art_type] = '-'
            if art_type not in consumable_count_by_type:
                consumable_count_by_type[art_type] = 0

            avg_current_type_consum_rating = '-'  
            if consum_rating_by_type[art_type] != '-':
                avg_current_type_consum_rating = \
                    float(consum_rating_by_type[art_type]) / count_rated_consumable_by_type[art_type]
            table.append([art_type, 
                        consum_time_hrs_by_type[art_type],
                        consum_days_by_type[art_type],
                        avg_current_type_consum_rating,
                        consumable_count_by_type[art_type]])    
        
        table.append(['Total',
                    sum_all_type_consum_time_hrs,
                    sum_all_type_consum_days,
                    avg_all_type_consum_rating,
                    count_all_type_consumable])

        print(tabulate(table, \
                        headers=['Art Type', 'Total Consumption Hours', 'Total Consumption Days',
                            'Rating', 'Count'], 
                        tablefmt='grid'), )
        

    @staticmethod
    ### Below method (when invoked) takes from User, the valid 'update'.. 
    ### ..attribute values (e.g. Time, Days, Rating, End Date) of a Consumable..
    ### ..and returns an updated Consumable object/record
    def inputConsumEditAttrs(consumable):
        # Taking Consumable 'consum_time_hrs' input and checking validity
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

        # Taking Consumable 'consum_days' input and checking validity
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

        # Taking Consumable 'rating' input and checking validity
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

        # Taking Consumable 'end_date' input and checking validity
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
        
        return consumable


    @staticmethod
    ### Below method (when invoked) takes from User, all the valid.. 
    ### ..attribute values (e.g. Name, Start Day, Rating..) of a Consumable..
    ### ..and returns a Consumable object/record
    def inputConsumCreateAttrs(art_type):
        # Taking Consumable 'name' input and checking validity
        validName = False
        while not validName:
            name = input('i. Name: ').strip()
            if name:
                break
            else:
                print(art_type+' name cannot be empty')

        # Taking Consumable 'start_date' input and checking validity
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

        # Taking Consumable 'end_date' input and checking validity
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

        # Taking Consumable 'consum_time_hrs' input and checking validity
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

        # Taking Consumable 'rating' input and checking validity
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

        # Taking Consumable 'consum_days' input and checking validity
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


    # @staticmethod
    ### --- Get a specific Consumable and show its details in a table
    # def readDetailsByObj(consumable):
    #     table = []
    #     if consumable:
    #         table.append([consumable.name, consumable.consum_days, consumable.consum_time_hrs,
    #              consumable.rating, consumable.start_date, consumable.end_date ])
    #     else:
    #         print('Record not valid')
        
    #     ## Showing a specific BOOK / SERIES / MOVIE's details
    #     print(Controller.getStarPadding() +' '+ art_types[consumable.art_type] +' Details ' \
    #             + Controller.getStarPadding())
    #     print(tabulate(table, \
    #                 headers=['Name', 'Total Consumption Days', 'Total Consumption Hours',
    #                     'Rating', 'Starting Date', 'Ending Date'], 
    #                 tablefmt='pretty') )
    
