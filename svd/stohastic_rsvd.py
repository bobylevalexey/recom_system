# coding=utf-8
from svd.brute_rsvd import BruteRSVD


class StohasticRSVD(BruteRSVD):
    def train(self):
        for epoch in xrange(self.max_epochs):
            for k in xrange(self.r):
                denominator = sum(self.V_matr[i_id][k] ** 2
                                  for i_id in self.V_matr) + self.reg
                for user_id in self.U_matr:
                    self.U_matr[user_id][k] = sum(
                            r * self.V_matr[i_id][k]
                            for u_id, i_id, r in self.R_matr
                            if u_id == user_id) / denominator
            for k in xrange(self.r):
                denominator = sum(self.U_matr[u_id][k] ** 2
                                  for u_id in self.U_matr) + self.reg
                for item_id in self.V_matr:
                    self.V_matr[item_id][k] = sum(
                            r * self.U_matr[u_id][k]
                            for u_id, i_id, r in self.R_matr
                            if i_id == item_id) / denominator
            lf = self.calc_loss_function()
            print 'lf', lf
            print self.calc_model_rmse()

if __name__ == "__main__":
    from svd.test_data import R
    model = StohasticRSVD(R, lrate=0.01, reg=1, r=3, max_epochs=100, acc=0.001)
    model.train()
    print model.calc_model_rmse()
