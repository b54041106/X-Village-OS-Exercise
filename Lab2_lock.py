import threading
import queue
import os

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0

def producer(top_dir,queue_buffer):
    # Search sub-dir in top_dir and put them in queue
    files=os.listdir(top_dir)
    queue_buffer.put(top_dir,block=True, timeout=0.1)
    for i in files:
        filepath=os.path.join(top_dir,i)
        #print(filepath)
        if os.path.isdir(filepath):
            producer(filepath,queue_buffer)

          
def consumer(queue_buffer):
    # search file in directory
    global file_count
    try:
        path=queue_buffer.get(block=True, timeout=0.1)
        filename=os.listdir(path)
        #print(filename)
        for f in filename:
            newpath=os.path.join(path,f)
            if os.path.isfile(newpath):
                lock.acquire()
                file_count+=1
                lock.release()
    except:
        pass
    

def main():
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))

    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()
   
    print(file_count, 'files found.')

if __name__ == "__main__":
    main()