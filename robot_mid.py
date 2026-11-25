
from collections import deque

ROWS,COLS=10,10 #Διαστάσεις πλέγματος
EMPTY,OBST,ITEM=".","#","*" #Σύμβολα για κενό, εμπόδιο και αντικείμενο

#Η μέθοδος load_world φορτώνει τον κόσμο από ένα αρχείο κειμένου και επιστρέφει μια λίστα λιστών που αναπαριστούν το πλέγμα του κόσμου.
def load_world(path:str)->list[list[str]]:
    world=[]
    with open(path,"r",encoding="utf-8") as f:
        for line in f: #Διαβάζει κάθε γραμμή από το αρχείο.
            row=line.strip().split() #Αφαιρεί τα κενά από την αρχή και το τέλος της γραμμής και χωρίζει τη γραμμή σε λίστα συμβόλων.
            if row: #Ελέγχει αν η σειρά δεν είναι κενή.
                world.append(row) #Προσθέτει τη σειρά στο πλέγμα world.
                
    assert len(world)==ROWS and all(len(r)==COLS for r in world),"Λάθος διαστάσεις world.txt" #Ελέγχει αν οι διαστάσεις του πλέγματος είναι σωστές. Η assert αυτό που κάνει είναι ουσιαστικά να ελέγχει αν η συνθήκη είναι αληθής. 
    #Αν είναι ψευδής, τότε εμφανίζει το μήνυμα που έχουμε γράψει στο string.
    valid={EMPTY,OBST,ITEM} #Ορίζει τα έγκυρα σύμβολα.
    for r in world: #Ελέγχει αν όλα τα σύμβολα στο πλέγμα είναι έγκυρα.
        for s in r: #Ελέγχει κάθε σύμβολο στη σειρά.
            assert s in valid,f"Άκυρο σύμβολο:{s}" #Αν βρεθεί άκυρο σύμβολο, εμφανίζει σφάλμα.
            
    return world
#Μέσω της in_bounds ελέγχουμε αν οι συντεταγμένες βρίσκονται εντός των ορίων του πλέγματος. Αυτό που κάνει είναι να ελέγχει αν η γραμμή και η στήλη είναι εντός των ορίων.

def in_bounds(r:int,c:int)->bool:# Ελέγχει αν οι συντεταγμένες (r, c) βρίσκονται εντός των ορίων του πλέγματος.
    return 0<=r<ROWS and 0<=c<COLS #Επιστρέφει True αν οι συντεταγμένες είναι εντός των ορίων, αλλιώς επιστρέφει False.

    
    

 #This is the method that finds the neighbors of a node   
def neighbors(world, r, c): 
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]: 
        nr, nc = r+dr, c+dc #Υπολογίζει τις συντεταγμένες του γείτονα.
        if in_bounds(nr, nc) and world[nr][nc] != OBST: 
            yield nr, nc #Η yield επιστρέφει έναν γείτονα κάθε φορά που καλείται η συνάρτηση.


#This is the method that prints the world    
def print_world(world: list[list[str]], r: int, c: int) -> None: 
    for i in range(ROWS): 
        line = []  #Δημιουργεί μια κενή λίστα για την αποθήκευση των συμβόλων της τρέχουσας γραμμής.
        for j in range(COLS): #Επαναλαμβάνει για κάθε στήλη στην τρέχουσα γραμμή.
            line.append("R" if (i,j)==(r,c) else world[i][j]) #Η append προσθέτει το σύμβολο "R" στη λίστα line αν οι συντεταγμένες είναι ίσες με τις συντεταγμένες του ρομπότ (r, c).
        print(" ".join(line)) #Εκτυπωνει τη γραμμή, ενώ η join συνενώνει τα στοιχεία της λίστας line σε μια συμβολοσειρά με κενά ανάμεσά τους.
    print()
    

def reconstruct_path(parent,start,end):
    result=[] #Δημιουργεί μια κενή λίστα.
    
    current_node=end #Θέτει τον τρέχοντα κόμβο ίσο με τον κόμβο προορισμού (end).
    
    while current_node is not None: #Βροχός που συνεχίζει όσο ο τρέχων κόμβος δεν είναι None.
        result.append(current_node) #Προσθέτει τον τρέχοντα κόμβο στη λίστα αποτελεσμάτων.
        
        row,col=current_node 
        current_node=parent[row][col] #Θέτει τον τρέχοντα κόμβο ίσο με τον γονέα του.
        
    return result    
        
    


def bfs_path_to_nearest_item(world,start):
    
    
    queue=deque() #Δημιουργεί μιά ουρά
    queue.append(start) #Εκτελεί σημείο εκκίνησης.
    parent=[[None for i in range(COLS)] for i in range(ROWS)] 
    visited=[] #Δημιουργεί μια κενή λίστα για κάθε σημείο που έχει επισκεφθεί το ρομπότ.
    visited.append(start) #Αρχικοποιεί τη λίστα visited με την αρχική θέση (start).
    #Με λίγα λόγια, παίρνει ως όρισμα έναν κόσμο και το τρέχον σημέιο, όπου το ρομπότ επισκέπτεται και επιστρέφει το μονοπάτι προς το κοντινότερο σημείο που πρέπει να συλλέξει το ρομπότ.
    
    
    while(queue):
        current_pos=queue.popleft() #Αφαιρεί το πρώτο στοιχείο από την ουρά (queue).
        
        if(world[current_pos[0]][current_pos[1]]==ITEM): #Ελέγχει αν το τρέχον σημείο περιέχει κάποιο αντικείμενο.
            path=reconstruct_path(parent,start,current_pos) #Αλλιώς ξαναφτιάχνει την διαδρομή από την αρχική θέση μέχρι το τρέχον σημείο.
            
            path=path[::-1] #Αντιστρέφει τη λίστα για να έχει τη σωστή σειρά από την αρχή μέχρι το τέλος.
            
            del path[0] #Αφαιρεί το πρώτο στοιχείο της λίστας και μεταφέρει τα υπόλοιπα στοιχεία μια θέση προς τα αριστερά.
            
            return path #Επιστρέφει τη διαδρομή προς το κοντινότερο αντικείμενο.
            
        
        for row,column in neighbors(world,current_pos[0],current_pos[1]):
            if (row,column) not in visited: #Ελέγχει αν ο γείτονας δεν έχει επισκεφθεί ακόμα.
                visited.append((row,column)) #Προσθέτει τον γείτονα στη λίστα visited.
                queue.append((row,column)) #Προσθέτει τον γείτονα στην ουρά για μελλοντική επεξεργασία.
                parent[row][column]=current_pos #Καταγράφει τον τρέχοντα κόμβο ως "γείτονα" του γείτονα.
            
            
    
    
