import pickle
f = open('/root/pyProject/pkl/16/d16pka_.pkl','rb')
info = pickle.load(f)
print("aa")
print(info.keys())
print(info)
print(info['seq'])
