'''
  * author 冯自立
  * created at : 2023-10-11 10:42:37
  * description: 
'''

from utils.app import startKakaAnimation

if __name__ == '__main__':
    '''for i in range(50000):
        import os
        if os.path.exist("stop"):
            print("existing stop file")
            time.sleep(0.1)
            continue
        with open("stop","w") as fl:
            fl.write("stop")
            print("write success.")
        import time
        time.sleep(0.2)'''
    startKakaAnimation()
