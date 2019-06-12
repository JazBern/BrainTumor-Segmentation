
#import modules-----------------------------------------------------------------------------------------
from tkinter import *
from tkinter import ttk
import tkinter as tk
import webbrowser  
from tkinter import filedialog
from tkinter import messagebox as box
from tkinter.filedialog import askopenfilename
import time
import os
import SimpleITK as sitk
import numpy as np
from keras.models import Model,load_model
from keras.layers.advanced_activations import PReLU
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers import Dropout,GaussianNoise, Input,Activation
from keras.layers.normalization import BatchNormalization
from keras.layers import  Conv2DTranspose,UpSampling2D,concatenate,add
from keras.optimizers import SGD
from keras.metrics import categorical_accuracy
import keras.backend as K
from keras.utils import to_categorical
import random
import json
from glob import glob
from sklearn.utils import class_weight
from keras.models import model_from_json,load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import  ModelCheckpoint,Callback,LearningRateScheduler
import cv2
import random, shutil
from zipfile import ZipFile
from PIL import Image
import matplotlib.pyplot as plt
#--------------------------------------------------------------------------------------------------------

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#--------------------------------------------------------------------------------------------------------

#-------------------Dice score calculation---------------------------------------------------------------
def dice_coef_np(y_true, y_pred, num_classes, smooth = 0.4):
    """
    :param y_true: sparse labels
    :param y_pred: sparse labels
    :param num_classes: number of classes
    :return:
    """
    y_true = y_true.astype(int)
    y_pred = y_pred.astype(int)
    y_true = y_true.flatten()
    y_true = one_hot(y_true, num_classes)
    y_pred = y_pred.flatten()
    y_pred = one_hot(y_pred, num_classes)
    intersection = np.sum(y_true * y_pred, axis=0)
    return (2. * intersection + smooth) / (np.sum(y_true, axis=0) + np.sum(y_pred, axis=0) + smooth)
  
  
def one_hot(y, num_classees):
    y_ = np.zeros([len(y), num_classees])
    y_[np.arange(len(y)), y] = 1
    return y_
#-------------------------------------------------------------------------------------------------------

#------------------ Designing window for registration---------------------------------------------------
def register():
	global register_screen
	register_screen = Toplevel(main_screen)
	register_screen.title("Register")
	register_screen.geometry("300x250")

	global username
	global password
	global username_entry
	global password_entry
	username = StringVar()
	password = StringVar()

	Label(register_screen, text="Please enter details below").pack()
	Label(register_screen, text="").pack()
	username_lable = Label(register_screen, text="Username * ")
	username_lable.pack()
	username_entry = Entry(register_screen, textvariable=username)
	username_entry.pack()
	password_lable = Label(register_screen, text="Password * ")
	password_lable.pack()
	password_entry = Entry(register_screen, textvariable=password, show='*')
	password_entry.pack()
	Label(register_screen, text="").pack()
	Button(register_screen, text="Register", width=10, height=1, bg="black", fg="white", command = register_user).pack()
#---------------------------------------------------------------------------------------------------------

# -------------------Designing window for login-----------------------------------------------------------
def login():
	global login_screen
	login_screen = Toplevel(main_screen)
	login_screen.title("Login")
	login_screen.geometry("300x250")
	Label(login_screen, text="Please enter details below to login").pack()
	Label(login_screen, text="").pack()

	global username_verify
	global password_verify

	username_verify = StringVar()
	password_verify = StringVar()

	global username_login_entry
	global password_login_entry

	Label(login_screen, text="Username * ").pack()
	username_login_entry = Entry(login_screen, textvariable=username_verify)
	username_login_entry.pack()
	Label(login_screen, text="").pack()
	Label(login_screen, text="Password * ").pack()
	password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
	password_login_entry.pack()
	Label(login_screen, text="").pack()
	Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
#----------------------------------------------------------------------------------------------------------

#------------------ Implementing event on register button--------------------------------------------------
def register_user():

	username_info = username.get()
	password_info = password.get()

	file = open(username_info, "w")
	file.write(username_info + "\n")
	file.write(password_info)
	file.close()

	username_entry.delete(0, END)
	password_entry.delete(0, END)

	Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
	register_screen.destroy
#---------------------------------------------------------------------------------------------------------	

#----------------- Implementing event on login button-----------------------------------------------------
def login_verify():
	username1 = username_verify.get()
	password1 = password_verify.get()
	username_login_entry.delete(0, END)
	password_login_entry.delete(0, END)

	list_of_files = os.listdir()
	if username1 in list_of_files:
		file1 = open(username1, "r")
		verify = file1.read().splitlines()
		if password1 in verify:
			login_sucess()

		else:
			password_not_recognised()

	else:
		user_not_found()
#---------------------------------------------------------------------------------------------------------

