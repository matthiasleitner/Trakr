#this loads up the default configurations upon first launch
import ConfigParser
import os


defaultConfigPath = "./trakr.ini"

def createDefaultConfig():
    file = open(defaultConfigPath, 'w')
    config = ConfigParser.ConfigParser()

    fullPath = str(getFullTrakrPath())


    config.add_section("trakr")
    config.set("trakr", "full_path", fullPath)
    config.set("trakr", "autostart", False)
    config.set("trakr", "key", "you-need-to-change-this")


    # database section
    config.add_section("db")
    config.set("db", "rolling_path", (fullPath + "/runtime/db/rolling.db"))
    config.set("db", "behavior_path", (fullPath + "/runtime/db/behavior.db"))
    config.set("db", "reduced_table_name", "REDUCED")
    config.set("db", "unqiue_table_name", "UNIQUEMACS")
    config.set("db", "rolling_table_name", "ROLLING")

    config.set("db", "graph_path", (fullPath + "/runtime/db/graph.db"))
    config.set("db", "hash_values", True)

    # scanner section
    config.add_section("scanner")
    # TODO
    # find a way to check the OS and then get the default interface
    # because this works for MacOS only
    config.set("scanner", "interface", "en0")
    config.set("scanner","duration", 60*10) #scan for 10 minutes
    config.set("scanner", "capture_dir", fullPath+"/runtime/pcap/")
    config.set("scanner", "keep_all_pcap", False)

    # analysis section
    config.add_section("analysis")
    config.set("analysis", "exit_seconds", 60*45) # 45 minutes
    config.set("analysis", "enter_period_seconds", 60*6) # 6 minutes

    # enter_period_second will be divided into enter_subperiod groups
    # and there must be at least one wifi observation in each of those
    # groups to then assume the person has entered and is not just passing by
    config.set("analysis", "enter_subperiods", 4)



    config.write(file)
    print "Default config written."



def getFullTrakrPath():
    return os.path.dirname(os.path.abspath(__file__))[:-7]