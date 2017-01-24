# get data from, and send data to, files (yaml, json, toml), processes
# create output string based on template file and dictionary object

import jinja2
import yaml
import toml
import sys
import subprocess

def runProcess(cmd):
   popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   rtn = popen.communicate(input=sys.stdin)
   return {'returncode': popen.returncode, 'stdout': rtn[0], 'stderr': rtn[1]}

def processTemplate(templateFile, templateVars):
   templateLoader = jinja2.FileSystemLoader( searchpath=os.path.dirname(templateFile) )
   templateEnv = jinja2.Environment( loader=templateLoader )
   template = templateEnv.get_template( os.path.basename(templateFile) )
   outputText = template.render( templateVars )
   return outputText

def saveToFile(text, filename):
   of = open(filename, 'w')
   of.write(text)
   of.close()

def merge(source, destination):
   for key, value in source.items():
      if isinstance(value, dict):
         # get node or create one
         node = destination.setdefault(key, {})
         merge(value, node)
      else:
         destination[key] = value
   return destination

def readYamlFile(filename):
   with open(filename, 'r') as stream:
      return yaml.load(stream)

def writeYamlFile(filename, data):
   with open(filename, 'w') as outfile:
      yaml.dump(data, outfile, default_flow_style=False)

def readYamlText(text):
   return yaml.load(text)

def readJsonFile(filename):
   with open(filename, 'r') as stream:
      return json.load(stream)

def writeJsonFile(filename, data):
   with open(filename, 'w') as outfile:
      json.dump(data, outfile)

def readJsonText(text):
   return json.load(text)

def readTomlFile(filename):
   with open(filename, 'r') as stream:
      return toml.loads(stream.read())

def writeTomlFile(filename, data):
   with open(filename, 'w') as outfile:
      outfile.write(toml.dumps(data))

def readTomlText(text):
   return toml.loads(text)

