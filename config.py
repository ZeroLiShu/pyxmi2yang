#!/usr/bin/python
import json, sys, getopt, os.path, time

# save data to json file
def storeJson(data, filename):
    with open(filename, 'w') as fw:
        # 将字典转化为字符串
        # json_str = json.dumps(data)
        # fw.write(json_str)
        # 上面两句等同于下面这句
        json.dump(data,fw)

# load json data from file
def loadJson(filename):
    with open(filename,'r') as f:
        data = json.load(f)
        return data

class CmdOptions:
    def __init__(self):
        self.projectDir = "./project"
        self.config = self.projectDir + "/config.json"
        self.yangDir = self.projectDir

def printHelp():
    print("Usage:   python xmi2yang.py [options]\n" +
            "\nConverts XML/UML to Yang\n" +
            "Options\n" +
            "\t-c\t\t specify path to config.json, default: specified project directory/config.json\n" +
            "\t-d\t\t specify project directory, default: ./project\n" +
            "\t-o\t\t specify output directory for generated yang files, default: specified project directory\n" +
            "\t-h, --help\t print usage information\n\n" +
            "Example: python xmi2yang.py -d /opt/project -c /etc/config.json -o /opt/project/yang\n")

def processArgs():
    print('processArgs: sys.argv', sys.argv)
    cmdOpts = CmdOptions()

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:d:o:",["help", "config=", "projectDir=", "outputDir="])
    except getopt.GetoptError:
        print("option error occurs, please use 'python pyxmi2yang.py -h' to get help message.")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            printHelp()
            sys.exit()
        elif opt in ("-c", "--config"):
            cmdOpts.config = arg
        elif opt in ("-d", "--projectDir"):
            cmdOpts.projectDir = arg
        elif opt in ("-o", "--outputDir"):
            cmdOpts.yangDir = arg

    print('processArgs: config=%s projectDir=%s yangDir=%s'%(cmdOpts.config, cmdOpts.projectDir, cmdOpts.yangDir))
    return cmdOpts

def parseHtml(configs):
    for k,v in configs.items():
        if type(v) == dict:
            parseHtml(v)
        elif type(v) == str:
            v = v.replace("/<br \/>/g","\r\n")
            v = v.replace("/<br\/>/g","\r\n")
            v = v.replace("/<br>/g","\r\n");

def isValidDate(date):
        try:
            if ":" in date:
                time.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(date, "%Y-%m-%d")
            return True
        except:
            return False

def validateConfig(configs):
    for k,v in configs.items():
        if type(v) == dict:
            #traverse object and replace <br> with "\r\n"
            parseHtml(v)
            curDate = time.strftime("%Y-%m-%d", time.localtime())
            if v.__contains__('revision'):
                if not isValidDate(v['revision'][0]['date']):
                    print("the config has (%s) invalid date."%(k))
                    sys.exit(2)
            else:
                v['revision'] = [{'date':curDate}]

def loadConfig(opts):
    if os.path.isfile(opts.config):
        configs = loadJson(opts.config)

        for k,v in configs.items():
            if type(v) == dict:
                v['projectDir'] = opts.projectDir
                v['config'] = opts.config
        
        configs['projectDir'] = opts.projectDir
        configs['config'] = opts.config
        return configs
    else:
        print("the config file (%s) does not exist. Please add a configuration file and try again."%(opts.config))
        sys.exit(2)

def readProjectDir(opts):
    files = os.listdir(opts.projectDir)
    files = [opts.projectDir + f for f in files if f.endswith(('.xml','.uml'))]
    return files