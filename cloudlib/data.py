# get data from, and send data to, files (yaml, json, toml), processes
# create output string based on template file and dictionary object

import jinja2
import yaml
import toml
import sys
import subprocess
import getopt
import tempfile
import os

# description: runs a process and capture all its output, stdin is implicitly passed to
# the new process
#
# parameters:
#    cmd: a list of tokens
#
# output:
#    a dictionary with these keys:
#      returncode
#      stdout
#      stderr
#      cmd
def runProcess(cmd):
   popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   rtn = popen.communicate(input=sys.stdin)
   return {'returncode': popen.returncode, 'stdout': rtn[0], 'stderr': rtn[1], 'cmd': cmd}

# description: create a shell script based on a template, then run it
#
# parameters:
#    templateFile: path to template
#    templateVars: variable to update placeholders in template
# output:
#    a dictionary with these keys:
#      all keys from runProcess
#      command_text: generate command from template

def runProcessFromTemplate(templateFile, templateVars):
   cmd_text = processTemplate(templateFile, templateVars)
   temp_file = tempfile.NamedTemporaryFile(delete=False)
   temp_file_name = temp_file.name
   temp_file.write(cmd_text)
   temp_file.close()
   os.chmod(temp_file_name, 0755)
   rtn = runProcess([temp_file_name])
   rtn['command_text'] = cmd_text
   os.remove(temp_file_name)
   return rtn

def readCLI(cli_opts):
   cli_opts_shorts = map(lambda x:(x['short'] if not x['has_value'] else x['short']+':'), cli_opts)
   cli_opts_longs = map(lambda x:(x['long'] if not x['has_value'] else x['long']+'='), cli_opts)
   cli_opts_all = map(lambda x:['-'+x['short'], '--'+x['long']], cli_opts)

   opts, remainder = getopt.getopt(sys.argv[1:], ''.join(cli_opts_shorts), cli_opts_longs)
   options = {}
   for opt, arg in opts:
      for index, value in enumerate(cli_opts_all):
         if opt in value:
            opt_name = cli_opts[index]['long']
            if opt_name in options:
               options[opt_name].append(arg)
            else:
               options[opt_name] = [arg]
            break
   return options

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

