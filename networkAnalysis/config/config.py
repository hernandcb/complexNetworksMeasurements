# -*- coding: utf-8 -*-
import configparser

config = configparser.ConfigParser()
config.read("networkAnalysis.conf")

def get(section, variable):
	return config.get(section, variable)

def getboolean(section, variable):
	return config.getboolean(section, variable)

def getint(section, variable):
	return config.getint(section, variable)

def getfloat(section, variable):
	return config.getfloat(section, variable)

def getBaseFolder():
	return get("project", "baseFolder")
	
def getDataFolder():
	return get("data", "baseFolder")