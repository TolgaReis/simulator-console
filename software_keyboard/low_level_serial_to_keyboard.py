import ctypes
from ctypes import wintypes
import time
import serial
import time
import serial.tools.list_ports
from flag import Flag

user32 = ctypes.WinDLL('user32', use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
MAPVK_VK_TO_VSC = 0
# msdn.microsoft.com/en-us/library/dd375731
wintypes.ULONG_PTR = wintypes.WPARAM
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))
LPINPUT = ctypes.POINTER(INPUT)

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

T_KEY = 0x54
U_KEY = 0x55

# M: throttle 
# F: break
M_KEY = 0x4D
F_KEY = 0x46

# V: steer right
# B: steer left
V_KEY = 0x56
B_KEY = 0x42

O_KEY = 0x4F
L_KEY = 0x4C

I_KEY = 0x49
K_KEY = 0x4B

H_KEY = 0x48
Y_KEY = 0x59

ports = [comport.device for comport in serial.tools.list_ports.comports()]

while len(ports) < 1:
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    if len(ports) >= 1:
        break

while True:
    try:
        ser = serial.Serial(port = ports[0],
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)
        break
    except:
        pass

key_flag = Flag

while True:
    try:
        data = ser.readline().decode()
        if(len(data) == 8):
            if(data[0] == '1'):
                PressKey(T_KEY)
                key_flag.T = True
                key_flag.U = False
            elif(data[0] == '2'):
                PressKey(U_KEY)
                key_flag.T = False
                key_flag.U = True
            
            if(key_flag.T == True and key_flag.U == False):
                ReleaseKey(U_KEY)
            elif(key_flag.U == True and key_flag.T == False):
                ReleaseKey(T_KEY)  
            if(data[0] == '0'):
                if(key_flag.T == True):
                    ReleaseKey(T_KEY)
                elif(key_flag.U == True):
                    ReleaseKey(U_KEY)
            
            if(data[1] == '1'):
                PressKey(I_KEY)
                key_flag.I = True
                key_flag.K = False
            elif(data[1] == '2'):
                PressKey(K_KEY)
                key_flag.I = False
                key_flag.K = True
            
            if(key_flag.I == True and key_flag.K == False):
                ReleaseKey(K_KEY)
            elif(key_flag.K == True and key_flag.I == False):
                ReleaseKey(I_KEY)  
            if(data[1] == '0'):
                if(key_flag.I == True):
                    ReleaseKey(I_KEY)
                elif(key_flag.K == True):
                    ReleaseKey(K_KEY)
            
            if(data[2] == '1'):
                PressKey(O_KEY)
                key_flag.O = True
                key_flag.L = False
            elif(data[2] == '2'):
                PressKey(L_KEY)
                key_flag.O = False
                key_flag.L = True
            
            if(key_flag.O == True and key_flag.L == False):
                ReleaseKey(L_KEY)
            elif(key_flag.L == True and key_flag.O == False):
                ReleaseKey(O_KEY)  
            if(data[2] == '0'):
                if(key_flag.O == True):
                    ReleaseKey(O_KEY)
                elif(key_flag.L == True):
                    ReleaseKey(L_KEY)
            
            if(data[3] == '1'):
                PressKey(V_KEY)
                key_flag.V = True

            if(data[3] == '2' and key_flag.V == True):
                ReleaseKey(V_KEY)
                key_flag.V = False

            if(data[4] == '1'):
                PressKey(M_KEY)
                key_flag.M = True

            if(data[4] == '2' and key_flag.M == True):
                ReleaseKey(M_KEY)
                key_flag.M = False

            if(data[5] == '1'):
                PressKey(B_KEY)
                key_flag.B = True

            if(data[5] == '2' and key_flag.B == True):
                ReleaseKey(B_KEY)
                key_flag.B = False
            
    except:
        try:
            ser = serial.Serial(port = ports[0],
                            baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)        
        except:
            pass
