#Solicitar datos
#Validar datos
#Procesar datos
from datetime import datetime

dia=int(input("dia?"))
mes=int(input("mes?"))
any=int(input("any?"))
any_actual = datetime.now().year

#Validar datos
if any <= any_actual:
     if mes >=1 and mes<=12:
         if dia >=1 and dia<=31:
             if any_actual - any>16 and any_actual - any<65:
                 print("Puedes trabajar")
         else:
             print("Dia erroneo")
     else:
         print("Mes erroneo")
else:
    print("Any erroneo")