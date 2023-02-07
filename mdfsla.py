import random
import sys
import math

P = 200 #population size
m = 10 #number of memeplexes
iMax = 500 #number of iterations
alpha = 0.4 #parameter for discrete
pm = 0.06 #mutation rate
p_max = 100000 #profit max
luggage_num = 0
capacity = 0
p_list = []
w_list = []


class population:
    frog_list = []
    memeplex_list = [] * m
    def __init__(self):
        self.global_best_frog = individual()
        self.is_termination = False
        self.best_fitness = 0
        self.former_best_fitness = 0
        self.delta = 0

    def init_population(self):
        for i in range(P):
            self.frog_list.append(individual(luggage_num, w_list, capacity, p_list))
    
    def calc_fitness_population(self):
        for i in range(P):
            self.frog_list[i].calc_fitness()
    
    def sort_population(self):
        self.frog_list = sorted(self.frog_list, key=lambda frog: frog.fitness, reverse = True)
        self.global_best_frog = self.frog_list[0]
        self.former_best_fitness = self.best_fitness
        self.best_fitness = self.global_best_frog.fitness
    
    def partition(self):
        for k in range(m):
            self.memeplex_list[k] = memeplex(self.global_best_frog)
        for i in range(P/m):
            for j in range(m):
                self.memeplex_list[j].frog_in_memeplex[i] = self.frog_list[i*m + j]
    
    def search(self):
        for i in range(m):
            self.memeplex_list[i].local_search()
    
    def mutation(self):
        for i in range(P):
            self.frog_list[i].ind_mutation()
    
    def judge_termination(self):
        self.sort_population()
        if self.best_fitness == self.former_best_fitness:
            self.delta += 1
        if self.delta >= math.ceil(iMax/20.0):
            self.is_termination = True




class memeplex:
    frog_in_memeplex = [] * (P / m)
    def __init__(self, global_best_frog):
        self.global_best_frog = global_best_frog
        self.best_frog = individual()
        self.worst_frog = individual()
        self.D = [] * luggage_num
        self.t = [] * luggage_num
        self.worst_frog_new = individual()
        self.xw_new = [] * luggage_num

    def local_sesarch(self):
        for i in range(iMax):
            self.sort_memeplex()
            self.mk_worst_new(self.best_frog.x)
            self.worst_frog.calc_fitness()
            self.worst_frog_new.calc_fitness()
            if self.worst_frog.fitness < self.worst_frog_new.fitness:
                self.worst_frog.x = self.worst_frog_new.x
                self.worst_frog.fitness = self.worst_frog_new.fitness
                continue
            self.mk_worst_new(self.global_best_frog.x)
            self.worst_frog_new.calc_fitness()
            if self.worst_frog.fitness < self.worst_frog_new.fitness:
                self.worst_frog.x = self.worst_frog_new.x
                self.worst_frog.fitness = self.worst_frog_new.fitness
                continue
            random_frog = individual()
            random_frog.calc_fitness()
            self.worst_frog.x = random_frog.x
            self.worst_frog.fitness = random_frog.fitness

    def sort_memeplex(self):
        self.frog_in_memeplelx = sorted(self.frog_in_memeplex, key=lambda frog: frog.fitness, reverse = True)
        self.best_frog = self.frog_in_memeplex[0]
        self.worst_frog = self.frog_in_memeplex[m-1]

    def mk_worst_new(self, xbg):
        for j in range(luggage_num):
            self.D[j] = random.random() * (xbg[j] - self.worst_frog.x[j])
            self.t[j] = 1 / (1 + math.exp(-self.D[j]))
            if self.t[j] < alpha:
                self.xw_new[j] = 0
            elif self.t[j] >= (1+alpha)/2:
                self.xw_new[j] = 1
            else:
                self.xw_new[j] = self.worst_frog.x[j]
        self.worst_frog_new.x = self.xw_new



class individual:
    x = []
    fitness = 0
    def __init__(self):
        for i in range(luggage_num):
            self.x.append(random.randint(0, 1))
    
    def calc_fitness(self):
        self.repair_x(self.x)
        p_in_bag = 0
        for i in range(luggage_num):
            if self.x[i] == 1:
                p_in_bag += p_list[i]
        self.fitness = p_in_bag

    def repair_x(self):
        w_in_bag = self.calc_w_in_bag()
        while w_in_bag > capacity: #capacityを超えていたらprofit/weightが最も小さいものを取り除く
            min_i = 0
            min_ppw = p_max
            for i in range(luggage_num):
                if self.x[i] == 1:
                    if p_list[i]/w_list[i] < min_ppw:
                        min_i = i
                        min_ppw = p_list[i] / w_list[i]
            self.x[min_i] = 0
            w_in_bag = self.calc_w_in_bag()

    def calc_w_in_bag(self):
        w_in_bag = 0
        for i in range(luggage_num):
            if self.x[i] == 1:
                w_in_bag += w_list[i]
        return w_in_bag
    
    def ind_mutation(self):
        for i in range(luggage_num):
            if random.random() < pm:
                if self.x[i] == 1:
                    self.x[i] = 0
                else:
                    self.x[i] = 1    


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

frog_population = population()
frog_population.init_population()
frog_population.calc_fitness_population()
frog_population.sort_population()
if not frog_population.is_termination:
    frog_population.partition()
    frog_population.search()
    frog_population.mutation()
    is_termination = frog_population.judge_termmination()
print(f'answer is {frog_population.global_best_frog.x}')
