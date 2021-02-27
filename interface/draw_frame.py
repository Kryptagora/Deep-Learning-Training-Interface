import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image, ImageDraw
import PIL
import numpy as np
from os.path import basename
import glob
import sys
sys.path.append('..')

from utils.predict import predict

class DrawFrame():
	def __init__(self, frame=None, main_window=None):
		self.frame = frame
		self.main_window = main_window
		self._xold = None
		self._yold = None
		self.canvas = None
		self.color = 'Black'
		self.thickness = 15
		self.tag = ['tag', '0']

		self.models = []
		self.image1 = PIL.Image.new('RGB', (400, 400), (255, 255, 255))
		self.draw = ImageDraw.Draw(self.image1)

		self._create_widgets()

	def _create_widgets(self):
		ttk.Label(self.frame, text="Select Model for Prediction:").grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='w')

		self.network_select = ttk.Combobox(self.frame, state="readonly", values=self.models)
		self.scan_model_dir()
		self.network_select.grid(row=1, column=0, columnspan=2, padx=5, sticky='news')

		ttk.Label(self.frame, text=" ").grid(row=2, column=0, columnspan=2, sticky='w')

		self.canvas = tk.Canvas(self.frame, width=400, height=400, bg='white')
		self.canvas.grid(row=3, column=0, columnspan=2, padx=5, pady=0)
		tk.Button(self.frame, text='Clear', bg='brown', fg='white', activebackground='brown4', activeforeground='white', command=self._clear).grid(row=4, column=0, padx=5, sticky='news')
		tk.Button(self.frame, text='Predict', bg='brown', fg='white', activebackground='brown4', activeforeground='white', command=self._save).grid(row=4, column=1, padx=5, sticky='news')
		self.canvas.bind('<ButtonRelease-1>', self._on_up)
		self.canvas.bind('<B1-Motion>', self._on_motion)

		tk.Label(self.frame, text="Predicted Letter:").grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky='w')
		self.predictedlabel = tk.StringVar()
		self.predictedlabel.set("-")
		tk.Label(self.frame, textvariable=self.predictedlabel, font=(None, 50)).grid(row=6, column=0, columnspan=2, sticky='w')


	def _clear(self):
		self.canvas.delete('all')
		self.image1 = PIL.Image.new('RGB', (400, 400), (255, 255, 255))
		self.draw = ImageDraw.Draw(self.image1)
		self.tag = ['tag', '0']

	def _on_up(self, event):
		self._xold = None
		self._yold = None
		self.tag = ['tag', str(int(self.tag[1])+1)]

	def _on_motion(self, event):
		tag = ''.join(self.tag)
		x1, y1 = (event.x - self.thickness), (event.y - self.thickness)
		x2, y2 = (event.x + self.thickness), (event.y + self.thickness)
		event.widget.create_oval(x1, y1, x2, y2, width=0, fill=self.color, tag=tag)

		if self._xold is not None and self._yold is not None:
			self.canvas.create_oval(x1, y1, x2, y2, width=0, fill=self.color, tag=tag)
			self.canvas.create_line(self._xold, self._yold, event.x, event.y, smooth=True, width=2*self.thickness, fill=self.color, tag=tag)
			self.draw.line([x1, y1, x2, y2],fill='black',width=self.thickness+5)

		self._xold = event.x
		self._yold = event.y


	def _save(self):
		filename = 'number.jpeg'
		image = self.image1.resize((28, 28)).convert('L')
		image = PIL.ImageOps.invert(image)

		# image.save(filename, 'JPEG')
		imgarray = np.asarray(image.getdata()).reshape((28,28))

		self.predictedlabel.set(str(predict(self.main_window, imgarray, self.network_select.get())))

	def scan_model_dir(self):
		self.models = [basename(x) for x in glob.glob('architecture/models/*.ckpt')]
		self.network_select.config(values=self.models)
		if len(self.models) != 0:
			self.network_select.current(0)
		return
