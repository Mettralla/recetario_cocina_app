class Ingredient():
    '''La clase representa a un ingrediente individual
        params:
            (str) name: nombre del ingrediente
            (int) amount: cantidad del ingrediente
            (str) metric: la medida a usarse
    '''
    def __init__(self, name: str, amount: int, metric: str) -> None:
        self.name = name
        self.amount = amount
        self.metric = metric
        
    def get_name(self) -> str:
        '''Regresa el nombre del ingrediente'''
        return self.name
    
    def get_amount(self) -> str:
        '''Regresa las cantidades formateados en "cantidad medida"'''
        return f'{str(self.amount)} {self.metric}'