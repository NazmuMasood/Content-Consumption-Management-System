from controller import Controller
import re

# -- Greeting the user
print('\n- - - '+' WELCOME TO ART CONSUMPTION MANAGEMENT SYSTEM ' \
                + ' - - -\n')

### -- Prompting main options to user
base_options = {'create':'Add a consumable', 'edit':'Edit a consumable', 
                'delete':'Delete a consumable', 
                'read_all':'See the list of consumables (and individually)', 
                'read_overall':'See overall info'}
base_option = Controller.selectFromDict(base_options, 'option')

### -- Prompting art types to user to choose
art_types = {'book':'Book', 'series':'Series', 'movie':'Movie'}
art_type = Controller.selectFromDict(art_types, 'art type')

### --------------- 'Add a consumable' -------------------
if base_option == 'create':
    Controller.create(art_type)


### --------------- 'See the list of consumables' -------------------
if base_option == 'read_all':
    ## -- Showing a list of consumables (of desired type) to user
    consum_coll = Controller.readAll(art_type)

    ### --------------- 'See full details of a consumable' -------------------    
    ## -- Prompting user to select a consumable/art_item from list to see more details
    if(len(consum_coll)>0): 
        print('Select a '+art_type+' to see more details')
        consumable_id = Controller.selectFromDict(consum_coll, art_type, printOptions=False)
        print(art_type+' id: '+str(consumable_id))
        Controller.readDetails(art_type, consumable_id)


### --------------- 'Delete a consumable' -------------------
if base_option == 'delete':
    ## -- Showing a list of consumables (of desired type) to user
    consum_coll = Controller.readAll(art_type)
    ## -- Prompting user to select a consumable/art_item from list to delete
    if(len(consum_coll)>0): 
        print('Select a '+art_type+' to delete')
        consumable_id = Controller.selectFromDict(consum_coll, art_type, printOptions=False)
        print(art_type+' id: '+str(consumable_id))
        Controller.delete(art_type, consumable_id)
    else:
        print('There is no '+art_type+' available to delete')


### --------------- 'Edit a consumable' -------------------
if base_option == 'edit':
    ## -- Showing a list of consumables (of desired type) to user
    consum_coll = Controller.readAll(art_type)
    ## -- Prompting user to select a consumable/art_item from list to edit
    if(len(consum_coll)>0): 
        print('Select a '+art_type+' to edit')
        activeConsum = False
        while not activeConsum:
            consumable_id = Controller.selectFromDict(consum_coll, art_type, printOptions=False)
            print(art_type+' id: '+str(consumable_id))

            consumable = Controller.readDetails(art_type, consumable_id, printDetails=False)
            if consumable.end_date:
                print('Cannot edit selected '+art_type+' since its consumption already ended')
                continue
            else:
                break
        
        Controller.edit(consumable)
    else:
        print('There is no '+art_type+' available to edit')



