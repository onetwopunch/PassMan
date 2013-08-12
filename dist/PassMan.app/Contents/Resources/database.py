import sqlite3
import os
import time
import binascii

# OUTPUT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = "passman.db"
class Database(object):
	__shared_state = {} #Borg design pattern, shared state
	def __init__(self):
		self.__dict__ = self.__shared_state
		self.filename = os.path.join(OUTPUT_FILE)
		if not os.path.isfile(self.filename):
			self.createDatabase(self.filename)
		else:
			self._db = sqlite3.connect(self.filename)
			self._db.row_factory = sqlite3.Row
			self.cursor = self._db.cursor()
	def createDatabase(self, filename):
		print 'Creating Database in', self.filename
		self._db = sqlite3.connect(self.filename)
		self._db.row_factory = sqlite3.Row
		self.cursor = self._db.cursor()
		#build database
		self.cursor.executescript("""
			--database schema

			CREATE TABLE IF NOT EXISTS passwd (
				pid INTEGER PRIMARY KEY,
				description TEXT,
				username TEXT,
				password TEXT
			);
			CREATE TABLE IF NOT EXISTS userpw (
				password TEXT,
				isset INTEGER
			);
			INSERT INTO userpw VALUES ('', 0)
		""")
		self.commit()
	
	def execute(self, sql, *params):
		return self.cursor.execute(sql, params)
	def fetchone(self):
		return self.cursor.fetchone()
	def fetchall(self):
		return self.cursor.fetchall()
	def lastrowid(self):
		return self.cursor.lastrowid
	def commit(self):
		self._db.commit()
	def close(self):
		self.commit()
		self._db.close()
db = Database() #single instance

def getDbFilename():
	return db.filename

def commit():
	db.commit()

def close():
	db.close()

#-----Root Password-------------------

def isUserSet():
	db.execute("SELECT isset FROM userpw")
	return db.fetchone()['isset']

def getUser():
	db.execute("SELECT password FROM userpw")
	return db.fetchone()['password']

def setUser(password):
	db.execute("UPDATE userpw SET password = ?, isset =1", password)
	commit()

#------------------------------------


def addPassword(description, username, password):
	encoded = password.encode('hex')
	db.execute("INSERT INTO passwd VALUES (NULL, ?, ?, ?)", description, username, encoded)
	commit()

def getPasswords():
	db.execute("SELECT * FROM passwd")
	passwords = [dict(x) for x in db.fetchall()]
	for entry in passwords:
		entry['password'] = entry['password'].decode('hex')
	return passwords
def delete(pid):
	db.execute("DELETE FROM passwd WHERE pid = ?", pid)
	db.commit()
def reset():
	db.execute("DELETE FROM passwd WHERE rowid > 0")
	db.execute("UPDATE userpw SET password = '', isset =0")
	commit()
def main():
	pass

if __name__ == '__main__':
	main()


