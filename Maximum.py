Maximo (A):
    if ALenght == 1:
        return A[0]
    
    else:
        Max = Maximo (A[0:(ALenght-1)])
        
        if Max < A[ALenght]:
            return A[ALenght]
        
        else:
            return Max