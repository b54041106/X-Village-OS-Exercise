import threading
import numpy as np 
import time
from memory_profiler import profile

def thread_func(i,matA, matB,matC,y,t):
    row_value=np.matmul(matA, matB)
    matC[i*(y//t):(i+1)*(y//t)]=row_value
    print(matC)

@profile
def main():
    x=input('please enter 10,100 or 1000:')
    y=int(x)
    thread_num = input('please enter thread number:')
    t=int(thread_num) 
    matA = np.random.randint(10, size = (y, y))
    matB = np.random.randint(10, size = (y, y))
    matC = np.zeros((y,y))
    Asplit=np.split(matA,t,axis=0)
    threads = []

    for i in range(t):
        thread = threading.Thread(target = thread_func, args = (i,Asplit[i],matB,matC,y,t))
        threads.append(thread)

    start_time=time.time()
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    print(matC)
    print(np.matmul(matA,matB))
    print('Answer is correct:', np.all(np.matmul(matA, matB) == matC))
    end_time = time.time()
    print('Time elapsed:\t', end_time - start_time)


if __name__ == "__main__":
    main()
