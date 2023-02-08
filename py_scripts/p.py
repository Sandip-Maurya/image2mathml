import random, os, time
rand_int = random.randint(100000, 999999)
datetime_now = str(time.time()).replace('.', 'dot')
print(datetime_now)
f = open('random.txt', 'a')
f.write(f'{datetime_now}.png\n')
f.close()


