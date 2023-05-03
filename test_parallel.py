import time
import multiprocessing
#from joblib import Parallel, delayed
import numpy as np

def tasks(n,k):
    rd = np.random.randint(0,4)
    rd2 = np.random.randint(0,4)
    a=(n+rd,k+rd2)
    return a
it=500000

start_time = time.time()
# rodando de forma sequencial

results_seq = []
for i in range(it):
    result = tasks(i,i)
    results_seq.append(result)
end_time = time.time()
time_seq = end_time - start_time

print(f"Tempo de execução sequencial: {time_seq:.4f} segundos")

'''
it=500000
# executando o loop em paralelo
start_time = time.time()
ka=10
na=10

results_par= Parallel(n_jobs=4)(delayed(tasks) (na,ka) for i in range(it))

end_time = time.time()
time_par = end_time - start_time

print(f"Tempo de execução em paralelo: {time_par:.4f} segundos")
r=sorted(results_par, key=lambda tupla: tupla[0])
#print(r)'''
if __name__ == '__main__':

    start_time2 = time.time()
    pool = multiprocessing.Pool(processes=4)
    elementos = list(range(it))
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        result = pool.starmap(tasks, [(elementos[i], elementos[i]) for i in range(it)])
    end_time2 = time.time()
    time_seq2 = end_time2 - start_time2

    print(f"Tempo de execução multiprocessing: {time_seq2:.4f} segundos")