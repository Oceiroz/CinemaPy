import os
import string



###################################### MODULES ######################################

def main():
    #Data file paths
    global account_path
    account_path = "Accounts"
    global movie_path
    movie_path = "Movies"
    global room_path
    room_path = "Rooms"
    
    #find/create username for login
    global username
    some = menu()
    if some == 1:
        username = sign_in()
    elif some == 2:
        username = create_account()
    #finding account information
    with open(f"{account_path}\\{username}.txt") as f:
        lines = [line.rstrip() for line in f]
        global f_name
        f_name = lines[0]
        global l_name
        l_name = lines[1]
        global e_mail
        e_mail = lines[2]
        global password
        password = lines[3]
        global money
        money = lines[4]
        global movies_list
        global movie
        #creating list of booked movies
        movie = lines[5]
        movies_list = movie.split(", ", -1)
        #removing whitespace and grammar for cleaner list
            
        if movies_list[0] == "":
            movies_list.remove("")
        
        #finding staff bool 
        #this does not have a function, staff/user account is changed in file    
        global staff
        staff = lines[6]
        global booked_rooms
        booked_rooms = lines[7:10]
        #send account data to account_info
        account_info(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)  

def get_input(input_message, input_type):
    #function to get text inputs
    while(True):
        raw_input = input(f"\n{input_message}\n")
        try:
            user_input = input_type(raw_input)
            break
        except ValueError:
            print(f"Not a valid input.\n")
    return user_input

def get_choice(input_message, choices):
    #function to get preset choices
    while(True):
        
        for x, choice in enumerate(choices):
            print(f"\n{x+1} -> {choices[x]}")
            
        raw_input = input(f"\n{input_message}\n")
        try:
            user_input = int(raw_input)
            if user_input > len(choices) or user_input < 1:
                raise ValueError
            break
        except ValueError:
            print(f"Not a valid option. Pick a number from 1 to {len(choices)}.\n")
    return user_input



#################################### FILE HANDLING ######################################

def get_files(path):
    #opens specified folder
    #files names retrieved
    data_list = os.listdir(path)
    data_list_clean = []
    for x in (data_list):
        #files listed
        new_data_name = x.replace(".txt", "")
        data_list_clean.append(new_data_name)    
    
    #list returned
    return data_list_clean

def format_list(item_list):
    
    item = str(item_list).replace("[", "")
    item1 = item.replace("]", "")
    item2 = item1.replace("'", "")
    item3 = item2.strip()
    
    return item3

def with_open(item_choice, item_list, path):
    for x, item in enumerate(item_list):
        if item_choice == x+1:
            with open(f"{path}\\{item_list[x]}.txt") as f:
                lines = [line.rstrip() for line in f]
    return lines

def write_file(file_list, path, file_name):
    #file is opened
    file_create = open(f"{path}\\{file_name}.txt", "w")
    #content is overwritten
    for x, file in enumerate(file_list):
        file = f"{file_list[x]}\n"
        file_create.writelines(f"{file}")
    #file is closed and saved
    file_create.close()
    
def seat_option_format():
    seat_option_raw = get_input("what seat would you like:", str)
    seat_option1 = seat_option_raw.capitalize()
    seat_option2 = seat_option1.replace("", " ")
    seat_option_final = seat_option2.strip()
    return seat_option_final 

def format_booking(booking_index):
    booked_indexes1 = str(booking_index).split(", ")
    booked_indexes = []
    for y, booked_index1 in enumerate(booked_indexes1):
        booked_seat_formatted = format_list(booked_index1)
        booked_indexes.append(booked_seat_formatted)
    return booked_indexes

def save_account(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms):
    movies_list_new = format_list(movies_list)
    for x, booked_room in enumerate(booked_rooms):
        booked_rooms[x] = format_booking(booked_rooms[x])
        for y, booked_chair in enumerate(booked_rooms[x]):
            if booked_room[y] == "":
                booked_rooms[x].remove("")
    booked_room1 = format_list(booked_rooms[0])
    booked_room2 = format_list(booked_rooms[1])
    booked_room3 = format_list(booked_rooms[2])
    #account info is placed into a list
    account_file_content = [f_name, l_name, e_mail, password, money, movies_list_new, staff, booked_room1, booked_room2, booked_room3]
    #account file is opened
    write_file(account_file_content, account_path, username)

################################# ACCOUNT MANAGING ##################################

def menu():
    #initial screen to sign in or make account
    options = ["Sign-in", "Create Account"]
    sign_create = get_choice("What would you like to do:", options)
    return sign_create

