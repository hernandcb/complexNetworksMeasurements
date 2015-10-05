# -*- coding: utf-8 -*-
import configparser, os

config = configparser.ConfigParser()
path = os.path.abspath(os.path.dirname(__file__))

config.read(os.path.join(path, "networkAnalysis.conf"))


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


def get_random_networks_full_path():
    fullpath = config.get("project", "baseFolder")
    fullpath += config.get("data", "baseFolder")
    fullpath += config.get("data", "randomNetworks")

    return fullpath


def get_real_networks_full_path():
    fullpath = config.get("project", "baseFolder")
    fullpath += config.get("data", "baseFolder")
    fullpath += config.get("data", "realNetworks")

    return fullpath


def get_results_folder_path():
    fullpath = config.get("project", "baseFolder")
    fullpath += config.get("results", "baseFolder")

    return fullpath


def get_random_results_folder_path():
    fullpath = config.get("project", "baseFolder")
    fullpath += config.get("results", "baseFolder")
    fullpath += config.get("results", "randomNetworks")

    return fullpath
