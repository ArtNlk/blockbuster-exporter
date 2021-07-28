import os
import tkinter as tk
from tkinter import filedialog as fd
import pygubu

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

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "main.ui")

class MainApp:
	def __init__(self, master=None):
		# build ui
		self.mainWindow = tk.Tk() if master is None else tk.Toplevel(master)
		self.mainFrame = tk.Frame(self.mainWindow)
		self.bbPathLabel = tk.Label(self.mainFrame)
		self.bbPathLabel.configure(text='Blockbuster file path:')
		self.bbPathLabel.grid(column='0', padx='10', pady='5', row='0', sticky='e')
		self.entry2 = tk.Entry(self.mainFrame)
		self.bb_file_path = tk.StringVar(value='')
		self.entry2.configure(relief='sunken', textvariable=self.bb_file_path, width='50')
		self.entry2.grid(column='1', padx='10', pady='5', row='0')
		self.bbPathOpenBtn = tk.Button(self.mainFrame)
		self.bbPathOpenBtn.configure(text='Open...')
		self.bbPathOpenBtn.grid(column='2', pady='5', row='0')
		self.bbPathOpenBtn.configure(command=self.openBBFilePicker)
		self.outputPathLabel = tk.Label(self.mainFrame)
		self.outputPathLabel.configure(justify='left', text='Output file path:')
		self.outputPathLabel.grid(column='0', padx='10', pady='5', row='1', sticky='e')
		self.entry3 = tk.Entry(self.mainFrame)
		self.output_file_path = tk.StringVar(value='')
		self.entry3.configure(textvariable=self.output_file_path, width='50')
		self.entry3.grid(column='1', pady='5', row='1')
		self.outputPathOpenBtn = tk.Button(self.mainFrame)
		self.outputPathOpenBtn.configure(text='Choose...')
		self.outputPathOpenBtn.grid(column='2', pady='5', row='1')
		self.outputPathOpenBtn.configure(command=self.openOutputFilePicker)
		self.scaleLabel = tk.Label(self.mainFrame)
		self.scaleLabel.configure(compound='top', font='TkTextFont', text='Output scale:')
		self.scaleLabel.grid(column='0', padx='10', pady='5', row='2', sticky='e')
		self.spinbox1 = tk.Spinbox(self.mainFrame)
		self.output_scale = tk.DoubleVar(value='')
		self.spinbox1.configure(from_='-1000000', increment='1', textvariable=self.output_scale, to='1000000')
		self.spinbox1.configure(width='7', wrap='false')
		self.spinbox1.grid(column='1', padx='10', pady='5', row='2', sticky='w')
		self.originXLabel = tk.Label(self.mainFrame)
		self.originXLabel.configure(text='Origin X:')
		self.originXLabel.grid(column='0', padx='10', pady='5', row='3', sticky='e')
		self.label8 = tk.Label(self.mainFrame)
		self.label8.configure(text='Origin Y:')
		self.label8.grid(column='0', padx='10', pady='5', row='4', sticky='e')
		self.label9 = tk.Label(self.mainFrame)
		self.label9.configure(text='Origin Z:')
		self.label9.grid(column='0', padx='10', pady='5', row='5', sticky='e')
		self.originXspinbox = tk.Spinbox(self.mainFrame)
		self.originX = tk.DoubleVar(value='')
		self.originXspinbox.configure(from_='-1000000', justify='left', textvariable=self.originX, to='1000000')
		self.originXspinbox.grid(column='1', padx='10', pady='5', row='3', sticky='w')
		self.originYspinbox = tk.Spinbox(self.mainFrame)
		self.originY = tk.DoubleVar(value='')
		self.originYspinbox.configure(from_='-1000000', textvariable=self.originY, to='1000000')
		self.originYspinbox.grid(column='1', padx='10', pady='5', row='4', sticky='w')
		self.originZspinbox = tk.Spinbox(self.mainFrame)
		self.originZ = tk.DoubleVar(value='')
		self.originZspinbox.configure(from_='-1000000', textvariable=self.originZ, to='1000000')
		self.originZspinbox.grid(column='1', padx='10', pady='5', row='5', sticky='w')
		self.processButton = tk.Button(self.mainFrame)
		self.processButton.configure(text='Process', width='40')
		self.processButton.grid(column='1', pady='5', row='6')
		self.processButton.configure(command=self.processFile)
		self.mainFrame.configure(height='576', width='1024')
		self.mainFrame.grid(column='0', row='0')
		self.mainWindow.configure(height='576', width='1024')
		self.mainWindow.geometry('1024x576')
		self.mainWindow.maxsize(1024, 576)
		self.mainWindow.minsize(1024, 576)
		self.mainWindow.title('Blockbuster exporter')
		
		self.output_scale.set(1)
		self.originX.set(0)
		self.originY.set(0)
		self.originZ.set(0)
		
		# Main widget
		self.mainwindow = self.mainWindow
	
	def openBBFilePicker(self):
		self.bb_file_path.set(fd.askopenfilename(filetypes=[("Blockbuster record files", ".dat .nbt")]));
		
	def openOutputFilePicker(self):
		self.output_file_path.set(fd.asksaveasfilename(filetypes=[("Python script files", ".py")],defaultextension='.py'));

	def processFile(self):
		processRecording(self.bb_file_path.get(),self.output_file_path.get(),self.output_scale.get(),self.originX.get(),self.originY.get(),self.originZ.get());

	def run(self):
		self.mainwindow.mainloop()

def processRecording(recordingPath, outputScriptPath, scale, oX,oY,oZ):
	print("Exporting from {} to {}\nScale:{}\nOrigin:\n X:{}\n Y:{}\n Z:{}\n".format(recordingPath,outputScriptPath,scale,oX,oY,oZ))
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

if __name__ == '__main__':
	app = MainApp()
	app.run()

