from position import Position

class Allocation():
    def __init__(self, positions, totalValue, allocation = None):
        if allocation is None:
            self.portion = {}
            total = 0
            for position in positions:
                div = position.open_value() / totalValue
                self.portion[position] = div
                total += div
            self.portion['cash'] = 1 - total
        else:
            self.portion = allocation.portion
    
    def edit(self):

        total = 0
    
        print(f'Current allocation\n\n{self.toString():>5}\n')
        # the key is a position object
        for position in self.portion:
            amount = None
            if type(position) is str:
                amount = 1 - total
                self.portion[position] = amount
                break

            print(f'Enter new allocation for {position.symbol} (%)')
            while amount is None:
                amount = input(' > ')
                try:
                    amount = float(amount)/100
                    if amount > 1 or total + amount > 1:
                        print('Can\'t be bigger than 1!')
                        amount = None
                    elif amount < 0:
                        print('Can\'t be negative')
                        amount = None
                    else:
                        total += amount
                except:
                    print('Enter a number!')
                    amount = None
            self.portion[position] = amount
        return '\nNew Allocation\n\n' + self.toString()
            

    def toString(self):
        return '\n'.join([f'{key.symbol:>8}: {self.portion[key]*100:.2f}%' if type(key) is not str else f'{key:>8}: {self.portion[key]*100:.2f}%' for key in self.portion])