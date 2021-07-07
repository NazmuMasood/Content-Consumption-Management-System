from repository import Repository
from models import Consumable

print('Seeding data...')

book1 = 'To Kill A Mockingbird'
book2 = 'Harry Potter - Deathly Hallows'
book3 = 'The Alchemist'
book4 = 'Farenheit 451'

movie1 = 'The Spiderman'
movie2 = 'Hugo'
movie3 = 'Narnia'
movie4 = 'Author Spiderwick'

series1 = 'Prison Break'
series2 = 'Dirilis Ertugrul'

consum_names = [book1,book2,book3,book4,movie1,movie2,movie3,movie4,series1,series2]

consum_art_types = {book1:'book',book2:'book', book3:'book', book4:'book', 
                    movie1:'movie', movie2:'movie', 
                    movie3:'movie', movie4:'movie',
                    series1:'series', series2:'series'} 

consum_start_dates = {book1:'2010-11-11',book2:'2019-7-1'}

consum_end_dates = {book1:'2010-11-21'}

consum_time_hrs = {book1:10,book2:4}

consum_ratings = {book1:9.5, book2:9}

consum_days = {book1:9, book2:4}

consumables = []
for consum_name in consum_names:
    consumable = Consumable()
    consumable.art_type = consum_art_types[consum_name]
    consumable.name = consum_name
    if consum_name in consum_start_dates:
        consumable.start_date = consum_start_dates[consum_name]
    if consum_name in consum_end_dates:
        consumable.end_date = consum_end_dates[consum_name]
    if consum_name in consum_time_hrs:
        consumable.consum_time_hrs = consum_time_hrs[consum_name]
    if consum_name in consum_ratings:
        consumable.rating = consum_ratings[consum_name]
    if consum_name in consum_days:
        consumable.consum_days = consum_days[consum_name]
    consumables.append(consumable)

Repository.createAll(consumables)
print('Data seeding successful ')

