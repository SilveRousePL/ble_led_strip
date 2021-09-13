from enum import IntEnum

class CommandId(IntEnum):
    BRIGHTNESS          = 0x01
    SPEED               = 0x02
    EFFECT              = 0x03
    POWER               = 0x04
    COLOR               = 0x05
    SENSITIVITY         = 0x07
    PIN_ORDER_BY_ID     = 0x08
    PIN_ORDER_BY_COLOR  = 0x81
    
class CommandSubIdEffect(IntEnum):
    RED                 = 0x80
    GREEN               = 0x81
    BLUE                = 0x82
    YELLOW              = 0x83
    CYAN                = 0x84
    MAGENTA             = 0x85
    WHITE               = 0x86
    JUMP_RGB            = 0x87
    JUMP_RGBYCMW        = 0x88
    GRADIENT_RGB        = 0x89
    GRADIENT_RGBYCMW    = 0x8a
    GRADIENT_RED        = 0x8b
    GRADIENT_GREEN      = 0x8c
    GRADIENT_BLUE       = 0x8d
    GRADIENT_YELLOW     = 0x8e
    GRADIENT_CYAN       = 0x8f
    GRADIENT_MAGENTA    = 0x90
    GRADIENT_WHITE      = 0x91
    GRADIENT_RED_GREEN  = 0x92
    GRADIENT_RED_BLUE   = 0x93
    GRADIENT_GREEN_BLUE = 0x94
    BLINK_RGBYCMW       = 0x95
    BLINK_RED           = 0x96
    BLINK_GREEN         = 0x97
    BLINK_BLUE          = 0x98
    BLINK_YELLOW        = 0x99
    BLINK_CYAN          = 0x9a
    BLINK_MAGENTA       = 0x9b
    BLINK_WHITE         = 0x9c
    
class CommandSubIdPower(IntEnum):
    OFF = 0x00
    ON  = 0x01

class CommandSubIdColor(IntEnum):
    GRAYSCALE   = 0x01  # First argument is value (0x00-0x64)
    TEMPERATURE = 0x02  # Second argument is value (0x00-0x64)
    RGB         = 0x03  # All three arguments are colors (RGB)


class MessageComposer:
    def __init__(self) -> None:
        self.command_id = 0
        self.subcommand_id = 0
        self.arg1 = 0
        self.arg2 = 0
        self.arg3 = 0

    def compose(self):
        return bytearray(
            [0x7e,
             0x00,
             self.command_id,
             self.subcommand_id,
             self.arg1,
             self.arg2,
             self.arg3,
             0x00,
             0xef
            ]
        )

    def brightness(self, value: int):
        self.command_id = CommandId.BRIGHTNESS
        self.subcommand_id = int(value)
        return self.compose()

    def speed(self, value: int):
        self.command_id = CommandId.SPEED
        self.subcommand_id = int(value)
        return self.compose()
    
    def effect(self, value: str):
        self.command_id = CommandId.EFFECT
        self.subcommand_id = CommandSubIdEffect[value.upper()].value
        return self.compose()
    
    def power(self, value: bool):
        self.command_id = CommandId.POWER
        self.subcommand_id = int(value)
        return self.compose()

    def color_grayscale(self, value: int):
        self.command_id = CommandId.COLOR
        self.subcommand_id = CommandSubIdColor.GRAYSCALE
        self.arg1 = int(value)
        self.arg2 = 0
        self.arg3 = 0
        return self.compose()

    def color_temperature(self, value: int):
        self.command_id = CommandId.COLOR
        self.subcommand_id = CommandSubIdColor.TEMPERATURE
        self.arg1 = 0
        self.arg2 = int(value)
        self.arg3 = 0
        return self.compose()

    def color_rgb(self, value: str):
        self.command_id = CommandId.COLOR
        self.subcommand_id = CommandSubIdColor.RGB
        value = bytearray.fromhex(value)
        self.arg1 = value[0]
        self.arg2 = value[1]
        self.arg3 = value[2]
        return self.compose()

    def raw(self, value: str):
        return bytearray.fromhex(value)
