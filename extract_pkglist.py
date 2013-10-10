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
    
    repos = 0
    other = 0
    
    for line in os.popen("yaourt -Qnq"):
        if (not args.quiet):
            print "Copying: '" + line[:-1] + "'"
        repos += 1
        pkglist_repo.write(line)
    for line in os.popen("yaourt -Qmq"):
        if (not args.quiet):
            print "Copying: '" + line[:-1] + "'"
        other += 1
        if (args.test):
            pkglist_other.write(line)
        else:
            num_lines = sum(1 for testline in 
                            os.popen("wget --spider -o /dev/stdout https://aur.archlinux.org/packages/" + 
                            line[:-1] + " | grep '404 Not Found'"))
            if (num_lines == 0):
                pkglist_other.write(line)
            else:
                pkglist_nondb.write(line)
    
    if (not args.quiet):
        print "---------------------"
        print "--------Done!--------"
        print "Repos:          %5s" % (str(repos))
        print "Other:          %5s" % (str(other))
        print "Total packages: %5s" % (str(repos + other))
    
    pkglist_repo.close()
    pkglist_other.close()
    if (not args.test):
        pkglist_nondb.close()