def create_account():
    #username create
    while(True):
        username = get_input("Please enter a username. please not username cannot be more than 15 characters long", str)
        if len(username) > 15:
            print("your username is too long, please shorten it.")
        elif len(username) <= 15:
            break

    # first name create
    f_name = get_input("What is your first name?", str)
    # last name create
    l_name = get_input("What is your last name?", str)
    # email create
    while(True):
        valid = 0
        e_mail = get_input("Enter your E-mail", str)
        for x, char in enumerate(e_mail):
            if e_mail[x] == "@":
                valid += 1
            if e_mail[x] == ".":
                valid += 1
        if valid == 2:
            break
        elif valid != 2:
            print("E-Mail is not valid, ensure it has a valid domain and uses the @ symbol")
    # password create
    while(True):
        #password creation input
        print("The password must:\nBe 12 characters long\nContain 2 special characters (e.g. @, %, &, etc.)\nContain uppercase letters\nContain numbers\n")
        password = get_input("please input a password", str)
        #password checklist
        special_char = 0
        number = False
        upper = False
        #special character count
        for char in password:
            if char.isalnum() == False:
                special_char += 1
            elif char.isnumeric() == True:
                number = True
            elif char.isupper() == True:
                upper = True
        #password validation
        if len(password) < 12 :
            print("Password is not 12 characters, please try again\n")
        elif number == False:
            print("Password must contain numbers, please try again\n")
        elif upper == False:
            print("Password must contain uppercase letters, please try again\n")
        elif special_char < 2:
            print("Password must contain at least 2 special characters, please try again\n")
        elif len(password) >= 12 and special_char >= 2 and number == True and upper == True:
            break
    #password confirmation
    while(True):
        pin_confirm = get_input("please re-enter new password", str)
        if pin_confirm == password:
            print("Your password has been set.\n")
            print(f"Welcome, {username}\n")
            break
        else:
            print("New password does not match initial password. Please try again.\n")
    
    #account placeholders to prevent file errors.
    money = 0
    movies_list = ""
    staff = False
    booked_rooms = ""

    #account saving
    #gets all inputs
    #creates list
    account_file_content = [f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms]
    #creates new file with username input
    write_file(account_file_content, account_path, username)
    #returns username to access account_info
    return username

def sign_in():
    while(True):
        #getting account files
        account_list = get_files(account_path)
        #username input
        username = get_input("Please type in username:", str)
        #finding username
        for x, account in enumerate(account_list):
            if username == account_list[x]:
                account_found = True
                break
            else:
                account_found = False
            
        #reenter id if account not found        
        if account_found == False:
            options = ["Yes", "No"]
            re_find = get_choice("You may have typed in your username wrong, would you like to try again:", options)
            if re_find == 2:
                print("Please make an account")
                menu()
        else:
            break
      
    #opens file
    with open(f"{account_path}\\{username}.txt") as f:
        lines = [line.rstrip() for line in f]
        #gets password
        password = lines[3]
    while(True):
        #password input
        pin_input = get_input("Please type in password", str)
        #validates password
        if pin_input == password:
            break
        elif pin_input != password:
            print("You typed in the pin wrong. Please try again\n")
    
    #returns username for account_info
    return username 

def sign_out(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms):
    #confirms if user wants to sign out
    options = ["Yes", "No"]
    get_out = get_choice("Are you sure you would like to sign out:", options)
    if get_out == 1:
        save_account(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)
    elif get_out == 2:
        account_info()




################################## INITIAL MENU #####################################

def account_info(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms):
    #prints account names
    print(f"\nWelcome: {username}")
    
    #account options for users
    if staff == "False":
        options = ["Balance", "Add Money", "Remove Money", "Book Tickets", "Sign-out"]
        account_option = get_choice("Where would you like to go:", options)
        
        #balance view - sends money data to function
        if account_option == 1:
            account_balance(money)
        #deposit money - sends money data to function
        elif account_option == 2:
            deposit_money(money)
        #withdrawal money - sends money data to function
        elif account_option == 3:
            withdraw_money(money)
        #book a movie - sends money and movie list data to function
        elif account_option == 4:
            movie_book(money, movies_list, booked_rooms)
        #sign out - sends all data to be written to a file
        elif account_option == 5:  
            sign_out(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)
    
    #account options for staff        
    elif staff == "True":
        options = ["Change Movies", "Sign-out"]
        account_option = get_choice("Where would you like to go:", options)
        
        #sends staff to movie manger menu
        if account_option == 1:
            movie_choice()
        #sends data to sign out for file saving
        elif account_option == 2:
            sign_out(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)
    


################################## CUSTOMER MENUS ###################################

