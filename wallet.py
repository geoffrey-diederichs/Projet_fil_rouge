import os
import sys
import hashlib
import datetime
import getpass



def clear():

    os.system('cls' if os.name == 'nt' else 'clear')


def open_user(user_mail, user_pw):

    fichier = open("users.txt", "r")
    contenu = fichier.read().split("\n")
    contenu = contenu[1:len(contenu)]
    fichier.close()

    hash = hashlib.sha1(user_pw.encode("utf-8")).hexdigest()

    for i in range(0, len(contenu)):
        if user_mail == contenu[i].split(";")[0]:
            if hash == contenu[i].split(";")[1]:
                return i

    return "fail"


def find_user(user_mail):

    fichier = open("users.txt", "r")
    contenu = fichier.read().split("\n")
    contenu = contenu[1:len(contenu)]
    fichier.close()
    

    for i in range(0, len(contenu)):
        if user_mail == contenu[i].split(";")[0]:
            return i

    return "fail"


def create_user(user_mail, user_pw):

    hash = hashlib.sha1(user_pw.encode("utf-8")).hexdigest()

    fichier = open("users.txt", "a")
    fichier.write("\n"+user_mail+";"+hash+";"+"100"+";"+str(datetime.datetime.now()))
    fichier.close()

    write_log(user_mail, "create user")


def open_wallet(user):

    fichier = open("users.txt", "r")
    contenu = fichier.read().split("\n")
    contenu = contenu[1:len(contenu)]
    fichier.close()

    return contenu[user].split(";")[2]


def write_wallet(user, founds):

    fichier = open("users.txt", "r")
    contenu = fichier.read().split("\n")
    contenu = contenu[1:len(contenu)]
    fichier.close()

    new_user = contenu[user].split(";")
    new_user[2] = str(int(new_user[2]) + founds)

    contenu[user] = ";".join(new_user)

    fichier = open("users.txt", "w")
    fichier.write("mail;password;wallet\n"+"\n".join(contenu))
    fichier.close()

    user_mail = contenu[user].split(";")[0]
    write_log(user_mail, "wallet "+str(founds)) 


def transfer_founds(user):

    clear()
    transfer_mail = input("What user do you wish to transfer founds to ? (Type 'exit' to exit)\nMail : ")
    if transfer_mail == "exit":
        return "fail"
    
    clear()

    transfer_user = find_user(transfer_mail)
    if transfer_user == "fail":
        while True:
            clear()
            print("Error ! User not found.")
            choice = input("1- Try again to transfer founds.\n2- Exit\n\nPlease enter 1 or 2 : ")
            if choice == "2":
                clear()
                return "fail"
            elif choice == "1":
                break
            print("\nError ! Please enter 1 or 2.")
    else:
        transfer_founds = input("How much do you wish to transfer to "+transfer_mail+" ?\nEnter a number : ")
        if int(transfer_founds) <= 0 :
            clear()
            print("Error ! Invalid amount.\n")
            return "fail"

        try:
            transfer_founds == int(transfer_founds)
            write_wallet(user, (-1)*int(transfer_founds))
            write_wallet(transfer_user, int(transfer_founds))
            return "done"
        except ValueError:
            print("Error ! Please Enter a number.")



def write_log(user_mail, action):

    fichier = open("log.txt", "a")
    fichier.write("\n"+str(datetime.datetime.now())+";"+user_mail+";"+action)
    fichier.close()


def user_admin():
    print("yo")


def menu():
    while True:

        clear()
        choice = input("WALLET\n\n1- Connect\n2- Create user\n\nPlease enter 1, 2 or 'exit' to leave : ")
        while True:
            if choice == "1" or choice == "2":
                break
            elif choice == "exit":
                clear()
                sys.exit()
            choice = input("Error ! Please Enter 1, 2 or exit to leave : ")
        
        if choice == "2":
            clear()
            while True:

                mail = input("Creating a new user.\nPlease enter an email or 'exit' to go back : ")
                if mail == "exit":
                    break

                signal = find_user(mail)
                if signal != "fail":
                    print("Sorry this mail is already used. Please enter another mail or 'exit' to go back.")
                else:
                    break
            

            if mail != "exit":
                pw = getpass.getpass("Please enter a password : ")
                clear()
                create_user(mail, pw)
                input("User "+mail+" created !\n\nPress enter to continue.")
                clear()

        elif choice == "1":
            while True:
                clear()
                user_mail = input("Mail : ")
                user_pw = getpass.getpass("Password : ")
                if user_mail == "admin" and user_pw == "admin":
                    clear()
                    user_admin()
                    break

                user = open_user(user_mail, user_pw)

                choice = ""
                try:
                    user == int(user)
                    break
                except ValueError:
                    clear()
                    print("Error ! Authentification failed.")
                    while True:
                        choice = input("1- Try again to log in\n2- Exit\n\nPlease enter 1 or 2 : ")
                        if choice == "2":
                            clear()
                            break
                        elif choice == "1":
                            break
                        clear()
                        print("Error ! Please enter 1 or 2.")

                if choice == "" or choice == "2":
                    break
            
            if choice != "2":
                write_log(user_mail, "connexion")
                wallet = open_wallet(user)

                while True:
                    clear()
                    print("You have "+wallet+" coins.")

                    choice = input("\n1- Transfer coins\n2- Exit\n\nEnter 1 or 2 : ")
                    if choice == "2":
                        clear()
                        write_log(user_mail, "disconnexion")
                        break
                    elif choice == "1":
                        signal = transfer_founds(user)
                        if signal == "fail":
                            input("Transaction cancelled.\n\nPlease press enter to continue.")
                        else:
                            wallet = open_wallet(user)
                        
                    
                    print("Error ! Please type in 1 or 2.")



clear()
menu()
