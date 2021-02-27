import tkinter as tk
import tkinter.ttk as ttk
import sys
sys.path.append('..')


class NetworkFrame():
	def __init__(self, frame=None, train_function=None, main_window=None):
		self.frame = frame
		self.train_function = train_function
		self.main_window = main_window

		self.stop_train = False
		self.stop_save = False

		self._create_widgets()

	def _create_widgets(self):
		tk.Label(self.frame, text="Select Dataset to train with:").grid(row=0, column=0, columnspan=2, pady=5, sticky='w')
		self.dataset_select = ttk.Combobox(self.frame, state="readonly", values=["MNIST", "EMNIST"])
		self.dataset_select.current(0)
		self.dataset_select.grid(row=1, column=0, columnspan=2, pady=5, sticky='news')

		tk.Label(self.frame, text="Select Architecture to train with:").grid(row=2, column=0, columnspan=2, pady=5, sticky='w')
		self.architecture_select = ttk.Combobox(self.frame, state="disabled", values=["default-CNN", "custom-CNN"])
		self.architecture_select.current(0)
		self.architecture_select.grid(row=3, column=0, columnspan=2, pady=5, sticky='news')

		tk.Label(self.frame, text="Hyperparameters:", bg='black', fg='white').grid(row=4, column=0, columnspan=2, pady=(25,0), sticky='news')

		# Batch Size
		tk.Label(self.frame, text="Batch Size:").grid(row=5, column=0, columnspan=2, pady=5, sticky='w')
		self.bs = tk.IntVar(value=500)
		bs_spinbox = tk.Spinbox(self.frame, textvariable=self.bs, wrap=True, width=10)
		bs_spinbox['to'] = 500
		bs_spinbox['from'] = 10
		bs_spinbox['increment'] = 10
		bs_spinbox.grid(row=6, column=0, columnspan=2, sticky='news')

		# Epochs
		tk.Label(self.frame, text="Number of Epochs:").grid(row=7, column=0, columnspan=2, pady=5, sticky='w')
		self.epochs = tk.IntVar(value=4)
		epo_spinbox = tk.Spinbox(self.frame, textvariable=self.epochs, wrap=True, width=10)
		epo_spinbox['to'] = 20
		epo_spinbox['from'] = 1
		epo_spinbox['increment'] = 1
		epo_spinbox.grid(row=8, column=0, columnspan=2, sticky='news')

		# Learning Rate
		tk.Label(self.frame, text="Learning Rate:").grid(row=9, column=0, columnspan=2, pady=5, sticky='w')
		self.lr = tk.DoubleVar(value=0.001)
		lr_spinbox = tk.Spinbox(self.frame, textvariable=self.lr, wrap=True, width=10)
		lr_spinbox['to'] = 0.2
		lr_spinbox['from'] = 0.00000000000
		lr_spinbox['increment'] = 0.001
		self.lr.set(0.001)
		lr_spinbox.grid(row=10, column=0, columnspan=2, sticky='news')

		# Momentum Term
		tk.Label(self.frame, text="Momentum Term:").grid(row=11, column=0, columnspan=2, pady=5, sticky='w')
		self.momentum = tk.DoubleVar(value=0.5)
		mom_spinbox = tk.Spinbox(self.frame, textvariable=self.momentum, wrap=True, width=10)
		mom_spinbox['to'] = 0.2
		mom_spinbox['from'] = 0.0
		mom_spinbox['increment'] = 0.01
		mom_spinbox.grid(row=12, column=0, columnspan=2, sticky='news')

		# Modelname
		tk.Label(self.frame, text="Save model as:").grid(row=13, column=0, columnspan=2, pady=5, sticky='w')
		self.modelname = tk.StringVar(value='randomModel')
		modelnameentry = tk.Entry(self.frame, textvariable=self.modelname, width=10)
		modelnameentry.grid(row=14, column=0, columnspan=2, sticky='news')

		tk.Label(self.frame, text="").grid(row=15, column=0, columnspan=2, pady=(25,0), sticky='news')

		self.train_button = tk.Button(self.frame, text="Train", bg="brown", fg="white", activebackground="brown4", activeforeground="white", command=lambda:self.train_function(self.main_window))
		self.train_button.grid(row=16, column=0, columnspan=2, padx=25, pady=5, sticky='news')

		self.stop_training = tk.Button(self.frame, text="Stop", bg="brown", fg="white", activebackground="brown4", activeforeground="white", command=self.stop_training)
		self.stop_training.grid(row=17, column=0, columnspan=2, padx=25, pady=5, sticky='news')

		self.stop_save = tk.Button(self.frame, text="Stop & Save", bg="brown", fg="white", activebackground="brown4", activeforeground="white", command=self.stop_and_save)
		self.stop_save.grid(row=18, column=0, columnspan=2, padx=25, pady=5, sticky='news')


	def stop_training(self):
		self.stop_train=True


	def stop_and_save(self):
		self.stop_save=True


	def reset_params(self):
	    self.train_button.config(state='disabled')
	    self.stop_train = False
	    self.stop_save = False
