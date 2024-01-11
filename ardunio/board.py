import serial
import serial.tools.list_ports
import time

import requests




def rotate_spring(arduino,timeout=10):
    _=arduino.read_all()#clear buffer
    arduino.write(str.encode("R-S*2\n"))
    for i in range(0,timeout):
        time.sleep(1)# in second
        status = arduino.readline()
        #print(status)
        string=status.decode()
        if string.isdigit():
            return int(string)
        #print(string)
    
    #print("Time out")
    return 400

def get_depth(arduino,timeout=10,max_depth=9): # 9 inch
    _=arduino.read_all()#clear buffer
    arduino.write(str.encode("G-D*2\n"))
    for i in range(0,timeout):
        time.sleep(1)
        status = arduino.readline()
        string=status.decode()
        if string[0:-1].isdigit():
            return int(string)
    return "error"




def init():
    ports=serial.tools.list_ports.comports()
    ports=sorted(ports)
    print("*********** Select arduino Board Port **************")
    i=0

    for port, desc, hwid in ports:
        print(f"[{i}] {port}: {desc} [{hwid}]")
        i+=1

    option=int(input(">> "))
    if option>=i:
        print("[!] Please selet a valid option")
        exit()
    port=ports[option][0]
    print(f"[*] Selected {port} ...")
    print(f"[-] Enter the bud rate ( Recomended: 57600 )")
    bud=int(input(">>"))
    arduino = serial.Serial(port=port,   baudrate=bud, timeout=.1)
    time.sleep(2)    
    return arduino
    
def quantize_percentage(per):
    floor_val=[0,5,25,50,75,100]
    quantized_value = min(floor_val, key=lambda x: abs(x - per))
    return quantized_value


if __name__=="__main__":
    arduino=init()
    api_key=input("(Enter API key) >> ")
    prev_depth=0
    while(True):
        res=get_depth(arduino)
        if type(res)==str:
            print("[!] Err Couldnot fetch data from ardunio")
            continue
        
        percentage=100-res/9*100
        q_val=quantize_percentage(percentage)
        print(f"[-] Depth in inch : {res}, Quantized % : {q_val}")
        if prev_depth==q_val:
            continue

        prev_depth=q_val
        req_data={"api_key":api_key,"status":q_val}
        res=requests.post("http://127.0.0.1:8080/api/inventory", data=req_data)
        if(res.status_code==200):
            print("[+] Sucessfully updated")
        else:
            print("[!] Error communicatiing with server")
        time.sleep(5)



