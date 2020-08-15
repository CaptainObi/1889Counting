class Player:
    def __init__(self, money, name):
        self.__stock = {'AR': 0, 'IR': 0, 'SR': 0, 'KO': 0, 'TR': 0, 'KU': 0, 'UR': 0}
        self.__money = money
        self.__privates = {20: False, 30: False, 40: False, 50: False, 60: False, 80: False, 150: False}
        self.__name = name
        self.__totalIncome = 0

    def adjust_money(self, adjustment):
        self.__money = self.__money + adjustment

    def return_money(self):
        return self.__money

    def adjust_stock(self, number, stock):
        self.__stock[stock] = self.__stock[stock] + number

    def return_stock(self, stock):
        return self.__stock[stock]

    def return_name(self):
        return self.__name
    
    def pay_out_privates(self, income):
        self.__totalIncome = 0
        for x in self.__privates:
            if self.__privates[x] == True:
                self.__money = self.__money + income[x]
                self.__totalIncome = self.__totalIncome + income[x]
        return self.__totalIncome
    
    def adjust_privates(self, private, change):
        self.__privates[private] = change

    def retrive_info(self):
        return [self.__name, self.__stock, self.__privates, self.__money]

class Company:
    def __init__(self, money):
        self.__money = money
        self.__floated = False
        self.__stocks_owned = 0
        self.__pared = False
        self.__privates = {20: False, 30: False, 40: False, 50: False, 60: False, 80: False, 150: False}
        self.__totalIncome = 0

    def adjust_money(self, adjustment):
        self.__money = self.__money + adjustment

    def return_money(self):
        return self.__money

    def is_floated(self):
        return self.__floated

    def increase_stocks_owned(self, amount):
        self.__stocks_owned = self.__stocks_owned + amount
        if self.__stocks_owned >= 5:
            self.__floated = True
        return self.__floated
    
    def is_pared(self):
        return self.__pared

    def par(self):
        self.__pared = True

    def pay_out_privates(self, income):
        self.__totalIncome = 0
        for x in self.__privates:
            if self.__privates[x] == True:
                self.__money = self.__money + income[x]
                self.__totalIncome = self.__totalIncome + income[x]
        return self.__totalIncome

    def adjust_privates(self, private, change):
        self.__privates[private] == change
    
    def retrive_info(self):
        return [self.__money, self.__privates]

