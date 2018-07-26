from book import models as bm
from users import models as um

copy_list = bm.Copy.objects.all()
loan_list = bm.Loan.objects.all()
bm.Loan.objects.filter(book__book__copy__id=6)
############################################################3
# from openpyxl import Workbook
# wb = Workbook()
#
# # grab the active worksheet
# ws = wb.active
#
# # Data can be assigned directly to cells
# ws['A1'] = 42
#
# # Rows can also be appended
# ws.append([1, 2, 3])
#
# # Python types will automatically be converted
# import datetime
# ws['A2'] = datetime.datetime.now()
#
# # Save the file
# wb.save("sample.xlsx")
############################################################3
# headers = ['name','price','type','num']
# columns = [['1','2'],['3','4'],['5','6'],['7','8']]
# for header, rows in zip(headers, columns):
#     print("{}: {}".format(header, ", ".join(rows)))
# name: 1, 2
# price: 3, 4
# type: 5, 6
# num: 7, 8
############################################################3