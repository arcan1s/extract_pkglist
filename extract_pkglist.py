#!/usr/bin/python2

import argparse, os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create bckp files for ArchLinux')
    parser.add_argument('-p','--prefix', dest='prefix',
                        help = 'Files prefix. Default is "pkglist"',
                        action='store', default = 'pkglist')
    parser.add_argument('-q','--quiet', dest='quiet',
                        help = 'Do not show output',
                        action='store_true', default = False)
    parser.add_argument('-n','--not-test', dest='test',
                        help = 'Do not test availability of package in AUR',
                        action='store_true', default = False)
    args = parser.parse_args()
    
    pkglist_repo = open(args.prefix + "_repo", 'w')
    pkglist_other = open(args.prefix + "_other", 'w')
    if (not args.test):
        pkglist_nondb = open(args.prefix + "_nondb", 'w')
    
    extra = 0
    core = 0
    multilib = 0
    community = 0
    other = 0
    
    for line in os.popen("yaourt -Qe"):
        if (not args.quiet):
            print "Copying: '" + line.split()[0].split('/')[1]+"'"
        if (line.split()[0].split('/')[0] == "extra"):
            extra += 1
            pkglist_repo.write(line.split()[0].split('/')[1]+"\n")
        elif (line.split()[0].split('/')[0] == "core"):
            core += 1
            pkglist_repo.write(line.split()[0].split('/')[1]+"\n")
        elif (line.split()[0].split('/')[0] == "community"):
            community += 1
            pkglist_repo.write(line.split()[0].split('/')[1]+"\n")
        elif (line.split()[0].split('/')[0] == "multilib"):
            multilib += 1
            pkglist_repo.write(line.split()[0].split('/')[1]+"\n")
        else:
            other += 1
            if (args.test):
                pkglist_other.write(line.split()[0].split('/')[1]+"\n")
            else:
                num_lines = sum(1 for testline in 
                                os.popen("wget --spider -o /dev/stdout https://aur.archlinux.org/packages/" + 
                                         line.split()[0].split('/')[1] + 
                                         " | grep '404 Not Found'"))
                if (num_lines == 0):
                    pkglist_other.write(line.split()[0].split('/')[1]+"\n")
                else:
                    pkglist_nondb.write(line.split()[0].split('/')[1]+"\n")
    
    if (not args.quiet):
        print "---------------------"
        print "--------Done!--------"
        print "Core:           %5s" % (str(core))
        print "Extra:          %5s" % (str(extra))
        print "Community:      %5s" % (str(community))
        print "Multilib:       %5s" % (str(multilib))
        print "other:          %5s" % (str(other))
        print "Total packages: %5s" % (str(core + extra + community + multilib + other))
    
    pkglist_repo.close()
    pkglist_other.close()
    if (not args.test):
        pkglist_nondb.close()
