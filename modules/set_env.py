from lib_vendor import yaml
import os

app_launch_file = open('config/env.yml')
app_launch_dictionary = yaml.load(app_launch_file)
app_launch_file.close()

def set_env(name, value):
	if os.environ.get(name):
		os.environ[name] += os.pathsep + value
	else:
		os.environ[name] = value
	return 0

app = 'houdini'
for i in app_launch_dictionary[app]:
	variable = i
	values = app_launch_dictionary[app][i]

	if type(values) == list:
		print "List Values Loop"
		for value in values:
			print "VARIABLE: ", variable
			print "VALUE: ", value
			set_env(variable, value)
	else:
		print "Just a string"
		print values
		set_env(variable, value)


# Test
print "####TEST####"
for i in app_launch_dictionary[app]:
	print i, os.environ[i]