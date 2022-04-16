#多进程验证哥德巴赫猜想
import time
from multiprocessing import cpu_count
from multiprocessing import Pool

import math
# 判断数字是否为素数
def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

#验证大于2的偶数可以分解为两个质数之和
def goldbach(T):
# T为列表，第一个元素为区间起点，第二个元素为区间终点
    S = T[0]
    E = T[1]
    sample=[]   #用于返回样例
    if S < 4:   #若不是大于2的偶数
        S = 4   #设为大于2的最小偶数
    if S % 2 == 1:      #除2余数为1的是奇数
        S += 1          #奇数+1为偶数
    for i in range(S, E + 1, 2):    #遍历区间内所有偶数
        isGoldbach = False
        for j in range(i // 2 + 1): # 表示成两个素数的和,其中一个不大于1/2
            if isPrime(j):
                k = i - j
                if isPrime(k):
                    isGoldbach = True
                    if i % 100000 == 0:  # 每隔10万输出样例
                        sample.append((i,j,k))
                    break
        if not isGoldbach:
            #如果打印这句话表示算法失败或欧拉错了
            sample.append('哥德巴赫猜想失败！')
            break
    return sample

#把数字空间N分段，分段数为内核数
def subRanges(N, CPU_COUNT):
    list = [[i + 1, i + N // CPU_COUNT] for i in range(4, N, N // CPU_COUNT)]
    list[0][0] = 4
    if list[CPU_COUNT - 1][1] > N:
        list[CPU_COUNT - 1][1] = N
    return list

def main():
    N = 10**6       #根据电脑性能调整
    CPU_COUNT = cpu_count()  #获取CPU内核数
    print("There are", CPU_COUNT, "core(s) CPU")
    #单进程测试
    print("Single Thread process running.......")
    start = time.perf_counter()
    results=goldbach([4, N])    #4-N区间内执行goldbach
    for sample in results:
        print('%d=%d+%d' % sample)
    print('Time used for single thread: %4.3fs' % (time.perf_counter() - start))

    #多进程测试
    print("Multi Thread process running")
    pool = Pool(CPU_COUNT)   #建立进程池，进程数等于CPU内核数
    sepList = subRanges(N, CPU_COUNT)   #将数N按内核数分割
    start = time.perf_counter()
    results=pool.map(goldbach, sepList)    #并行迭代goldbach函数
    pool.close()    #关闭进程池
    pool.join()     #等待所有进程结束

    for result in results:
        for sample in result:
            print('%d=%d+%d' % sample)
    print('Time used for multi thread: %4.3fs' % (time.perf_counter() - start))

if __name__ == '__main__':
    main()