#-------------------Designing popup for login success-----------------------------------------------------
def login_sucess():
	global login_success_screen
	login_success_screen = Toplevel(login_screen)
	login_success_screen.title("BRATS")
	login_success_screen.geometry("800x500")
	login_success_screen.configure(background = 'black')

	label = Label(login_success_screen, text = 'BRATS', fg = 'light green',bg = 'black', font = (None, 30), height = 2)
	label.pack(side = TOP)

	frame1 = Frame(login_success_screen, bg='black') 
	frame2 = Frame(login_success_screen, bg='black') 
	frame3 = Frame(login_success_screen, bg='black') 
	global name
	def OpenFile():
		global name
		name = askopenfilename(initialdir="/Home",filetypes =(("image File", "*.png"),("All Files","*.*")),title = "Choose a file.")
		v.set(name)
	
	def uploading():
		if name != "":
			popup = tk.Toplevel()
			tk.Label(popup, text="uploading").grid(row=0,column=0)
			progress=ttk.Progressbar(popup,orient=HORIZONTAL,length=100,mode='determinate')
			progress.grid(row=1, column=0)
			progress['value']=50
			login_success_screen.update_idletasks()
			time.sleep(0.8)
			progress['value']=75
			login_success_screen.update_idletasks()
			time.sleep(0.8)
			progress['value']=99
			login_success_screen.update_idletasks()
			time.sleep(0.8)
			tk.Label(popup, text="uploaded").grid(row=0,column=0)
			progress['value']=99
			login_success_screen.update_idletasks()
			time.sleep(0.8)
			popup.destroy()

	#The given input file is segmented using the model trained using Unet deeplabV3+ architecture and is saved into a folder.
	def predicting():
		popup = tk.Toplevel()
		tk.Label(popup, text="processing").grid(row=0,column=0)
		progress=ttk.Progressbar(popup,orient=HORIZONTAL,length=100,mode='determinate')
		progress.grid(row=1, column=0)

		progress['value']=5
		login_success_screen.update_idletasks()
		time.sleep(0.8)

		m2 = load_model('/home/user/BrainTumor-Segmentation/final.h5')
		if os.path.exists("abc/"):
			shutil.rmtree("abc/")
		with ZipFile(name, 'r') as zipf: 
			zipf.extractall('abc') 
			f=os.listdir('abc')
		path = "abc/" + f[0]

		p = os.listdir(path)
		p.sort(key=str.lower)
		arr = []

		progress['value']=25
		login_success_screen.update_idletasks()
		time.sleep(0.8)

		save = '/home/user/BrainTumor-Segmentation/Output/'
		if os.path.exists(save):
			shutil.rmtree(save)
		os.makedirs(save)

		destin = '/home/user/BrainTumor-Segmentation/Output_Segmented/'
		if os.path.exists(destin):
			shutil.rmtree(destin)
		os.makedirs(destin)

		dice_whole = []

		in_img = '/home/user/BrainTumor-Segmentation/Data/Plots/'
		if os.path.exists(in_img):
			shutil.rmtree(in_img)
		os.makedirs(in_img)

		for i in range(len(p)):
			if(i != 1):
				p1 = p[i]
				img = sitk.ReadImage(path+'/'+p[i])
				arr.append(sitk.GetArrayFromImage(img))
		    
			else:
				p1 = p[i]
				img = sitk.ReadImage(path+'/'+p[i])
				Y_labels = sitk.GetArrayFromImage(img)    
		data = np.zeros((155,240,240,4))
		for i in range(155):
			data[i,:,:,0] = arr[0][i,:,:]
			data[i,:,:,1] = arr[1][i,:,:]
			data[i,:,:,2] = arr[2][i,:,:]
			data[i,:,:,3] = arr[3][i,:,:]
		info = []

		for i in range(155):
			img = data[i, :, :, 2]
			indata = in_img + str(i) + ".png"
			plt.imsave(indata, img,cmap='gray')

		progress['value']=50
		login_success_screen.update_idletasks()
		time.sleep(0.8)

		Y_labels = Y_labels.reshape((Y_labels.shape[0],Y_labels.shape[1],Y_labels.shape[2],1))
		y = Y_labels.reshape((-1))
		class_weights = class_weight.compute_class_weight('balanced', np.unique(y), y)
		Y_labels = to_categorical(Y_labels,5)
		n = 0
		dicescore1 = 0
		dicescore2 = 0
		dicescore3 = 0
		dicescore4 = 0
		dicescore5 = 0
		for i in range(155):
			test = np.zeros((1,240,240,4))
			test[0] = data[i]
			Y_pred = m2.predict(test)
			l = dice_coef_np(Y_labels[i], Y_pred, 5)
			n = n+1
			dicescore1 = dicescore1 + l[0]
			dicescore2 = dicescore2 + l[1]
			dicescore3 = dicescore3 + l[2]
			dicescore4 = dicescore4 + l[3]
			dicescore5 = dicescore5 + l[4]
			print(l)
			colors=[(255,255,255),(255,0,0),(0,255,0),(0,0,255),(169,169,169)]
			pr = Y_pred.reshape(( 240 ,  240 , 5 ) ).argmax( axis=2)
			global seg_img
			seg_img = np.zeros( ( 240 , 240 , 3  ) )
			for c in range(5):
				seg_img[:,:,0] += ( (pr[:,: ] == c )*( colors[c][0] )).astype('uint8')
				seg_img[:,:,1] += ((pr[:,: ] == c )*( colors[c][1] )).astype('uint8')
				seg_img[:,:,2] += ((pr[:,: ] == c )*( colors[c][2] )).astype('uint8')
			#seg_img = cv2.resize(seg_img  , (240 , 240 ))
			k = save + "/" + str(i) + ".png"
			cv2.imwrite(k , seg_img)

		print((dicescore1 + dicescore2 + dicescore3) / (3*n))

		for i in range(155):
			path1 = '/home/user/BrainTumor-Segmentation/Data/Plots/' + str(i) +'.png'
			path2 = '/home/user/BrainTumor-Segmentation/Output/' + str(i) +'.png'
			img1 = cv2.imread(path1)
			img2 = cv2.imread(path2)
			dst = cv2.addWeighted(img1,0.8,img2,0.5,0)
			destination = "/home/user/BrainTumor-Segmentation/Output_Segmented/"+str(i) + ".png"
			cv2.imwrite(destination, dst)

		progress['value']=75
		login_success_screen.update_idletasks()
		time.sleep(0.8)

		progress['value']=99
		login_success_screen.update_idletasks()
		time.sleep(0.8)

		tk.Label(popup, text="processing completed").grid(row=0,column=0)
		progress['value']=99
		login_success_screen.update_idletasks()
		time.sleep(0.8)
		popup.destroy()

	v = StringVar()
	v.set("")
	E1 = Entry(frame1, width=45,textvariable=v)
	E1.pack(padx=0, pady=30, side=LEFT)

	browse = Button(frame1, text="Browse",width=10,height=1,command=OpenFile)
	browse.pack(padx=10, pady=30, side=LEFT)

	frame1.pack(side="top")

	upload = Button(frame2, text="Upload",width=20,height=2,command=uploading)
	upload.grid(row=0, column=0, pady = 10, sticky =N)

	progress = ttk.Progressbar(frame2,orient=HORIZONTAL,length=100,mode='determinate')
	progress.grid()
	   
	analysis = Button(frame2, text = 'Start analysis!', width = 20, height = 2,command=predicting)
	analysis.grid(row=1, column=0, pady = 10, sticky =N)

	frame2.pack()

	def callback(event):
		webbrowser.open_new(r"http://www.google.com")

	link1 =Label(frame3, text = "Liked it?", pady=5, fg = 'cyan', bg = 'black')
	link1.pack()
	link2 =Label(frame3, text = "Leave a review!", pady=5, fg = 'cyan', bg='black')
	link2.pack()

	link1.bind("<Button-1>", callback)
	link2.bind("<Button-1>", callback)
	 
	frame3.pack()

	login_success_screen.mainloop()
