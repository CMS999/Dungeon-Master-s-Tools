import pickle
import sys
import os


class pickleJar():
	def __init__(self, jarName: str):
		self.filename = 'pickles/'+jarName
		if not os.path.isdir('pickles'):
			os.makedirs("pickles")

	def putInJar(self, object: any) -> None:
		""" Adds the object to the jar of pickles (this methods overwrites the jar) """
		with open(self.filename, 'wb') as jar:
			pickle.dump(object, jar, protocol=pickle.HIGHEST_PROTOCOL)
			jar.close()

	def addToJar(self, object: any):
		""" Adds the object to the jar of pickles (this methods does not overwrites the jar) """
		with open(self.filename, 'ab') as jar:
			pickle.dump(object, jar, protocol=pickle.HIGHEST_PROTOCOL)
			jar.close()

	def popFromJar(self) -> list:
		""" Returns a list with all the objects from the jar of pickles """
		data : list = []
		with open(self.filename, 'rb') as jar:
			while True:
				try:
					data.append(pickle.load(jar))
				except EOFError:
					break
			jar.close()
		return data

