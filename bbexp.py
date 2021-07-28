import nbtlib
import sys
	
HEADER = r"""import bpy
myobj = bpy.context.object
myobj.animation_data_clear()
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = {}
################################################
"""

FRAME_SEGMENT = """
bpy.context.scene.frame_set({})

myobj.location.x = {:.10f}
myobj.location.y = {:.10f}
myobj.location.z = {:.10f}

myobj.rotation_euler.x = {:.10f}
myobj.rotation_euler.y = 0
myobj.rotation_euler.z = {:.10f}

myobj.keyframe_insert(data_path="location")
myobj.keyframe_insert(data_path="rotation_euler")
#################################################
"""

HELP_TEXT = """
Parameters: inputFilePath outputFilePath scale originX originY originZ
"""
	
def processRecording(recordingPath, outputScriptPath, scale, oX,oY,oZ):
	nbt_file = nbtlib.load(recordingPath)
	
	num_frames = len(nbt_file.root['Frames'])
	
	x_offset = nbt_file.root['Frames'][0]['X'] * scale - oX
	y_offset = -(nbt_file.root['Frames'][0]['Z'] * scale) - oY
	z_offset = nbt_file.root['Frames'][0]['Y'] * scale - oZ
	
	with open(outputScriptPath,'w+') as output_file:
		output_file.write(HEADER.format(num_frames))
		for i in range(0,num_frames):
			x = nbt_file.root['Frames'][i]['X'] * scale - x_offset
			y = -(nbt_file.root['Frames'][i]['Z'] * scale) - y_offset
			z = nbt_file.root['Frames'][i]['Y'] * scale - z_offset
			
			cam_pitch = (-nbt_file.root['Frames'][i]['RY'] % 360.0 + 90) * 0.0174533
			cam_yaw = -(nbt_file.root['Frames'][i]['RX'] % 360.0 + 180) * 0.0174533
			output_file.write(FRAME_SEGMENT.format(i,x,y,z,cam_pitch,cam_yaw))

if __name__ == "__main__":
	print(len(sys.argv))
	if len(sys.argv) < 7:
		print(HELP_TEXT)
		exit(0)
	input_path = sys.argv[1]
	output_path = sys.argv[2]
	scale = float(sys.argv[3])
	oX = float(sys.argv[4])
	oY = float(sys.argv[5])
	oZ = float(sys.argv[6])
	
	print("Exporting from {} to {}\nScale:{}\nOrigin:\n X:{}\n Y:{}\n Z:{}\n".format(input_path,output_path,scale,oX,oY,oZ))
	
	processRecording(input_path,output_path, scale, oX,oY,oZ)