class Game:
    def __init__(self):
        self.__startingMoney = 0
        self.__gameOver = False
        self.__privateIncome = {20: 5, 30: 5, 40: 10, 50: 15, 60: 15, 80: 20, 150: 30}
        self.__activeCompanies = []
        self.__listOfPlayerObjects = 0
        self.__AR = Company(0)
        self.__IR = Company(0)
        self.__SR = Company(0)
        self.__KO = Company(0)
        self.__TR = Company(0)
        self.__KU = Company(0)
        self.__UR = Company(0)
        self.__companyReference = {'AR': self.__AR, 'IR': self.__IR, 'SR': self.__SR, 'KO': self.__KO, 'TR': self.__TR, 'KU': self.__KU, 'UR': self.__UR}
        self.__trainDefaultPrice = {'2': 80, '3': 180, '4': 300, '5': 450, '6': 630, 'D': 1100}
        self.__bank = 7000
        self.__valid = False
        self.setup()
        self.__priorityDeal = self.__listOfPlayerObjects[0]
        self.__firstPlayerToPass = 1
        self.__playersTurnNumber = 0
        self.__open_stock = {'AR': 0, 'IR': 0, 'SR': 0, 'KO': 0, 'TR': 0, 'KU': 0, 'UR': 0}
        self.__phase = 1
        self.terminal()
        self.gameLoop()

    def gameLoop(self):
        while self.__gameOver == False:
            if self.__phase == 1:
                self.stockRound()
                self.terminal()
                self.operatingRound()
                self.terminal()
            elif self.__phase == 3:
                self.stockRound()
                self.terminal()
                self.operatingRound()
                self.terminal()
                self.operatingRound()
                self.terminal()
            elif self.__phase == 5:
                self.stockRound()
                self.terminal()
                self.operatingRound()
                self.terminal()
                self.operatingRound()
                self.terminal()
                self.operatingRound()
                self.terminal()

    def setup(self):
        while not self.__valid:
            try:
                self.__numOfPlayers = int(input('How Many People Are Playing? '))
                if 6 >= self.__numOfPlayers >= 2:
                    self.__valid = True
                else:
                    print('Invalid Asnwer. Please pick a number of players between 2 and 6.')
            except ValueError:
                print('Invalid Asnwer. Please pick a number of players between 2 and 6.')
        if 4 >= self.__numOfPlayers >= 2:
            self.__startingMoney = 420
            self.__bank = self.__bank - 420*self.__numOfPlayers
        else:
            self.__startingMoney = 390
            self.__bank = self.__bank - 390*self.__numOfPlayers
        self.__playerOne = Player(self.__startingMoney, 'Player One')
        self.__playerTwo = Player(self.__startingMoney, 'Player Two')
        self.__playerThree = Player(self.__startingMoney, 'Player Three')
        self.__playerFour = Player(self.__startingMoney, 'Player Four')
        self.__playerFive = Player(self.__startingMoney, 'Player Five')
        self.__playerSix = Player(self.__startingMoney, 'Player Six')
        if self.__numOfPlayers == 2:
                self.__listOfPlayerObjects = [self.__playerOne, self.__playerTwo]
        elif self.__numOfPlayers == 3:
                self.__listOfPlayerObjects = [self.__playerOne, self.__playerTwo, self.__playerThree]
        elif self.__numOfPlayers == 4:
            self.__listOfPlayerObjects = [self.__playerOne, self.__playerTwo, self.__playerThree, self.__playerFour]
        elif self.__numOfPlayers == 5:
            self.__listOfPlayerObjects = [self.__playerOne, self.__playerTwo, self.__playerThree, self.__playerFour, self.__playerFive]
        elif self.__numOfPlayers == 6:
            self.__listOfPlayerObjects = [self.__playerOne, self.__playerTwo, self.__playerThree, self.__playerFour, self.__playerFive, self.__playerSix]

    def stockRound(self):
        self.__playersPassed = 0
        while self.__playersPassed != self.__numOfPlayers:
            self.__playersPlayed = 0
            self.__playersTurn = self.__priorityDeal
            while self.__playersPlayed != self.__numOfPlayers:
                if self.__playersPassed == self.__numOfPlayers:
                    break
                print(f'It is {str(self.__playersTurn.return_name())}\'s Turn \nThey have {self.__playersTurn.return_money()} Yen')
                self.__turnDone = False
                while not self.__turnDone:
                    self.__turnValid = False
                    while not self.__turnValid:
                        try:
                            self.__move = input('Please pick Buy, Sell, Done, Pass: ').lower()
                            if self.__move == 'pass' or self.__move == 'buy' or self.__move == 'done' or self.__move == 'sell':
                                self.__turnValid = True
                            else:
                                print('Invalid Asnwer. Please pick Buy, Sell, Done, Pass: ')
                        except ValueError:
                            print('Invalid Asnwer. Please pick Buy, Sell, Done, Pass: ')
                    if self.__move == 'pass':
                        if self.__playersPassed == 0:
                            self.__firstPlayerToPass = self.__playersTurnNumber
                        self.__playersPassed = self.__playersPassed + 1
                        self.__playersPlayed = self.__playersPlayed + 1
                        self.__turnDone = True
                        if self.__playersPassed == self.__numOfPlayers:
                            self.__playersTurnNumber = self.__firstPlayerToPass
                            self.__playersTurn = self.__listOfPlayerObjects[self.__firstPlayerToPass]
                            self.__priorityDeal = self.__listOfPlayerObjects[self.__firstPlayerToPass]
                        try:
                            self.__playersTurnNumber = self.__playersTurnNumber + 1
                            self.__playersTurn = self.__listOfPlayerObjects[self.__playersTurnNumber]
                        except IndexError:
                            self.__playersTurnNumber = 0
                            self.__playersTurn = self.__listOfPlayerObjects[0]
                    elif self.__move == 'done':
                        self.__turnDone = True
                        self.__playersPlayed = self.__playersPlayed + 1
                        self.__playersPassed = 0
                        try:
                            self.__playersTurnNumber = self.__playersTurnNumber + 1
                            self.__playersTurn = self.__listOfPlayerObjects[self.__playersTurnNumber]
                        except IndexError:
                            self.__playersTurnNumber = 0
                            self.__playersTurn = self.__listOfPlayerObjects[0]
                    elif self.__move == 'buy':
                        self.__stockValid = False
                        while not self.__stockValid:
                            self.__stockName = input('What stock? Enter Two Letter Code: ')
                            if self.__stockName == 'AR' or self.__stockName == 'IR' or self.__stockName == 'SR' or self.__stockName == 'KO' or self.__stockName == 'TR' or self.__stockName == 'KU' or self.__stockName == 'UR':
                                self.__stockValid = True
                            else:
                                print('Invalid Answer. Enter Two Letter Code: ')
                        if self.__companyReference[self.__stockName].is_floated() == False:
                            if self.__companyReference[self.__stockName].is_pared() == False:
                                self.__playersTurn.adjust_stock(2, self.__stockName)
                                self.__parValid = False
                                while not self.__parValid:
                                    try:
                                        self.__par = int(input('Please pick par, 100, 90, 80, 75, 70, 65: '))
                                        if self.__par == 100 or self.__par == 90 or self.__par == 80 or self.__par == 75 or self.__par == 70 or self.__par == 65:
                                            self.__parValid = True
                                        else:
                                            print('Invalid Asnwer. Please pick par, 100, 90, 80, 75, 70, 65.')
                                    except ValueError:
                                        print('Invalid Asnwer. Please pick par, 100, 90, 80, 75, 70, 65.')
                                self.__playersTurn.adjust_money(-2*self.__par)
                                self.__companyReference[self.__stockName].par()
                                self.__bank = self.__bank + 2*self.__par
                                self.__companyReference[self.__stockName].increase_stocks_owned(2)
                            else:
                                self.__playersTurn.adjust_stock(1, self.__stockName)
                                self.__priceValid = False
                                while not self.__priceValid:
                                    try:
                                        self.__price = int(input('Please input perchase price: '))
                                        if 10 <= self.__price <= 350:
                                            self.__priceValid = True
                                        else:
                                            print('Invalid Asnwer. Please input perchase price.')
                                    except ValueError:
                                        print('Invalid Asnwer. Please input perchase price lo')
                                self.__playersTurn.adjust_money(-1*self.__price)
                                self.__bank = self.__bank + self.__price
                                if self.__companyReference[self.__stockName].increase_stocks_owned(1):
                                    self.__companyReference[self.__stockName].adjust_money(10*self.__price)
                                    self.__bank = self.__bank + -10*self.__price
                                    self.__activeCompanies.append(self.__companyReference[self.__stockName])
                                    self.check_game_end()
                        else:
                            self.__playersTurn.adjust_stock(1, self.__stockName)
                            self.__priceValid = False
                            while not self.__priceValid:
                                try:
                                    self.__price = int(input('Please input perchase price: '))
                                    if 10 <= self.__price <= 350:
                                        self.__priceValid = True
                                    else:
                                        print('Invalid Asnwer. Please input perchase price: ')
                                except ValueError:
                                    print('Invalid Asnwer. Please input perchase price: ')
                            self.__playersTurn.adjust_money(-1*self.__price)
                            self.__bank = self.__bank + self.__price
                            self.__locationValid = False
                            while not self.__locationValid:
                                try:
                                    self.__location = input('Please input O for Open Market or IPO: ').lower()
                                    if self.__location == 'o' or self.__location == 'ipo':
                                        if self.__location == 'o' and self.__open_stock[self.__stockName] != 0:
                                            print('Invalid Asnwer. Please input O for Open Market or IPO:')
                                        else:
                                            self.__locationValid = True
                                    else:
                                        print('Invalid Asnwer. Please input O for Open Market or IPO: ')
                                except ValueError:
                                    print('Invalid Asnwer. Please input O for Open Market or IPO: ')
                            if self.__location == 'o':
                                self.__open_stock[self.__stockName] = self.__open_stock[self.__stockName] - 1
                    elif self.__move == 'sell':
                        self.__stockValid = False
                        while not self.__stockValid:
                            self.__stockName = input('What stock? Enter Two Letter Code: ')
                            if self.__stockName == 'AR' or self.__stockName == 'IR' or self.__stockName == 'SR' or self.__stockName == 'KO' or self.__stockName == 'TR' or self.__stockName == 'KU' or self.__stockName == 'UR':
                                self.__stockValid = True
                            else:
                                print('Invalid Answer. Enter Two Letter Code')
                        self.__stockNumValid = False
                        while not self.__stockNumValid:
                            try:
                                self.__numOfSharesSold = int(input('Please input number of stocks sold: '))
                                if 0 <= self.__numOfSharesSold <= self.__playersTurn.return_stock(self.__stockName):
                                    self.__stockNumValid = True
                                else:
                                    print('Invalid Asnwer. Please input number of stocks sold.')
                            except ValueError:
                                print('Invalid Asnwer. Please input number of stocks sold.')
                        self.__playersTurn.adjust_stock(-1*self.__numOfSharesSold, self.__stockName)
                        self.__open_stock[self.__stockName] = self.__open_stock[self.__stockName] + self.__numOfSharesSold
                        self.__priceValid = False
                        if self.__numOfSharesSold == 0:
                            break
                        while not self.__priceValid:
                            try:
                                self.__price = int(input('Please input current stock price: '))
                                if 10 <= self.__price <= 350:
                                    self.__priceValid = True
                                else:
                                    print('Invalid Asnwer. Please input current stock price.')
                            except ValueError:
                                print('Invalid Asnwer. Please input current stock price.')
                        self.__playersTurn.adjust_money(self.__numOfSharesSold*self.__price)
                        self.__bank = self.__bank - self.__price*self.__numOfSharesSold
                        self.check_game_end()

    def operatingRound(self):
        self.__companiesGone = []
        for i in self.__listOfPlayerObjects:
            self.__bank = self.__bank - i.pay_out_privates(self.__privateIncome)
            self.check_game_end()
        if self.__phase == 3:
            for i in self.__activeCompanies:
                self.__bank = self.__bank - i.pay_out_privates(self.__privateIncome)
                self.check_game_end()
        while len(self.__activeCompanies) != len(self.__companiesGone): 
            self.__comapnyValid = False
            while not self.__comapnyValid:
                self.__companyName = input('What company is next? Enter Two Letter Code: ')
                if self.__companyName == 'AR' or self.__companyName == 'IR' or self.__companyName == 'SR' or self.__companyName == 'KO' or self.__companyName == 'TR' or self.__companyName == 'KU' or self.__companyName == 'UR':
                    for y in self.__activeCompanies:
                        if y == self.__companyReference[self.__companyName]:
                            self.__comapnyValid = True
                        else:
                            print('Invalid Answer. Enter Two Letter Code: ')
                else:
                    print('Invalid Answer. Enter Two Letter Code: ')
            print(f'{self.__companyName} has {self.__companyReference[self.__companyName].return_money()}')
            self.__trackValid = False
            while not self.__trackValid:
                self.__trackCost = input('Is there a 80 Yen cost for the track lay? Y or N: ').lower()
                if 'y' == self.__trackCost or 'n' == self.__trackCost:
                    self.__trackValid = True
                else:
                    print('Invalid Asnwer. Y or N: ')
            if self.__trackCost == 'y':
                self.__bank = self.__bank + 80
                self.__companyReference[self.__companyName].adjust_money(-80)
            self.__tokenValid = False
            while not self.__tokenValid: 
                self.__tokenCost = input('Do you want to lay a token? Y or N: ').lower()
                if 'y' == self.__tokenCost or 'n' == self.__tokenCost:
                    self.__tokenValid = True
                else:
                    print('Invalid Asnwer. Y or N: ')
            if self.__tokenCost == 'y':
                self.__bank = self.__bank + 40
                self.__companyReference[self.__companyName].adjust_money(-40)
            self.__incomeValid = False
            while not self.__incomeValid:
                try:
                    self.__income = int(input('Input Income: '))
                    if self.__income >= 0:
                        self.__incomeValid = True
                    else:
                        print('Invalid Asnwer. Input Income: ')
                except ValueError:
                    print('Invalid Asnwer. Input Income: ')
            if self.__income == 0:
                pass
            else: 
                self.__dividendsValid = False
                while not self.__dividendsValid:
                    self.__dividends = input('Are you paying dividends? Y or N ').lower()
                    if self.__dividends == 'y' or self.__dividends == 'n':
                        self.__dividendsValid = True
                    else:
                        print('Invalid Asnwer. Input Income: ')
                if self.__dividends == 'n':
                    self.__bank = self.__bank - self.__income
                    self.check_game_end()
                    self.__companyReference[self.__companyName].adjust_money(self.__income)
                else:
                    for z in self.__listOfPlayerObjects:
                        self.__sharesOwned = z.return_stock(self.__companyName)
                        z.adjust_money(self.__sharesOwned*self.__income/10)
                        self.__bank = self.__bank - self.__income*self.__sharesOwned/10
                        self.check_game_end()
                        print(f'{z.return_name()} makes {self.__sharesOwned/10*self.__income}')
                    self.__companyReference[self.__companyName].adjust_money(self.__open_stock[self.__companyName]*self.__income/10)
                    self.__bank = self.__bank - self.__income*self.__open_stock[self.__companyName]/10
                    self.check_game_end()
            self.__trainValid = False
            while not self.__trainValid: 
                self.__trainBuy = input('Do you want to buy a train? Y or N: ').lower()
                if 'y' == self.__trainBuy or 'n' == self.__trainBuy:
                    self.__trainValid = True
                else:
                    print('Invalid Asnwer. Y or N: ')
            if self.__trainBuy == 'y':
                self.__trainOriginValid = False
                while not self.__trainOriginValid: 
                    self.__trainOrigin = input('Where do you want to buy a train from? C for other company or B from bank: ').lower()
                    if 'c' == self.__trainOrigin or 'b' == self.__trainOrigin:
                        self.__trainOriginValid = True
                    else:
                        print('Invalid Asnwer. C for other company or B from bank: ')
                if self.__trainOrigin == 'c':
                    self.__trainOriginCompanyValid = False
                    while not self.__trainOriginCompanyValid:
                        self.__trainOriginCompany = input('What company is it? Enter Two Letter Code: ')
                        if self.__trainOriginCompany == 'AR' or self.__trainOriginCompany == 'IR' or self.__trainOriginCompany == 'SR' or self.__trainOriginCompany == 'KO' or self.__trainOriginCompany == 'TR' or self.__trainOriginCompany == 'KU' or self.__trainOriginCompany == 'UR':
                            for y in self.__activeCompanies:
                                if y == self.__companyReference[self.__trainOriginCompany]:
                                    self.__trainOriginCompanyValid = True
                                else:
                                    print('Invalid Answer. Enter Two Letter Code: ')
                        else:
                            print('Invalid Answer. Enter Two Letter Code: ')
                    self.__trainPriceValid = False
                    while not self.__trainPriceValid:
                        try:
                            self.__trainPrice = int(input('Please input perchase price: '))
                            if 1 <= self.__trainPrice:
                                self.__trainPriceValid = True
                            else:
                                print('Invalid Asnwer. Please input perchase price: ')
                        except ValueError:
                                print('Invalid Asnwer. Please input perchase price: ')
                    self.__companyReference[self.__companyName].adjust_money(-1*self.__trainPrice) 
                    self.__companyReference[self.__trainOriginCompany].adjust_money(1*self.__trainPrice)
                else:
                    self.__trainNumberValid = False
                    while not self.__trainNumberValid:
                        self.__trainNumber = input('What is the name of the train you are buying? Enter the name of the train: ').upper()
                        if self.__trainNumber == '2' or self.__trainNumber == '3' or self.__trainNumber == '4' or self.__trainNumber == '5' or self.__trainNumber == '6' or self.__trainNumber == 'D':
                            self.__trainNumberValid = True
                        else:
                            print('Invalid Answer. Enter the name of the train:')
                    if self.__trainNumber == 'D':
                        self.__dTrainTradeInValid = False
                        while not self.__dTrainTradeInValid: 
                            self.__tradeIn = input('Do you want to trade in a train? Y or N: ').lower()
                            if 'y' == self.__tradeIn or 'n' == self.__tradeIn:
                                self.__dTrainTradeInValid = True
                            else:
                                print('Invalid Asnwer. Y or N: ')
                        if self.__tradeIn == 'y':
                            self.__companyReference[self.__companyName].adjust_money(-800)
                            self.__bank = self.__bank + 800
                        else:
                            self.__companyReference[self.__companyName].adjust_money(-1100)
                            self.__bank = self.__bank + 1100
                    else:
                        self.__companyReference[self.__companyName].adjust_money(-1*self.__trainDefaultPrice[self.__trainNumber])
                        self.__bank = self.__bank + self.__trainDefaultPrice[self.__trainNumber]
                    if self.__trainNumber == '3':
                        self.__phase = 3
                    elif self.__trainNumber == '5':
                        self.__phase = 5
                        self.__privateIncome = {20: 0, 30: 0, 40: 0, 50: 0, 60: 0, 80: 0, 150: 50}
            if self.__phase == 3:
                self.__privateBuyValid = False
                while not self.__privateBuyValid: 
                    self.__privateBuy = input('Do you want to buy a private company? Y or N: ').lower()
                    if 'y' == self.__privateBuy or 'n' == self.__privateBuy:
                        self.__privateBuyValid = True
                    else:
                        print('Invalid Asnwer. Y or N: ')
                if self.__privateBuy == 'y':
                    self.__playerNameValid = False
                    while not self.__playerNameValid:
                        try:
                            self.__playerName = int(input('Please input who you are perchasing from: ')) - 1
                            if 0 <= self.__playerName <= self.__numOfPlayers - 1:
                                self.__playerNameValid = True
                            else:
                                print('Invalid Asnwer. Please input who you are perchasing from: ')
                        except ValueError:
                                print('Invalid Asnwer. Please input who you are perchasing from: ')
                    self.__privatePriceValid = False
                    while not self.__privatePriceValid:
                        try:
                            self.__privatePrice = int(input('Please input the price that you are perchasing: '))
                            if 1 <= self.__privatePrice:
                                self.__privatePriceValid = True
                            else:
                                print('Invalid Asnwer. Please input the price that you are perchasing: ')
                        except ValueError:
                                print('Invalid Asnwer. Please input the price that you are perchasing: ')
                    self.__privateCompanyValid = False
                    while not self.__privateCompanyValid:
                        try:
                            self.__privateCompanyPar = int(input('Please input the par value of the private company that you are perchasing: ')) 
                            if 20 == self.__privateCompanyPar or 30 == self.__privateCompanyPar or 40 == self.__privateCompanyPar or 50 == self.__privateCompanyPar or 60 == self.__privateCompanyPar or 80 == self.__privateCompanyPar or 150 == self.__privateCompanyPar:
                                self.__privateCompanyValid = True
                            else:
                                print('Invalid Asnwer. Please input the par value of the private company that you are perchasing: ')
                        except ValueError:
                                print('Invalid Asnwer. Please input the par value of the private company that you are perchasing: ')
                    self.__listOfPlayerObjects[self.__playerName].adjust_privates(self.__privateCompanyPar, False)
                    self.__companyReference[self.__companyName].adjust_privates(self.__privateCompanyPar, True)
                    self.__listOfPlayerObjects[self.__playerName].adjust_money(self.__privatePrice)
                    self.__companyReference[self.__companyName].adjust_money(-1*self.__privatePrice)
            self.__companiesGone.append(self.__companyName)

    def check_game_end(self):
        if self.__bank <= 0:
            if self.__gameOver == False:
                print('Bank Has Broken')
            self.__gameOver = True

    def terminal(self):
        self.__terminalDone = False
        while not self.__terminalDone:
            try:
                self.__terminalAction = input('Money, Stock, Bankrupt, Privates, Data, Done: ').lower()
                if self.__terminalAction == 'money':
                    self.__companyOrPersonValid = False
                    while not self.__companyOrPersonValid: 
                        self.__companyOrPerson = input('Do you want to adjust a company? Y or N: ').lower()
                        if 'y' == self.__companyOrPerson or 'n' == self.__companyOrPerson:
                            self.__companyOrPersonValid = True
                        else:
                            print('Invalid Asnwer. Y or N: ')
                    if self.__companyOrPerson == 'n':
                        self.__playerAdjustValid = False
                        while not self.__playerAdjustValid:
                            try:
                                self.__playerName = int(input('Please input who you are adjusting: ')) - 1
                                if 0 <= self.__playerName <= self.__numOfPlayers - 1:
                                    self.__playerAdjustValid = True
                                else:
                                    print('Invalid Asnwer. Please input who you are adjusting: ')
                            except ValueError:
                                    print('Invalid Asnwer. Please input who you are adjusting: ')  
                        self.__adjustAmountValid = False 
                        while not self.__adjustAmountValid:
                            try:
                                self.__adjustAmount = int(input('Please input adjustment: '))
                                self.__adjustAmountValid = True
                            except ValueError:
                                    print('Invalid Asnwer. Please input adjustment: ')  
                        self.__listOfPlayerObjects[self.__playerName].adjust_money(self.__adjustAmount)
                    else:
                        self.__companyValid = False
                        while not self.__companyValid:
                            self.__companyAdjust = input('What company is it? Enter Two Letter Code: ')
                            if self.__companyAdjust == 'AR' or self.__companyAdjust == 'IR' or self.__companyAdjust == 'SR' or self.__companyAdjust == 'KO' or self.__companyAdjust == 'TR' or self.__companyAdjust == 'KU' or self.__companyAdjust == 'UR':
                                self.__companyValid = True
                            else:
                                print('Invalid Answer. Enter Two Letter Code: ')
                        self.__adjustAmountValid = False 
                        while not self.__adjustAmountValid:
                            try:
                                self.__adjustAmount = int(input('Please input adjustment: '))
                                self.__adjustAmountValid = True
                            except ValueError:
                                print('Invalid Asnwer. Please input adjustment: ')  
                        self.__companyReference[self.__companyAdjust].adjust_money(self.__adjustAmount)
                elif self.__terminalAction == 'stock':
                    self.__stockAdjustValid = False
                    while not self.__stockAdjustValid:
                        try:
                            self.__playerName = int(input('Please input who you are adjusting: ')) - 1
                            if 0 <= self.__playerName <= self.__numOfPlayers - 1:
                                self.__stockAdjustValid = True
                            else:
                                print('Invalid Asnwer. Please input who you are adjusting: ')
                        except ValueError:
                                print('Invalid Asnwer. Please input who you are adjusting: ')  
                    self.__adjustAmountValid = False 
                    while not self.__adjustAmountValid:
                        try:
                            self.__adjustAmount = int(input('Please input adjustment: '))
                            self.__adjustAmountValid = True
                        except ValueError:
                                print('Invalid Asnwer. Please input adjustment: ')
                    self.__companyValid = False
                    while not self.__companyValid:
                        self.__companyAdjust = input('What company is it? Enter Two Letter Code: ')
                        if self.__companyAdjust == 'AR' or self.__companyAdjust == 'IR' or self.__companyAdjust == 'SR' or self.__companyAdjust == 'KO' or self.__companyAdjust == 'TR' or self.__companyAdjust == 'KU' or self.__companyAdjust == 'UR':
                            self.__companyValid = True
                        else:
                            print('Invalid Answer. Enter Two Letter Code: ')
                    self.__listOfPlayerObjects[self.__playerName].adjust_stock(self.__adjustAmount, self.__companyAdjust)
                    self.__companyReference[self.__companyAdjust].increase_stocks_owned(self.__adjustAmount)
                elif self.__terminalAction == 'bankrupt':
                    self.__gameOver = True
                elif self.__terminalAction == 'privates':
                    self.__privateAdjustValid = False
                    while not self.__privateAdjustValid:
                        try:
                            self.__playerName = int(input('Please input who you are adjusting: ')) - 1
                            if 0 <= self.__playerName <= self.__numOfPlayers - 1:
                                self.__privateAdjustValid = True
                            else:
                                print('Invalid Asnwer. Please input who you are adjusting: ')
                        except ValueError:
                                print('Invalid Asnwer. Please input who you are adjusting: ')  
                    self.__adjustValid = False 
                    while not self.__adjustValid:
                        try:
                            self.__adjustAmount = bool(input('Please input True or False: '))
                            self.__adjustValid = True
                        except ValueError:
                                print('Invalid Asnwer. Please input True or False: ')
                    self.__privateValid = False
                    while not self.__privateValid:
                        try:
                            self.__privateAdjusted = int(input('What company is it? Enter Par Value: '))
                            self.__privateValid = True
                        except ValueError:
                            print('Invalid Answer. Enter Par Value: ')
                        self.__listOfPlayerObjects[self.__playerName].adjust_privates(self.__privateAdjusted, self.__adjustAmount)
                elif self.__terminalAction == 'data':
                    for i in self.__listOfPlayerObjects:
                        print(i.retrive_info())
                    for x in self.__companyReference:
                        print(f'{x}: {self.__companyReference[x].retrive_info()}')
                elif self.__terminalAction == 'done':
                    self.__terminalDone = True
                elif self.__terminalAction == 'phaseAdjust':
                    self.__phaseValid = False
                    while not self.__phaseValid:
                        try:
                            self.__newPhase = int(input('What company is it? Enter 1, 3 or 5: '))
                            if self.__newPhase == 1 or self.__newPhase == 3 or self.__newPhase == 5:
                                self.__phaseValid = True
                    self.__phase = self.__newPhase
            except:
                pass

game = Game()        
