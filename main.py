from cox_ingersoll import CoxIngersoll
from rendleman_bartter import RB 
from vasicek import Vasicek
from merton import Merton
from ho_lee import HoLee

time = 30

V = Vasicek(time)
C = CoxIngersoll(time) 
# M = Merton(time)
# R = RB(time) 
# H = HoLee(time)

V.show_rates()
C.show_rates()

# M.show_rates()
# R.show_rates()
# H.show_rates()
