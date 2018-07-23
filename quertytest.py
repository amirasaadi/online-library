from book import models as bm
from users import models as um

sadaf= um.User.objects.get(username='sadaf08')
bagher = um.User.objects.get(username='bagher')

mebeforeyou = bm.Copy.objects.get(id=4)

lo = bm.Loan()

lo.person= bagher
lo.book = mebeforeyou

lo.can_loan()