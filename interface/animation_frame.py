import matplotlib
matplotlib.use('TkAgg')

from matplotlib import animation, figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
plt.style.use('seaborn-bright')
# matplotlib.pyplot.xkcd(scale=1, length=100, randomness=2)



class AnimationFrame():
	def __init__(self, frame=None, bgcolor=None):
		self.frame = frame
		self.bgcolor = bgcolor
		self.loss = 0
		self.animate_start = True
		self._create_widgets()

	def _create_widgets(self):
		# First Plot (local loss)
		self.fig = figure.Figure(figsize=(6, 6), dpi=100)
		self.fig.patch.set_facecolor(self.bgcolor)
		self.ax = self.fig.add_subplot(1, 1, 1)
		self.xs = []
		self.ys = []

		self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
		self.canvas.get_tk_widget().grid(column=0, row=1)

		# Global loss (second plot)
		self.fig2 = figure.Figure(figsize=(6, 2), dpi=100)
		self.fig2.patch.set_facecolor(self.bgcolor)
		self.ax2 = self.fig2.add_subplot(1, 1, 1)
		self.xs_global = []
		self.ys_global = []

		self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.frame)
		self.canvas2.get_tk_widget().grid(column=0, row=2)


		self.animate()
		self.animate2()


	def animate(self):
		self.xs = self.xs[-100:]
		self.ys = self.ys[-100:]
		self.ax.clear()
		self.ax.plot(self.xs, self.ys, color='red')
		self.canvas.draw()

	def animate2(self):
		self.xs_global = self.xs_global[-10000:]
		self.ys_global = self.ys_global[-10000:]
		self.ax2.clear()
		self.ax2.plot(self.xs_global, self.ys_global, color='red')
		self.canvas2.draw()

	def stop_animation(self):
		'''Stop all animations'''
		self.xs = []
		self.ys = []
		self.ax.clear()
		self.ax.plot(self.xs, self.ys)
		self.canvas.draw()

		self.xs_global = []
		self.ys_global = []
		self.ax2.clear()
		self.ax2.plot(self.xs, self.ys)
		self.canvas2.draw()
