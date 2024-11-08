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
# Här skappas en TCP-server och binder sedan servern till en adress (FULLADDR) så att klienter senare kan ansluta.
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(FULLADDR)

# En lista över alla klienter. När en klient ansluter, läggs de till i listan.
# När de kopplar från tas de bort från listan.
all_clients= []

#-------------------------------------------------------------------------------------------------------------------------
# Första funktionen som hanterar själva klienten när de är inne på i chattrummet. 
# Här kommer funktionen att försöka läsa inkomande medelande, Hantera utloggningar, skicka medelanden och felhantera programmet.
def handle_clients(conn, addr):

    # Ett inloggningsmedelande i servern och en bool som säger att klienten är inne på servern med True.
    print(f'New conection from following adress: {addr}')
    inserver = True

    # Startar en While loop sålänge klienten är inne i servern
    while inserver:

        # Kollar om servern fått ett medelande från klienten, och hanterar vad som ska göras beroende på vad servern fått in.
        #   Blir det något fel så stängs while loopen.
        try:
            message_coded = conn.recv(HEADER)
            # Om klienten skulle lämna chatten genom att stänga ner progremmt kommer det finnas ett tomt medelande. 
            # Denna del hanterar det tomma medelandet och stänger ner while loopen för denna klient. 
            if not message_coded:
                inserver = False
            # Här kollar programmet vad klienten har valt att skriva. 
            # Om det är Q stängs while loopen, annars används send_message_to_clients för att skicka medelandet till alla andra klienter. 
            message_decoded = message_coded.decode(FORMAT)
            if message_decoded == 'Q':
                print(f'{addr} left the chatt')
                inserver = False
            else:
                send_message_to_clients(message_coded, conn)
        except:
            inserver = False  

    # Först kopplas klienten bort från servern. Sen tas klienten bort från klient listan om de finns kvar där.
    conn.close()
    if conn in all_clients:
        all_clients.remove(conn)
    print(f'Connection from {addr} closed')

# Funktionen som hanterar att skicka klientens medelandet till andra klienter.
# Här kollar programmet i en forloop att programmet tar alla klienter förutom klienten som skickat medelandet själv och förösker skicka deras medelande till de andra utplockade klienterna.
# Skulle inte det funka kommer klienten tas bort från klientlistan och även bli disconnectade.
def send_message_to_clients(message_coded, self_conn):
    for aclient in all_clients:
        if aclient != self_conn:
            try:
                aclient.send(message_coded)
            except:
                aclient.close()
                all_clients.remove(aclient)

# Funktionen som sätter igång servern och lyssnar efter anslutningar från klienter. 
def start_server():
    server.listen() 
    print("Server listening for connections...")   
    try:
        # startar en while loop 
        while True:
            # Accepterar en inkommande anslutning och lägger till den i listan över klienter
            conn, addr = server.accept()
            all_clients.append(conn)
            
            # Startar en ny tråd för att hantera den anslutna klienten
            getclient = threading.Thread(target=handle_clients, args=(conn, addr))
            getclient.start()
    except:
        print('Servern kan inte starta.')



# Simpel try som sätter igång programmet eller printar att något gick fel om det inte skulle funka.  
try:
    start_server()
except:
    print('Servern cant connect')
#-------------------------------------------------------------------------------------------------------------------------