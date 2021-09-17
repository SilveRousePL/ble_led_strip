import PySimpleGUI as sg
import colorsys
import socket
import string
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.107', 45555)

def hsv2rgb(h,s,v):
    return '%02X%02X%02X' % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h/360.0,s/100.0,v/100.0))

def rgb2hsv(r,g,b):
    hsv = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    return (round(hsv[0]*360), round(hsv[1]*100), round(hsv[2]*100))

def send(message):
    return sock.sendto(message.encode('utf-8'), server_address)

# GUI
sg.ChangeLookAndFeel('Dark')
sg.SetOptions(element_padding=(0,0))

layout = [
    [
        sg.T('Hue '),
        sg.Slider(range=(0,360), default_value=0, orientation='h', size=(100, 12), enable_events=True, key='h_slider')
    ],
    [
        sg.T('Saturation '),
        sg.Slider(range=(0,100), default_value=100, orientation='h', size=(100, 12), enable_events=True, key='s_slider')
    ],
    [
        sg.T('Value '),
        sg.Slider(range=(0,100), default_value=100, orientation='h', size=(100, 12), enable_events=True, key='v_slider')
    ],
    [
        sg.Text(' ')
    ],
    [
        sg.InputText('FF0000', background_color='#ff0000', key='rgb_color', enable_events=True),
        sg.Button('PWR ON', key='pwr_on', size=(8, 1), button_color=('white', 'black')),
        sg.Button('PWR OFF', key='pwr_off', size=(8, 1), button_color=('white', 'black')),
        sg.Button('Send', button_color=('white', 'springgreen4'), key='send'),
        sg.Checkbox('Autosending', enable_events=True, key='autosending')
    ]
]

window = sg.Window("BLE LED Strip Client", layout, default_element_size=(10,1), text_justification='r', auto_size_text=False, auto_size_buttons=False, default_button_element_size=(12,1), finalize=True)

# Event loop
while True:
    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED:
        sock.close()
        exit(0)
    elif event == 'pwr_on':
        send(f'{{"device": "ELK-BLEDOM   ", "command": "power", "value": "1"}}')
    elif event == 'pwr_off':
        send(f'{{"device": "ELK-BLEDOM   ", "command": "power", "value": "0"}}')
    elif event[2:] == 'slider':
        rgb = hsv2rgb(values['h_slider'], values['s_slider'], values['v_slider'])
        window['rgb_color'].update(f'{str(rgb)}')
        window['rgb_color'].update(background_color=f'#{rgb}')
        #if self._window.SliderR.value() * 0.299 + self._window.SliderG.value() * 0.687 + self._window.SliderB.value() * 0.114 < 160:
        if values['autosending']:
            send(f'{{"device": "ELK-BLEDOM   ", "command": "color_rgb", "value": "{rgb}"}}')
    elif event == 'rgb_color':
        if len(values['rgb_color']) == 6 and all(c in string.hexdigits for c in values['rgb_color']):
            rgb = values['rgb_color']
            rgb_tuple = tuple(int(rgb[i:i+2], 16) for i in (0, 2, 4))
            hsv = rgb2hsv(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
            window['rgb_color'].update(f'{str(rgb).upper()}')
            window['rgb_color'].update(background_color=f'#{rgb}')
            window['h_slider'].update(value=hsv[0])
            window['s_slider'].update(value=hsv[1])
            window['v_slider'].update(value=hsv[2])
            if values['autosending']:
                send(f'{{"device": "ELK-BLEDOM   ", "command": "color_rgb", "value": "{rgb}"}}')

    elif event == 'send':
        rgb = hsv2rgb(values['h_slider'], values['s_slider'], values['v_slider'])
        send(f'{{"device": "ELK-BLEDOM   ", "command": "color_rgb", "value": "{rgb}"}}')
    elif event == 'autosending':
        if values['autosending']:
            window['send'].update(disabled=True)
        else:
            window['send'].update(disabled=False)
