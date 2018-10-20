# Recursive fib

def fib_r(index, result=[], _count = 0):

    # Flush
    if _count == 0:
        del result[:]

    if len(result) == (index + 1):
        return result
    
    _count += 1
    if _count <= 2:
        result.append(1)
        return fib_r(index, result, _count)
        
    result.append(result[-1] + result[-2])
    return fib_r(index, result, _count)
