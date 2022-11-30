class Sujeto:
    observadores=[]
    
    def agregar(self,obj):
        self.observadores.append(obj)
        
    def notificar(self,*args):
        if(args):
            for observador in self.observadores:
                observador.update(args)
            print(self.observadores)    
    
           
    
        
class Observador:
    def update(self):
        raise NotImplementedError("delegacion de actualizacion")
    
class ConcreteObserver(Observador):
    def __init__(self,obj):
        self.observado_a=obj
        self.observado_a.agregar(self)
    
    def update(self,*args):
        print("actualizacion dentro del observador" , args)
        
    