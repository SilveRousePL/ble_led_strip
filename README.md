# ble_led_strip
Wrapper for cheap LED strip with Bluetooth LE

---
**NOTE:** *This is early phase of development and not everything may be working properly.*

---
## First usage
First install dependencies:
```shell
pip3 install -r requirements.txt
```
Next, fill JSON config just like below: **[src/config.json]**:
```json
{
    "devices": {
        "ELK-BLEDOM": "XX:XX:XX:XX:XX:XX"
    }
}
```
And let's try to run it:
```shell
python3 main.py
```

## Examples
```json
{"device": "ELK-BLEDOM", "command": "power", "value": true}
{"device": "ELK-BLEDOM", "command": "brightness", "value": 100} // values: <0-100>
{"device": "ELK-BLEDOM", "command": "color_rgb", "value": "ffffff"} // values: rrggbb
{"device": "ELK-BLEDOM", "command": "effect", "value": "GRADIENT_RGBYCMW"} // values: the list below
```

### More effects
```
    RED                
    GREEN              
    BLUE               
    YELLOW             
    CYAN               
    MAGENTA            
    WHITE              
    JUMP_RGB           
    JUMP_RGBYCMW       
    GRADIENT_RGB       
    GRADIENT_RGBYCMW   
    GRADIENT_RED       
    GRADIENT_GREEN     
    GRADIENT_BLUE      
    GRADIENT_YELLOW    
    GRADIENT_CYAN      
    GRADIENT_MAGENTA   
    GRADIENT_WHITE     
    GRADIENT_RED_GREEN 
    GRADIENT_RED_BLUE  
    GRADIENT_GREEN_BLUE
    BLINK_RGBYCMW      
    BLINK_RED          
    BLINK_GREEN        
    BLINK_BLUE         
    BLINK_YELLOW       
    BLINK_CYAN         
    BLINK_MAGENTA      
    BLINK_WHITE        
```

## TODO
- More commands
- UDP listener and GUI client apps
- Integration with Google Assistant

## References
- https://github.com/arduino12/ble_rgb_led_strip_controller
