import random
import sys

P = 200 #population size
m = 10 #number of memeplexes
iMax = 500 #number of iterations
alpha = 0.4 #parameter for discrete
pm = 0.06 #mutation rate
p_max = 100000 #profit max


class population:
    frog_list = []
    memeplex_list = [] * m
    def __init__(self, luggage_num, w_list, capacity, p_list):
        self.luggage_num = luggage_num
        self.w_list = w_list
        self.capacity = capacity
        self.p_list = p_list
        self.xg = [0] * self.luggage_num #globalで最もfitnessの大きいxが格納される

    
    def init_population(self):
        for i in range(P):
            self.frog_list.append(individual(self.luggage_num, self.w_list, self.capacity, self.p_list))
    
    def calc_fitness_population(self):
        for i in range(P):
            self.frog_list[i].calc_fitness()
    
    def sort_population(self):
        self.frog_list = sorted(self.frog_list, key=lambda frog: frog.fitness, reverse = True)
        self.xg = self.frog_list[0].x
    
    def partition(self):
        for k in range(m):
            self.memeplex_list[k] = memeplex()
        for i in range(P/m):
            for j in range(m):
                self.memeplex_list[j].frog_in_memeplex[i] = self.frog_list[i*m + j]
    
    def search(self):
        for i in range(m):
            self.memeplex_list[i].local_search(self.xg)



class memeplex:
    frog_in_memeplex = [] * (P / m)

    def local_sesarch(self.xg):
        for i in range(iMax):

    


class individual:
    x = []
    fitness = 0
    def __init__(self, luggage_num, w_list, capacity, p_list):
        for i in range(luggage_num):
            self.x.append(random.randint(0, 1))
        self.w_list = w_list
        self.capacity = capacity
        self.p_list = p_list
    
    def calc_fitness(self):
        self.repair_x()
        p_in_bag = 0
        for i in range(luggage_num):
            if self.x[i] == 1:
                p_in_bag += self.p_list[i]
        self.fitness = p_in_bag

    def repair_x(self):
        w_in_bag = self.calc_w_in_bag()
        while w_in_bag > self.capacity: #capacityを超えていたらprofit/weightが最も小さいものを取り除く
            min_i = 0
            min_ppw = p_max
            for i in range(luggage_num):
                if self.x[i] == 1:
                    if self.p_list[i]/self.w_list[i] < min_ppw:
                        min_i = i
                        min_ppw = self.p_list[i] / self.w_list[i]
            self.x[min_i] = 0
            w_in_bag = self.calc_w_in_bag()

    def calc_w_in_bag(self):
        w_in_bag = 0
        for i in range(luggage_num):
            if self.x[i] == 1:
                w_in_bag += self.w_list[i]
        return w_in_bag


#main
args = sys.argv
c_filename = args[0] #capacity
w_filename = args[1] #weight
p_filename = args[2] #profit
s_filename = args[3] #selection

cf = open(c_filename, 'r')
capacity = cf.readlines()

wf = open(w_filename, 'r')
w_list = wf.readlines()
luggage_num = len(w_list)

pf = open(p_filename, 'r')
p_list = pf.readlines()

sf = open(s_filename, 'r')
s_list = sf.readlines()

frog_population = population(luggage_num, w_list, capacity, p_list)
frog_population.init_population()
frog_population.calc_fitness_population()
frog_population.sort_population()
frog_population.partition()
frog_population.search()
