import random


# Runge kutta 
def rungeKutta(t):

    h = 0.01
    to = 0
    Co = t
    tiempoEnfriamento = 0

    while Co >= 0:
        

        k1 = (0.025*to)-(0.5*Co)-(12.85)
        k2 = (0.025*(to+(h/2)))-(0.5*(Co+(h/2)*k1))-(12.85)
        k3 = (0.025*(to+(h/2)))-(0.5*(Co+(h/2)*k2))-(12.85)
        k4 = (0.025*(to+(h)))-(0.5*(Co+(h)*k3))-(12.85)

        to = to+h
        Co = Co+(h/6)*(k1+2*k2+2*k3+k4)

    
    tiempoEnfriamento = ((to*30)/60)

    return tiempoEnfriamento
        

# Funcion que establece a que hora se realiza el corte
def relojCorte(t): 

    """
    Minutos       P ()         P () Ac 
    4t minutos    0,20         0,20
    6t minutos    0,60         0,80
    8t minutos    0,20         1,00
    
    """

    rnd = round(random.random(),4)
    if rnd < 0.20:
        return 4*t
    elif rnd < 0.80:
        return 6*t
    else:
        return 8*t