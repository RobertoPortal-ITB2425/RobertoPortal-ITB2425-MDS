"""
Solicita un mes y un any y calcula el numero de dias en ese mes
"""
try:
    mes=int(input("mes?"))
    if mes >=1 and mes <=12:
        if mes in(12,10,8,7,5,3,1):
            print("31")
        elif mes in (11,9,6,4):
            print("30")
        else: #Febrero
            #any bisiesto?
            year = int(input("any?"))
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                print("29")
            else:
                print("28")
    else:
        print("ERROR mes no valido")
except ValueError:
    print("Intente otra vez")