def account_balance(money):
    #shows account balance
    while(True):
        print("Your current balance is:\n")
        print(f"{round(float(money),2)}")
        
        #exit menu
        options = ["Yes", "No"]
        get_out = get_choice("Are you finished in this section?", options)
        if get_out == 1:
            break
    
    #sends user and data back to account info
    account_info(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)
             
def deposit_money(money):
    while(True):
        #add money
        amount = get_input("How much would you like to add", float)
        money = float(money) + amount
        print("Your total is now:\n", f"{money}")
        
        #exit menu
        options = ["Yes", "No"]
        get_out = get_choice("Are you finished in this section?", options)
        if get_out == 1:
            break
    
    #sends user and data back to account info
    account_info(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)
      
def withdraw_money(money):
    while(True):
        #remove money
        remove_amount = get_input("How much money would you like to withdraw", float)
        remove_money = float(money) - remove_amount
        
        #negative money validation
        if remove_money < 0:
            print("Money cannot be removed as you do not have enough in your account\n")
        #removing money
        elif remove_money >= 0:
            print("Money was succesfully withdrawn\n")
            money = remove_money
            print("Your total is now:", f"{money}")
        
        #exit menu
        options = ["Yes", "No"]
        get_out = get_choice("Are you finished in this section?", options)
        if get_out == 1:
            break
    
    #returns user and data to account info
    account_info(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)

def movie_book(money, movies_list, booked_rooms):
    while(True):
        #decision for what user wants to do with bookings
        book_options = ["View Booking", "Add Booking", "Remove Booking", "Exit"]
        book_choices = get_choice("What would you like to do:", book_options)
        
        
        movie_list = get_files(movie_path)
        room_list = get_files(room_path)
        
        #view the bookings andd seats
        if book_choices == 1:
            movie_no = get_choice("What booking would you like to view", movie_list)
            lines = with_open(movie_no, movie_list, movie_path)
            room_no = int(lines[2])
            if booked_rooms == [""]:
                booked_room = ""
                room_ascii(booked_room, room_no)
            elif booked_rooms != [""]:
                booked_room = format_booking(booked_rooms[room_no - 1])
                booked_rooms[room_no - 1] = booked_room
                room_ascii(booked_room, room_no)
        
        #create booking for movie    
        elif book_choices == 2:
            while(True):
                #get list of movies and make choices
                movie_choice = get_choice("What movie would you like to see?", movie_list)
                
                #checking if there is a value in the movie list
                if movies_list == []:
                    e_movie = False
                    m_movie = False
                
                #checking if the movie has already been booked
                #m_movie is a variable that changes with status of the movie existing in list and if they want to adjust the booking.
                #e_movie is a permnant variable that stays the same so that the movie is not appended twice.
                for movie in movies_list:              
                    if movie == movie_list[movie_choice - 1]:
                        m_movie = True
                        e_movie = True
                        break
                    elif movie != movie_list[movie_choice-1]:
                        m_movie = False
                        e_movie = False
                #notify if movie has been booked        
                if m_movie == True:
                    print("You have already booked this movie")
                    #ask user wether they would like to add more seats
                    option = ["Yes", "No"]
                    more_seats = get_choice("would you like to book more seats?", option)
                    if more_seats == 1:
                        m_movie = False
                
                if m_movie == False:
                    #finding movie in list of movies
                    lines = with_open(movie_choice, movie_list, movie_path)
                    cost = lines[1]
                    room_no = int(lines[2])
                    movie_name = lines[0]

                    if booked_rooms == [""]:
                        booked_room = ""

                    elif booked_rooms != [""]:
                        booked_room = format_booking(booked_rooms[room_no - 1])
                        booked_rooms[room_no - 1] = booked_room
                        if booked_room == [""]:
                            booked_room = ""

                    print(f"{movie_name} costs: {cost} per seat.\n")
                                    
                    seat_amount = get_input("How many seats would you like", int)
                                
                    lines2 = with_open(room_no, room_list, room_path)
                    rows = 10
                    columns = 10
                    booked_amount = int(lines2[2])
                                    
                    total_cost = seat_amount * float(cost)
                    available_seats = (rows*columns) - booked_amount
                    #validating user input and checking if they have the right amount of money
                    if seat_amount > available_seats:
                        print("you have added more seats than there are available")
                    elif total_cost > float(money):
                        print("you cannot afford this many movies")
                    elif total_cost <= float(money) and seat_amount <= available_seats and seat_amount > 0:
                        #removing users money
                        money = float(money) - total_cost
                        #adding movies to users list 
                        if e_movie == False:   
                            movies_list.append(movie_list[room_no - 1]) 
                        #take user to the room_booking
                        room_book(seat_amount, booked_room, room_no)
                        break
                    elif seat_amount <=0:
                        print("you cannot book a negative amount of seats")
              
                break

        elif book_choices == 3:
            #choice to confirm removal
            option = ["Yes", "No"]
            remove_confirm = get_choice("Are you sure you want to remove your bookings?", option)
            
            #choice for removing movie
            if remove_confirm == 1:
                
                movie_remove = get_choice("What movie would you like to remove?", movies_list)
                lines = with_open(movie_remove, movie_list, movie_path)
                room_id = int(lines[2])
                refund = float(lines[1])
                
                booked_room = format_booking(booked_rooms[room_id - 1])
                booked_rooms[room_id - 1] = booked_room
                option = ["Whole Movie", "Specific Seats"]
                movie_room = get_choice("What would you like to remove?", option)
                if movie_room == 1:
                    
                    lines2 = with_open(room_id, room_list, room_path)
                    all_bookings = lines2[1].split(", ")
                    y = 0
                    for room in booked_room:
                        print(f"room: {room}")
                        for booking in all_bookings:
                            if room == booking:
                                all_bookings.remove(booking)
                                booked_room.remove(room)
                                y += 1
                                break
                    seat_amount = int(lines2[2]) - y
                    total_refund = refund * y
                    money = float(money) + total_refund
                    room_save(lines2[0], all_bookings, seat_amount, room_id)  
                    
                elif movie_room == 2:
                    while(True):
                        #get amount of seats removed
                        remove_amount = get_input("how many seats would you like to remove?", int)
                        #validate remove amount with amount  of existing seats
                        x = 0
                        for room in booked_room:
                            x += 1
                        if remove_amount > x:
                            print("You have inputted more seats than you have already booked.\n")
                        elif remove_amount <= x:
                            total_refund = refund * remove_amount
                            money = float(money) + total_refund
                            break
                        elif remove_amount <= 0:
                            print("you cannot remove chairs in an amount below 1")
                    #go to room_remove
                    room_remove(remove_amount, booked_room, room_id)
                    
        elif book_choices == 4:
            #takes user out of booking and back to account info
            break
    
    #returns user and data back to account info
    account_info(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)




