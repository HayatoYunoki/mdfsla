import random

P = 200 #population size
m = 10 #number of memeplexes
iMax = 500 #number of iterations
alpha = 0.4 #parameter for discrete
pm = 0.06 #mutation rate
p_max = 100000 #profit max


class population:
    frog_list = []
    def __init__(self, luggage_num, w_list, capacity, p_list):
        self.luggage_num = luggage_num
        self.w_list = w_list
        self.capacity = capacity
        self.p_list = p_list
    
    def init_population():
        for i in range(P):
            frog_list.append(individual(self.luggage_num, self.w_list, self.capacity, self.p_list))




class memeplex:
    def __init__(self):


class individual:
    x = []
    def __init__(self, luggage_num, w_list, capacity, p_list):
        for i in range(luggage_num):
            self.x.append(random.randint(0, 1))
        self.w_list = w_list
        self.capacity = capacity
        self.p_list = p_list
    
    def calc_fitness():
        repair_x()
    
    def repair_x():
        w_in_bag = calc_w_in_bag()
        while w_in_bag > self.capacity: #capacityを超えていたらprofit/weightが最も小さいものを取り除く
            min_i = 0
            min_ppw = p_max
            for i in range(luggage_num):
                if x[i] == 1:
                    if p_list[i]/w_list[i] < min_ppw:
                        min_i = i
                        min_ppw = p_list[i]/w_list[i]
            x[min_i] = 0
            w_in_bag = calc_w_in_bag()
        
    
    def calc_w_in_bag():
        w_in_bag = 0
        for i in range(luggage_num):
            if self.x[i] == 1:
                w_in_bag += self.w_list[i]
        return w_in_bag




#main