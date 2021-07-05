import ctypes
from ctypes import wintypes
import time
import serial
import time
import serial.tools.list_ports

ports = [comport.device for comport in serial.tools.list_ports.comports()]

if(len(ports) == 1):
    ser = serial.Serial(ports[0], 9600, timeout=0)

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

flag_F = None
flag_M = None
flag_T = None
flag_U = None
flag_O = None
flag_L = None
flag_I = None
flag_K = None
flag_V = None
flag_B = None

while True:
    try:
        data = ser.readline().decode()
        if(len(data) == 6):
            if(data[0] == '1'):
                PressKey(T_KEY)
                flag_T = True
                flag_U = False
            elif(data[0] == '2'):
                PressKey(U_KEY)
                flag_T = False
                flag_U = True
            
            if(flag_T == True and flag_U == False):
                ReleaseKey(U_KEY)
            elif(flag_U == True and flag_T == False):
                ReleaseKey(T_KEY)  
            if(data[0] == '0'):
                if(flag_T == True):
                    ReleaseKey(T_KEY)
                elif(flag_U == True):
                    ReleaseKey(U_KEY)
            
            if(data[1] == '1'):
                PressKey(I_KEY)
                flag_I = True
                flag_K = False
            elif(data[1] == '2'):
                PressKey(K_KEY)
                flag_I = False
                flag_K = True
            
            if(flag_I == True and flag_K == False):
                ReleaseKey(K_KEY)
            elif(flag_K == True and flag_I == False):
                ReleaseKey(I_KEY)  
            if(data[1] == '0'):
                if(flag_I == True):
                    ReleaseKey(I_KEY)
                elif(flag_K == True):
                    ReleaseKey(K_KEY)
            
            if(data[2] == '1'):
                PressKey(O_KEY)
                flag_O = True
                flag_L = False
            elif(data[2] == '2'):
                PressKey(L_KEY)
                flag_O = False
                flag_L = True
            
            if(flag_O == True and flag_L == False):
                ReleaseKey(L_KEY)
            elif(flag_L == True and flag_O == False):
                ReleaseKey(O_KEY)  
            if(data[2] == '0'):
                if(flag_O == True):
                    ReleaseKey(O_KEY)
                elif(flag_L == True):
                    ReleaseKey(L_KEY)
            
            if(data[3] == '1'):
                PressKey(V_KEY)
                flag_V = True

            if(data[3] == '2' and flag_V == True):
                ReleaseKey(V_KEY)
                flag_V = False

            if(data[4] == '1'):
                PressKey(M_KEY)
                flag_M = True

            if(data[4] == '2' and flag_M == True):
                ReleaseKey(M_KEY)
                flag_M = False

            if(data[5] == '1'):
                PressKey(B_KEY)
                flag_B = True

            if(data[5] == '2' and flag_B == True):
                ReleaseKey(B_KEY)
                flag_B = False
            
    except ser.SerialTimeoutException:
        print('Data could not be read')        