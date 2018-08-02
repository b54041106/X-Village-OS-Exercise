import multiprocessing 
import numpy as np 
import time

def thread_func(process_no, result_queue,matA_row,matB):
    result_queue.put((process_no, np.matmul(matA_row,matB)))

def main():
    x=input('please enter 10,100 or 1000:')
    y=int(x)
    thread_num = input('please enter thread number:')
    t=int(thread_num) #y要可以被t整除，不然就false

    matA = np.random.randint(10, size = (y, y))
    matB = np.random.randint(10, size = (y, y))
    result = np.zeros((matA.shape[0], matB.shape[1]))    
    matrix=np.zeros((matA.shape[0], matB.shape[1]))
    result_queue = multiprocessing.Manager().Queue()
    Asplit=np.split(matA,10,axis=0)
    processes = 10
    jobs = []

    for i in range(processes):
        # matA_row=matA[i]
        process = multiprocessing.Process(target = thread_func,args = (i, result_queue,Asplit[i],matB))
        jobs.append(process)
    
    start_time = time.time()
    for process in jobs:
        process.start()
    
    for process in jobs:
        process.join()

    while not result_queue.empty():
        result = result_queue.get()
        #print(result)
        matrix[result[0]*(y//t):result[0]*(y//t)+(y//t),:100]=result[1]
        print(matrix)
    print(np.matmul(matA,matB))
    print('Answer is correct:', np.all(np.matmul(matA, matB) == matrix))
    end_time = time.time()
    print('Time elapsed:\t', end_time - start_time)

if __name__ == "__main__":
    main()

