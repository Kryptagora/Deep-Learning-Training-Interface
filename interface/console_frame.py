import tkinter as tk
import tkinter.ttk as ttk


class ConsoleFrame():
	def __init__(self, frame=None):
		self.frame = frame
		self.pb = None
		self._create_widgets()

	def _create_widgets(self):
		self.train_console = tk.Text(self.frame, bg="white", fg="black", height=24, width=40)
		self.train_console.grid(row=0, column=0, columnspan=2)
		self.train_console.insert(tk.END, "Training Performance:\n")

		self.epoch_text = tk.StringVar()
		self.epoch_text.set("Epoch 0: ")
		tk.Label(self.frame, textvariable=self.epoch_text).grid(row=1, column=0, columnspan=2, sticky='w')

		self.pb = ttk.Progressbar(self.frame, orient="horizontal", mode="determinate")

		tk.Label(self.frame, text="Your Device:").grid(row=3, column=0, sticky='w', pady=(50,0))
		self.device_text = tk.StringVar()
		self.device_text.set("none")
		tk.Label(self.frame, textvariable=self.device_text, bg='brown', fg='white').grid(row=3, column=1, sticky='e',pady=(50,0))

	def push_text(self, text1:str=None, bold=False):
		self.train_console.insert(tk.END, text1, "bold" if bold else None)

	def delete_text(self):
		self.train_console.delete('1.0', tk.END)

	def spawn_progressbar(self, max_value):
		self.pb["value"] = 0
		self.pb["maximum"] = max_value
		self.pb.grid(row=2, column=0, columnspan=2, sticky="news")

	def change_max_value(self, max_value):
		self.pb["maximum"] = max_value
