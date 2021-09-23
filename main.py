from ci import CoxIngersoll
from rb import RB 
from vasicek import Vasicek
from merton import Merton
from ho_lee import HoLee

V = Vasicek()
C = CoxIngersoll() 

M = Merton()
R = RB() 
H = HoLee()

V.show_rates()
C.show_rates()

M.show_rates()
R.show_rates()
H.show_rates()
