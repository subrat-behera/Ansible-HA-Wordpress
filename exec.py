#!/usr/bin/env python
import yaml
import csv
import os
import sys
from subprocess import call

yml_home=os.path.join(os.path.dirname(os.path.realpath(__file__)),"/home/ec2-user/SKB/GreenField-Deployment/Ansible-HA-Wordpress/aws/vars")

def input_Validater(file):
	try:
		if  os.path.isfile(file):
			print "Input file exists"
			return file
		else:
			print file+" named file doesn't exist , check the file path and permissions "
			sys.exit()
		
	except Exception as e:
		print "Pass proper arguments to script "+str(e)
		sys.exit()


def list_yml(yml_home):
	try:
		for file in os.listdir(yml_home):
			if os.path.isfile(os.path.join(yml_home,file)) and file.endswith(('.yml', '.yaml','.YML', '.YAML','.Yml', '.Yaml')):
				yield os.path.join(yml_home,file)
			
	except 	Exception as e:	
		print "Error in function list_yml : "+str(e)
		
		

def read_csv(Input_file):
	try:
		csvstream=open(Input_file, "r")
		csvdocs = csv.reader(csvstream)
		return csvdocs
	except IOError:
		print "Error: File does not appear to exist."
		return 0
		

def yml_dump(file):
	try:
		print "updating file "+ file
		yamlstream = open(file, "r")
		yamldocs = yaml.load(yamlstream)
		
		# manipulating yml file on basis of csv input
		for line in read_csv(sys.argv[1]):
			
			if line and line[0] in yamldocs:
				yamldocs[line[0]]=str(line[1])
				
		# writing buffer to yml file		
		with open(file, 'w') as outfile:
			outfile.write( yaml.dump(yamldocs, default_flow_style=False ))	
			
	except Exception as e:
		print "Error :",str(e)
		return 0
		

def main():
	try:
		input_Validater(sys.argv[1])
		for file in list_yml(yml_home):
			yml_dump(file)
			
	except IndexError:
		print "Pass proper arguments to script "
	except Exception as e:
		print "Error "+str(e)
		sys.exit()	
	
		
if __name__ == '__main__':
	main()
        call(["ansible-playbook", "-i","hosts","-vvv","site.yml"])
	#call(["sudo","ansible-playbook", "-i","'localhost,'","-c", "local","ansi.yml"])
    #call(["ansible-playbook","main.yml"])

	
