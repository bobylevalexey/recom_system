class StohasticRSVD(object):
    # def find_min(self):
    def train(self):
        for epoch in xrange(self.max_epochs):
            for k in xrange(self.r):
                denominator = sum(self.V_matr[i_id] ** 2
                                  for i_id in self.V_matr) + self.reg
                for user_id in self.U_matr:
                    self.U_matr[user_id] = sum(r * self.V_matr[i_id][k]
                                               for u_id, i_id, r in self.R_matr
                                               if u_id == user_id) / denominator
            for k in xrange(self.r):
                denominator = sum(self.U_matr[u_id] ** 2
                                  for u_id in self.U_matr) + self.reg
                for item_id in self.V_matr:
                    self.V_matr[item_id] = sum(r * self.U_matr[u_id][k]
                                               for u_id, i_id, r in self.R_matr
                                               if i_id == item_id) / denominator
