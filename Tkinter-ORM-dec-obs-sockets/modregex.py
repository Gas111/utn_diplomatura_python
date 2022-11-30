import re

class Textofiltro():
    
    def filtro_numero(self, datos):#este modulo fitra para detectar numeros en cantidad
        patron=re.compile(r'[0-9][0-9]{0,6}',re.X)
        resultado=patron.match(str(datos))
        return resultado
    
    def filtro_cadena(self,datos):#este modulo lo 
        patron=re.compile('^[A-Za-z]+(?:[ _-][A-Za-z]+)*$')
        resultado=patron.match(str(datos))
        return resultado