#This is the method that finds the next step by using the method bfs_path_to_nearest_item 
def next_step_bfs(world,pos):
    path=bfs_path_to_nearest_item(world,pos)
    return path[0] if path else pos
    
#This is the method that finds the next step by using the sweep method 

def next_step_sweep(world,r,c,direction):
    if direction==1 and c==COLS-1: #Ελέγχει αν η κατεύθυνση είναι προς τα δεξιά και αν η στήλη είναι η τελευταία στήλη.
        return (r+1 if r+1<ROWS else r,c,-1) #Επιστρέφει τις νέες συντεταγμένες και αλλάζει την κατεύθυνση προς τα αριστερά.
        
    if direction ==-1 and c==0: #Ελέγχει αν η κατεύθυνση είναι προς τα αριστερά και αν η στήλη είναι η πρώτη στήλη.
        return (r+1 if r+1<ROWS else r,c,1) #Επιστρέφει τις νέες συντεταγμένες και αλλάζει την κατεύθυνση προς τα δεξιά.
        
        
    return (r,c+direction,direction) #Επιστρέφει τις νέες συντεταγμένες με βάση την τρέχουσα κατεύθυνση.
    
def run(strategy="BFS",path="world.txt",verbose_every=10): #Εκτελεί το πρόγραμμα με τη δεδομένη στρατηγική και το αρχείο κόσμου.
    world=load_world(path) #Φορτώνει τον κόσμο από το αρχείο.
    r,c=0,0 #Αρχικές συντεταγμένες του ρομπότ.
    direction=1 #Αρχική κατεύθυνση προς τα δεξιά.
    score,steps=0,0 #Αρχικοποιεί το σκορ και τα βήματα.
    print("This is the initial state of the world!")
    print()
    print_world(world,r,c)#Εκτυπώνει την αρχική κατάσταση του κόσμου
    while steps<80: #Επαναλαμβάνει μέχρι να φτάσει τα 80 βήματα.
    
        if world[r][c]==ITEM: #Συνθήκη για συλλογή αντικειμένου.
            world[r][c]=EMPTY #Αντικαθιστά το αντικείμενο με κενό.
            score+=1 #Προσθέτει 1 στο σκορ.
            
        if not any(ITEM in row for row in world): #Ελέγχει αν δεν υπάρχουν άλλα αντικείμενα στον κόσμο.
            break #Τερματίζει τον βρόχο αν δεν υπάρχουν άλλα αντικείμενα.
            
        if strategy.upper()=="BFS": #Ελέγχει αν η στρατηγική είναι BFS.
           nr,nc=next_step_bfs(world,(r,c)) #Βρίσκει το επόμενο βήμα χρησιμοποιώντας τη μέθοδο BFS.
           r,c=(nr,nc) #Ενημερώνει τις συντεταγμένες του ρομπότ.
           
        else:
            r,c,direction=next_step_sweep(world,r,c,direction) #Βρίσκει το επόμενο βήμα χρησιμοποιώντας τη μέθοδο Sweep.
            
        steps+=1
        if verbose_every and steps % verbose_every ==0: #Ελέγχει αν πρέπει να εκτυπώσει την τρέχουσα κατάσταση.
            print(f"Steps{steps} | Pos =({r},{c}) | Score ={score} | Strat={strategy}") #Εκτυπώνει τα βήματα, τη θέση, το σκορ και τη στρατηγική.
            print_world(world,r,c) #Εκτυπώνει τον κόσμο με τη θέση του ρομπότ.
        print(f"Τελικό σκορ:{score},Βήματα:{steps},Στρατηγική:{strategy}") #Εκτυπώνει το τελικό αποτέλεσμα.
        
        

    
def main():

    print("Give the path of the file:") #Ζητάει από τον χρήστη να εισάγει το όνομα του αρχείου όπως ''world_001.txt''.
    path=input() # Διαβάζει το όνομα του αρχείου από την είσοδο του χρήστη.
    print("Give the strategy  you want to use:") #Ζητάει από τον χρήστη να εισάγει τη στρατηγική που θέλει να χρησιμοποιήσει (BFS ή SWEEP)
    strategy=input() # Διαβάζει τη στρατηγική από την είσοδο του χρήστη.
    
    run(strategy,path) #Επιλέγει τη στρατηγική και το αρχείο για να τρέξει το πρόγραμμα.
    
    
if __name__=="__main__": #Αν το αρχείο εκτελείται απευθείας, τότε καλεί τη συνάρτηση main().
    main()
    