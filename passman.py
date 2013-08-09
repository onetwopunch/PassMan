import sqlite3 
import wx
from database import *
from passlib.apps import custom_app_context as pwd_context
import sys
from pprint import pprint

ID_NEW = 1
ID_RENAME = 2
ID_CLEAR = 3
ID_DELETE = 4
ID_UN_OUT = 5
ID_PW_OUT = 6
ID_LIST = 7
ID_SHOW = 8
ID_CHPW = 9
APP_EXIT = 10

class PassMan(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=(500, 320))
		
		if self.login():
			panel = wx.Panel(self, -1)
			self.SetBackgroundColour('#86c440')
			menubar = wx.MenuBar()
			fileMenu = wx.Menu()
			cmi = wx.MenuItem(fileMenu, ID_CHPW, 'C&hange Password')
			qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit')
			fileMenu.AppendItem(cmi)
			fileMenu.AppendItem(qmi)
			self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
			self.Bind(wx.EVT_MENU, self.ChangePassword, id=ID_CHPW)
			menubar.Append(fileMenu, '&File')
			self.SetMenuBar(menubar)

			hbox = wx.BoxSizer(wx.HORIZONTAL)

			self.listbox = wx.ListBox(panel, -1)
			self.listdata = getPasswords()
			for entry in self.listdata:
				self.listbox.Append(entry['description'])

			hbox.Add(self.listbox, ID_LIST, wx.EXPAND | wx.ALL, 20)

			btnPanel = wx.Panel(panel, -1)
			vbox = wx.BoxSizer(wx.VERTICAL)
			new = wx.Button(btnPanel, ID_NEW, 'New', size=(90, 30))
			dlt = wx.Button(btnPanel, ID_DELETE, 'Delete', size=(90, 30))
			clr = wx.Button(btnPanel, ID_CLEAR, 'Clear', size=(90, 30))
			show = wx.Button(btnPanel, ID_SHOW, 'Show', size=(90, 30))

			self.tcOutUsername = wx.TextCtrl(btnPanel, ID_UN_OUT, style=wx.TE_READONLY)
			self.tcOutPassword = wx.TextCtrl(btnPanel, ID_PW_OUT, style=wx.TE_READONLY)

			self.Bind(wx.EVT_BUTTON, self.NewItem, id=ID_NEW)
			self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE)
			self.Bind(wx.EVT_BUTTON, self.OnClear, id=ID_CLEAR)
			self.Bind(wx.EVT_BUTTON, self.OnShow, id=ID_SHOW)
			# self.Bind(wx.EVT_CHAR_HOOK, self.onKey)

			vbox.Add((-1, 20))
			vbox.Add(new)
			vbox.Add(dlt, 0, wx.TOP, 5)
			vbox.Add(show, 0, wx.TOP, 5)
			vbox.Add(self.tcOutUsername, 0, wx.TOP, 5)
			vbox.Add(self.tcOutPassword, 0, wx.TOP, 5)
			vbox.Add(clr, 0, wx.TOP, 5)
			btnPanel.SetSizer(vbox)
			hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
			panel.SetSizer(hbox)

			addid = wx.NewId()
			quitid = wx.NewId()
			clearid = wx.NewId()
			showid = wx.NewId()

			self.Bind(wx.EVT_MENU, self.NewItem, id=addid)
			self.Bind(wx.EVT_MENU, self.OnQuit, id=quitid)
			self.Bind(wx.EVT_MENU, self.OnClear, id=clearid)
			self.Bind(wx.EVT_MENU, self.OnShow, id=showid)
			self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('N'), addid),
													(wx.ACCEL_CTRL, ord('Q'), quitid),
													(wx.ACCEL_CTRL, ord('C'), clearid),
													(wx.ACCEL_CTRL, ord('S'), showid)
													])
			self.SetAcceleratorTable(self.accel_tbl)

			self.Centre()
			self.Show(True)
		else:
			sys.exit(1)



	def login(self):
		userpw = wx.GetPasswordFromUser('Enter root password', 'Root Password')
		loggedin = False
		if not isUserSet():
			conf = wx.GetPasswordFromUser('Please confirm root password', 'Root Password')
			while conf != userpw:
				print 'Passwords do not match'
				userpw = wx.GetPasswordFromUser('Enter root password', 'Root Password')				
				conf = wx.GetPasswordFromUser('Please confirm root password', 'Root Password')
			print 'Initializing user'
			password = pwd_context.encrypt(userpw)
			setUser(password)
			return True
		else:
			tries = 2
			while not loggedin:
				loggedin = pwd_context.verify(userpw, getUser())
				if not loggedin:
					print 'Wrong password'
					userpw = wx.GetPasswordFromUser('Enter root password', 'Root Password')
					tries -=1
					if tries == 0:
						self.ResetApplication()
						return False
			return True

	def ChangePassword(self, evt):
		dlg = wx.MessageDialog(self, "Do you really want to change your password?", 
									"Confirm Password Change", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_OK:
			userpw = wx.GetPasswordFromUser('Enter root password', 'Root Password')
			conf = wx.GetPasswordFromUser('Please confirm root password', 'Root Password')
			while conf != userpw:
				wx.MessageBox('', 'Passwords do not match', wx.OK | wx.ICON_INFORMATION)
				userpw = wx.GetPasswordFromUser('Enter root password', 'Root Password')
				conf = wx.GetPasswordFromUser('Please confirm root password', 'Root Password')
			password = pwd_context.encrypt(userpw)
			setUser(password)

	def ResetApplication(self):
		dlg = wx.MessageDialog(self, 'You have tried to log in 3 times unsucessfully. Do you want to reset the application, destying your data? You will need to relaunch the application and enter a new password after this process is complete.', 
										 "Confirm Password Change", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_OK:
			reset()


	def NewItem(self, event):
		dialog = wx.Frame(None, 1, 'New Password', size=(250, 175))

		vbox = wx.BoxSizer(wx.VERTICAL)

		gs = wx.GridSizer(4, 2, 10, 10)
		lblDesc = wx.StaticText(dialog, label="Description")
		lblUser = wx.StaticText(dialog, label="Username")
		lblPass = wx.StaticText(dialog, label="Password")

		tcDesc = wx.TextCtrl(dialog, wx.EXPAND)
		tcUser = wx.TextCtrl(dialog, wx.EXPAND)
		tcPass = wx.TextCtrl(dialog, wx.EXPAND, style=wx.TE_PASSWORD)

		btnAdd = wx.Button(dialog, 1, label='Add')
		btnAdd.SetFocus()
		btnCancel = wx.Button(dialog, 2, label='Close')

		gs.AddMany([(lblDesc, 0, wx.EXPAND), 
					(tcDesc, 0, wx.EXPAND), 
					(lblUser, 0, wx.EXPAND), 
					(tcUser, 0, wx.EXPAND), 
					(lblPass, 0, wx.EXPAND), 
					(tcPass, 0, wx.EXPAND), 
					(btnAdd, 0, wx.EXPAND), 
					(btnCancel, 0, wx.EXPAND)])
		def OnCancel(event):
			dialog.Close(True)
		def OnAdd(event):
			desc = tcDesc.GetValue()
			un = tcUser.GetValue()
			pw = tcPass.GetValue()
			addPassword(desc, un, pw)
			tcDesc.SetValue('')
			tcUser.SetValue('')
			tcPass.SetValue('')
			self.listbox.Append(desc)
			dialog.Close()
			wx.MessageBox('', 'Password added successfully', wx.OK | wx.ICON_INFORMATION)
		
		def onKey(evt):
			if evt.GetKeyCode() == wx.WXK_RETURN:
				OnAdd(evt)	
			else:
				evt.Skip()

		addid = wx.NewId()
		closeid = wx.NewId()
		dialog.Bind(wx.EVT_CHAR_HOOK, onKey)
		dialog.Bind(wx.EVT_MENU, OnAdd, id=addid)
		dialog.Bind(wx.EVT_MENU, OnCancel, id=closeid)
		dialog.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('A'), addid), (wx.ACCEL_CTRL, ord('C'), closeid)])
		dialog.SetAcceleratorTable(self.accel_tbl)
		dialog.Bind(wx.EVT_BUTTON, OnAdd, id = 1)
		dialog.Bind(wx.EVT_BUTTON, OnCancel, id = 2)

		vbox.Add(gs, flag=wx.TOP|wx.RIGHT|wx.LEFT, border=15)
		dialog.SetSizer(vbox)


		dialog.Show(True)



	def OnShow(self, event):
		sel = self.listbox.GetSelection()
		# print "Selected", str(sel)
		if sel != -1:
			entry = getPasswords()[sel]
			self.tcOutUsername.SetValue(entry['username'])
			self.tcOutPassword.SetValue(entry['password'])

	def OnDelete(self, event):
		sel = self.listbox.GetSelection()
		pprint(self.listdata)
		print 'Selected', str(sel)
		if sel != -1:
			self.listbox.Delete(sel)
			pid = self.listdata[sel]['pid']
			delete(pid)
			self.listdata = getPasswords()

	def OnClear(self, event):
		self.tcOutUsername.SetValue('')
		self.tcOutPassword.SetValue('')
	def OnQuit(self, e):
		self.Close()



def main():
	app = wx.App()
	PassMan(None, -1, 'PassMan')
	app.MainLoop()




if __name__ == '__main__':
	main()

