from __future__ import print_function
import numpy as np
from Queue import PriorityQueue, Empty
from collections import deque
import sys


MAX_VALUE=999999999.0


class BatchActiveSubset(object):
    '''
        BatchActiveSubset:
            A class controlling the parameters of the batch active learner.
            It takes as input the submodular objective function, the budget,
            which is the constraint in the optimization problem, a list of words
            used to learn some feature extractors or edge similarity for
            instance, a list of words from which we will select upto budget's
            worth, and a few optional arguments that control the selection.
            
            Inputs: 
                objective -- The submodular objective to optimize. This is
                             implemented as a class
                budget    -- The contraint in the submodular optimization problem
                wordlist  -- A list of words from which to select budget's
                             worth
                cost=1 -- The cost of select each word for g2p training. The cost
                          could be things such as the length, some power of the
                          length, the word frequency, etc..
    '''
    def __init__(self, objective, budget, wordlist,
                cost=lambda x: 1, cost_select=False):
        self.objective = objective # An objective object
        self.budget = budget
        self.test_wordlist = wordlist
        self.cost = cost
        self.cost_select = cost_select 
    
 
    def run_lazy(self):
        S = []
        set_value = 0.0
        total_cost = 0.0
        remaining_budget = self.budget

        # Initialize Priority Queue
        upper_bounds = PriorityQueue()
        self.objective.set_subset(S)
        for i, w in enumerate(self.test_wordlist):
            if (self.cost(w) <= self.budget):
                upper_bounds.put((-MAX_VALUE, i))    
        
        # Main loop (Continue until budget is reached, or no elements remain) 
        while total_cost < self.budget and not upper_bounds.empty():
            alpha_idx, idx = upper_bounds.get(False)
           
            if (self.cost(self.test_wordlist[idx]) > remaining_budget):
                continue;
                 
            new_set_value = self.objective.run(idx)
            gain = (new_set_value - set_value)
            assert gain >= 0, "ERROR: Expected gain >= 0" 
            if self.cost_select:
                gain /= self.cost(self.test_wordlist[idx])
          
            # This is for the case when idx is the last element 
            try: 
                max_val, idx_max = upper_bounds.get(False)
                upper_bounds.put((max_val, idx_max))
            except Empty:
                max_val = 0.0 

            if (gain >= -max_val):
                S.append(idx)
                #self.objective.set_subset(S)
                self.objective.add_to_subset(idx)
                total_cost += self.cost(self.test_wordlist[idx])
                set_value = new_set_value

                print(self.test_wordlist[idx].encode('utf-8'), "Consumed: ", total_cost, "/", self.budget,
                    ":  +", self.cost(self.test_wordlist[idx]), end=" : ")
                print("Set value: ", set_value, end=" : ")
                print("Gain: ", gain, end=" : ")
 
                remaining_budget = self.budget - total_cost
                print("Remaining Candidates: ", upper_bounds.qsize())

            else:
                upper_bounds.put((-gain, idx))
                
        return [self.test_wordlist[idx] for idx in S]


class RandomSubset(object):
    def __init__(self, objective, budget, wordlist, cost=lambda x: 1, cost_select=False):
        self.budget = budget
        self.test_wordlist = wordlist
        self.cost = cost
    
    
    def run(self):
        ranked_words = []
        V_minus_S = [w for w in self.test_wordlist if self.cost(w) <= self.budget]
        total_cost = 0.0
        
        while total_cost < self.budget and len(V_minus_S) > 0:
            w_star = V_minus_S.pop(np.random.randint(len(V_minus_S)))
            ranked_words.append(w_star)
            total_cost += self.cost(w_star)
            print(w_star.encode('utf-8'), "Consumed: ", total_cost, "/", self.budget, ": + ", self.cost(w_star), end=" : ")
            
            remaining_budget = self.budget - total_cost
            V_minus_S = [w for w in V_minus_S if self.cost(w) <= remaining_budget]
            print("Remaining Candidates: ", len(V_minus_S))
            
        return ranked_words
    
    def run_lazy(self):
        return self.run()

