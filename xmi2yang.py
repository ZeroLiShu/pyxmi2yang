import config

def main():
    opts = config.processArgs()

    configs = config.loadConfig(opts)
    print('load configs', configs)
    print('\n')

    config.validateConfig(configs)
    print('validate configs', configs)
    print('\n')

    files = config.readProjectDir(opts)
    print('uml files', files)
    print('\n')

if __name__ == "__main__":
    main()