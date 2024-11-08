# Importerar socket och threading till programmet.
import socket
import threading
#-------------------------------------------------------------------------------------------------------------------------
# Här definieras värden för port och host så att klienten senare kan ansluta till denna unika adress.
# Även Format och Header har definerats för att underlätta hanteringen av data i programmet.
HOST = '127.0.0.1'
PORT =  50007
FULLADDR = HOST,PORT
FORMAT = "utf-8"
HEADER = 512
#-------------------------------------------------------------------------------------------------------------------------
# Här skappas en TCP-klient.
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# en tom closed variabel och en input för namn som kommer användas senare för att skicka sitt namn i meddelanden samt kunna stänga ner programmet.
closed = ''
name = input('Whats youre username: ')
#-------------------------------------------------------------------------------------------------------------------------

# Funktionen som är till för att skriva för att antingen logga ut eller skicka ett medelande till andra klienter.
def write():
    # Skapar en while true loop där användaren får skriva in något i sin chatt. loopen använder try och execpt för felhantering.
    # Om klient inte skriver Q kommer antingen ett medelande med användarens namn att skickas till servern men om klienten skrev Q...
    # kommer klienten att skicka ett medelande som säger att klienten har lämnat, ändra på closed variabeln och sedan bryta loopen.  
    global closed 
    while True: 
        try:
            chatt =input('')
            if chatt == 'Q':
                print('you left the chatt')
                quitmessage = f'{name} left the chatt'
                client.send(quitmessage.encode(FORMAT))
                closed= 'Closedown'
                break
            else:
                message = f'{name}: {chatt}'
                client.send(message.encode(FORMAT))
        except:
            closed = 'Closedown'
            break

# Denna funktion letar efter medelanden från andra klienter. Innan funkitonen startar väntar funktionen allitd 1 sekund innan den sätter igång med while loopen.
# Anledningen till att ha en settimeout är för att den inet ska krocka med koden så att användaren behöver vänta på att någon skriver för att avsluta sitt programm.
def lookformessage():
    client.settimeout(1)
    # Här startar annars loopen där den kollar att medelandet inte är tom, är den det brytter den loopen för att inte "läsa" ett tomt medelande.
    # Annars printas det medelande som klienten fått.  
    # Här har även programmet kollat att efter varje sekund om klienten har stängt chatten med Q, har den gjort detta så bryts loopen och klienten slutar lyssna på medelanden. 
    while True:
        try:
            crypted_message = client.recv(HEADER)
            if not crypted_message:
                break
            else:
                message= crypted_message.decode(FORMAT)
                print(message)
                break
        except socket.timeout:
            global closed
            if closed == 'Closedown':
                break

# Detta är funktionen som faktiskt är till för att klienten ska kunna läsa. 
def read():
    # Som förväntat, startar programmet med en while loop. Har användaren skrivit Q i chatten så stängs loopen, annars kommer den aktivt leta efter medelanden
    # Även en simpel exception som skulle brytta loopen, skriva ett felmedelande och stännga ner kleinten med en client.close.
    while True:
        try:
            global closed
            if closed == 'Closedown':
                break
            else:
                lookformessage()
        except:
            print('Something is wrong with the messages, stoping now')
            client.close()
            break


# Här startar själva programmet
# Först connectar klienten till servern, får ett simpelt medelande om hur de kan avsluta och sedan startas alla 2 trådar så att klienten kan skriva och läsa samtidigt.
# Skulle ett fel uppstå så kommer en exception printa ut ett felmedelande.
try:
    client.connect(FULLADDR)
    print('you can quite any time by wrighting Q')
    writting=threading.Thread(target=write)
    reading=threading.Thread(target=read)
    writting.start()
    reading.start()

    writting.join()
    reading.join()
except: 
    print('something went wrong, please try starting again.')
#-------------------------------------------------------------------------------------------------------------------------










