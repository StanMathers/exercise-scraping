
def display_info():
    print('1. Scrape from website\n2. Truncade table\n0. Exit')
    
    
def ask_for_save(steamparsing_obj):
    while True:
        try:
            command = input('Do you want to save the information? y/n: ').lower()
            if command == 'y':
                steamparsing_obj.to_sql()
                print('Information was saved successfully')
                break
            elif command == 'n':
                break
            
        except ValueError:
            print('Invalid Value')
        except KeyboardInterrupt:
            break

def ask_for_trunc(steamparsing_obj):
    while True:
        try:
            command = input('Do you want to truncade records? y/n: ').lower()
            if command == 'y':
                steamparsing_obj.trunc_table()
                print('Information was deleted successfully')
                break
            elif command == 'n':
                break
            
        except ValueError:
            print('Invalid Value')
        except KeyboardInterrupt:
            break

