##############################
# DECORADORES. 
##############################


def decorador_insertar(func):
    def envoltura(*args):
        file=open("logfile.txt","a")
        if args:
            for i in args:
                word=str(i)+" "
                file.write(word)
        file.write('\n')
                
        file.close()    
    return envoltura   