#---------------------------------------------------------------------------------------------------

#------------------ Designing popup for login invalid password -------------------------------------
def password_not_recognised():
	global password_not_recog_screen
	password_not_recog_screen = Toplevel(login_screen)
	password_not_recog_screen.title("Success")
	password_not_recog_screen.geometry("150x100")
	Label(password_not_recog_screen, text="Invalid Password ").pack()
	Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
#---------------------------------------------------------------------------------------------------

#------------------ Designing popup for user not found --------------------------------------------- 
def user_not_found():
	global user_not_found_screen
	user_not_found_screen = Toplevel(login_screen)
	user_not_found_screen.title("Success")
	user_not_found_screen.geometry("150x100")
	Label(user_not_found_screen, text="User Not Found").pack()
	Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
#---------------------------------------------------------------------------------------------------

#----------------- Deleting popups -----------------------------------------------------------------
def delete_login_success():
	login_success_screen.destroy()


def delete_password_not_recognised():
	password_not_recog_screen.destroy()


def delete_user_not_found_screen():
	user_not_found_screen.destroy()
#----------------------------------------------------------------------------------------------------

#---------------- Designing Main(first) window -------------------------------------------------------
def main_account_screen():
	global main_screen
	main_screen = Tk()
	main_screen.geometry('800x500')
	main_screen.title("Brat Account Login")
	main_screen.configure(background = 'black')

	label = Label(main_screen, text = 'BRATS', fg = 'light green',bg = 'black', font = (None, 30), height = 2)
	label.pack(side = TOP)

	Label(text="Select Your Choice", bg="blue", width="50", height="2", font=("Calibri", 13)).pack()
	Label(text="").pack()
	Button(text="Login", height="2", width="30", command = login).pack()
	Label(text="").pack()
	Button(text="Register", height="2", width="30", command=register).pack()

	main_screen.mainloop()


main_account_screen()
