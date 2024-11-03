# Code 100% written in JustText. Simple fibonnacci function.

def fibo(n: int) -> int:
    fn1: int = 0
    fn2: int = 1
    
    for _ in range(2, n+1):
        fn2 = fn1 + fn2
        fn1 = fn2 - fn1

    return n > 0 and fn2 or 0

print(fibo(10)) # 55