################################### STAFF MENUS ####################################

def movie_choice():
    while(True):
        #choice input for what staff would like to do with movies
        options = ["Add Movie", "Remove Movie", "Exit"]
        movie_option = get_choice("What would you like to do", options)
        if movie_option == 1:
            #allows staff to add movies
            add_movie()
        elif movie_option == 2:
            #allows staff to remove movies
            remove_movie()
        elif movie_option == 3:
            #allows staff to exit to go to account info
            break
    #sends staff and data back to account info
    account_info(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)

def add_movie():
    while(True):
        #confirms if staff want to add movie
        options = ["Yes", "No"]
        confirm = get_choice("Would you like to add a movie?", options)
        if confirm == 2:
            #returns staff to movie choices
            break
        
        #get movies title input
        movie_title = get_input("what is the title of the movie:", str)
        #decide the cost of the movie
        movie_cost = get_input("How much will a ticket cost:", float)
        #decide which room the movie goes in
        room_options = get_files(room_path)
        room = get_choice("what room is the movie going to be in", room_options)
        #creates list of movie info
        movie_file_content = [movie_title, movie_cost, room]
        #creates file for movie
        write_file(movie_file_content, movie_path, movie_title)
        
    #function call for movie editing menu    
    movie_choice()

def remove_movie():
    while(True):
        #confirms if staff wiah to remove a movie
        options = ["Yes", "No"]
        confirm = get_choice("Would you like to remove a movie?", options)
        if confirm == 2:
            #returns staff to movie editing
            break
        
        #default value for finding a movie
        movie_found = False
        #gets list of movies from Movies folder
        movie_list = get_files(movie_path)
        #decide which movie to remove
        movie_option = get_choice("What movie would you like to remove", movie_list)
        #finding movie
        for x, movie in enumerate(movie_list):
            if movie_option == x+1:
                os.remove(f"{movie_path}\\{movie}.txt")
                movie_found = True
        #warning for if movie is not found
        if movie_found == False:
            print("movie cannot be found")
    #returns staff to movie editing menu
    movie_choice()



#################################### CINEMA ROOMS ##################################

