import traceback
try:
    a = 1 / 0
except Exception as e:
    print(traceback.format_exc())
print('end')