# blockbuster-exporter
This script allows exporting blockbuster mod player camera recording into blender, skipping camera tracking

## bbexp
CLI version of BB exporter. 
#### Usage:
```
bbexp.py bbRecordFilePath pythonOutputFilePath outputScale originX originY originZ
```
 - **bbRecordFilePath** - input recording file path
 - **pythonOutputFilePath** - output python script path
 - **outputScale** - Scale multiplier: moving by 1 block in minecraft would equate moving outputScale BU in blender
 - **originX** - Starting point X in BU. Keyframed camera path would start from here
 - **originY** - Starting point Y in BU. Keyframed camera path would start from here
 - **originZ** - Starting point Z in BU. Keyframed camera path would start from here

#### Required packages
nbtlib, tkinter

## bbexp_gui
GUI version of BB exporter.
#### Required packages
nbtlib

## Usage
1. Install blockbuster mod
2. After recording, locate recording file inside ```\.minecraft\saves\*savename*\blockbuster\records\```
3. Use located file as input file, specify other settings as needed and process the file
4. Go in blender, select camera that you want to animate
5. Open and run generated script
6. New camera will be animated according to blockbuster recording data

## Limitations
1. Due to blockbuster mod recording every tick, output animation is 20 fps only. 
Possible solution is scaling up camera animation or use AI upscaler on output video TODO: builtin interpolation