def room_ascii(booked_room, room_no):
    #import room data
    room_index = room_no - 1
    room_list = get_files(room_path)
    lines = with_open(room_no, room_list, room_path)
    booked_seat = lines[1]
    booked_seats = format_booking(booked_seat)

    #room sizes            
    seats = []
    seats_ascii = []
    rows = 10
    columns = 10
    seats_amount = rows*columns
    
    #creating room coordinates
    for x in range(rows):
        row = string.ascii_uppercase[x]
        for y in range(columns):
            seat = (f"{row} {y+1}")
            seats.append(seat)
            status = f"{row}{y+1}"
            seats_ascii.append(f"| {status} |")
            
    #replacing booked seats        
    for x, seat in enumerate(seats):
        seat = seats[x].replace(" ", "")
        for booked_seat in booked_seats:
            if booked_seat == seats[x]:
                seats_ascii[x] = f"|={seat}=|"
        for room in booked_room:
            if room == seats[x]:
                seats_ascii[x] = f"|#{seat}#|"
                
                
    print(f"----------------------------------------<[ {lines[0]} ]>----------------------------------------\n")
    print("# - Your Bookings")
    print("= - Booked Seat\n")
    print("-------------------------------------------<[ SCREEN ]>-------------------------------------------\n")
    #ascii cinema room
    for x in range(0, seats_amount, columns):
        formatted_seats = seats_ascii[x:x+columns]
        print(f"{formatted_seats}")
    
    return seats
        
def room_book(seat_amount, booked_room, room_no):
    #when user books a room start this
    room_index = int(room_no) - 1
    room_list = get_files(room_path)
    
    lines = with_open(room_no, room_list, room_path)
    booked_seat = lines[1]
    booked_seats = format_booking(booked_seat)
                    
    #shows room_ascii
    seats = room_ascii(booked_room, room_no)
    #ask user what seats they would like to take
    for i in range(seat_amount):
        #make user input seats 1 at a time to make listing easier
        while(True):
            seat_valid = True
            seat_exist = True
            seat_option = seat_option_format()
            
            #check if seat is already taken or bought by the user
            for seat in seats:
                if seat_option == seat:
                    seat_exist = True
                    break
                else:
                    seat_exist = False
                    
            if seat_exist == True:    
                for room in booked_room:
                    if seat_option == room:
                        your_booking = True
                        break
                    else:
                        your_booking = False
                    
                for seat in booked_seats:
                    if seat_option == seat and your_booking == True:
                        print("You have already booked this seat")
                        seat_valid = False       
                    elif seat_option == seat and your_booking == False:
                        print("Someone has already booked this seat")
                        seat_valid = False
                   
            else:
                print("The room you inputted either does not exist or an error occured.")
            
            if seat_valid == True:
                booked_seats.append(seat_option)
                #save seats to account
                format_book_room = format_list(booked_room)
                booked_room_list = format_booking(format_book_room)
                booked_room_list.append(seat_option)
                booked_room = booked_room_list
                booked_rooms[room_index] = booked_room
                break
    #save seats to room
    for x, seat in enumerate(booked_seats):
        seat_amount = x+1

    save_account(f_name, l_name, e_mail, password, money, movies_list, staff, booked_rooms)    
    room_save(lines[0], booked_seats, seat_amount, room_no)

def room_save(movie_title, booked_seats, seat_amount, room_no):
    new_seat = format_list(booked_seats)
    room_file_content = [movie_title, new_seat, seat_amount]
    #save file
    write_file(room_file_content, room_path, room_no)

def room_remove(remove_amount, booked_room, room_no):
    #remove from account and room
    #save
    #exit
    room_list = get_files(room_path)
        #for however many seats removed
    for x in range(0, remove_amount, 1):
        while(True):
            seats = room_ascii(booked_room, room_no)
            seat_exist = True
            #ask user what seat they would like to remove showing ascii
            seat_remove_list = []
            seat_option = seat_option_format()
            
            for seat in seats:
                if seat_option == seat:
                    seat_exist = True
                    break
                else:
                    seat_exist = False
                    
            #check if seat is already taken or bought by the user
            if seat_exist == True:
                for room in booked_room:
                    if seat_option == room:
                        your_booking = True
                        booked_room.remove(seat_option)
                        break
                    else:
                        your_booking = False
                        
                if your_booking == True:
                    
                    seat_remove_list.append(seat_option)
                    break
                
                elif your_booking == False:
                    print("You do not own this seat")
            else:
                print("The room you inputted either does not exist or an error occured.")
                    
               
        lines2 = with_open(room_no, room_list, room_path)
        all_bookings = lines2[1].split(", ")
        y = 0
        for remove in seat_remove_list:
            for booking in all_bookings:
                if remove == booking:
                    all_bookings.remove(booking)
                    y += 1
                    break
        seat_amount = int(lines2[2]) - remove_amount
        room_save(lines2[0], all_bookings, seat_amount, room_no)  

main()