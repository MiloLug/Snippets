
def calc(C, I, InU, StorageFee, TheirExchangeProfitFee):
    """
    In:
    InU = Your UAH input
    C = EUR/UAH
    Fee = How much you pay for storing
    I = inflation
    """
    
    # Calc:
    # EUR = C * UAH
    # UAH = EUR / C
    
    InE = C * InU
    MyStorageProfitE = InE * StorageFee
    
    BalanceU = InU - MyStorageProfitE / C
    BalanceE = BalanceU * C
    
    # After inflation I (% decimal as 0.1, -0.2 etc.):
    C = C * (1 - I)
    
    BalanceDiffE = BalanceU * C - BalanceE
    
    MyExchangeProfitE = BalanceDiffE * TheirExchangeProfitFee
    TheirExchangeProfitE = BalanceDiffE - MyExchangeProfitE
    
    MyProfitE = MyStorageProfitE + MyExchangeProfitE
    
    BalanceU = BalanceU - MyExchangeProfitE / C
    # move their profit in UAH to the BalanceU and return to the client
    TheirProfitE = BalanceU * C - InE

    return {
        'my_profit_eur': MyProfitE,
        'client_return_uah': BalanceU,
        'client_profit_eur': TheirProfitE
    }
    

def calc_optimized(C, I, InU, StorageFee, TheirExchangeProfitFee):
    return InU * C * (StorageFee + (1 - StorageFee) * I * TheirExchangeProfitFee)

    
InU = 10000
C = 1/30
StorageFee = 0
TheirExchangeProfitFee = 0.9

print('Inflation:', -0.2, '\n', calc_optimized(
    C=C,
    I=-0.2,
    InU=InU,
    StorageFee=StorageFee,
    TheirExchangeProfitFee=TheirExchangeProfitFee
))
print('Inflation:', 0, '\n', calc_optimized(
    C=C,
    I=0,
    InU=InU,
    StorageFee=StorageFee,
    TheirExchangeProfitFee=TheirExchangeProfitFee
))
print('Inflation:', 0.2, '\n', calc_optimized(
    C=C,
    I=0.2,
    InU=InU,
    StorageFee=StorageFee,
    TheirExchangeProfitFee=TheirExchangeProfitFee
))
