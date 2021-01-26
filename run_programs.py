#!/usr/bin/python3
import os
import signal
import sys
import time

def main(args):
    if len(args) < 2:
        print("Arguments <section_to_trace> <pin_line> <args_for_program>")
        return -1;

    section = args[1].lower()
    if section == 'writeable':
        lines_to_look_for = [" r-", " --"]
    elif section == 'readable':
        lines_to_look_for = [" rw", " r-"]
    elif section == 'heap':
        lines_to_look_for = ['heap']
    elif section == 'stack':
        lines_to_look_for = ['stack']
    else:
        print("Section to trace should be one of: writeable, readable, heap, stack")
        print(args[1].lower())
        return -1

    for index, arg in enumerate(args):
        if arg == "-o":
            out_file = args[index + 1]

    # Signal handler for sigchild. This stops the read loop for the
    # proc/<process_number>/maps file. The flag variable has to be enclosed in
    # a refrence type so it doesn't get copied in the signal handle, hence the
    # list for the variable keep_running.
    keep_running = [True,]
    def handler(signum, frame):
        keep_running[0] = False

    signal.signal(signal.SIGCHLD, handler)

    pid = os.fork()

    if pid == 0:
        # sleep before execing so that the porc/maps loop is running before
        # we start tracing.
        time.sleep(1)
        error = os.execv(args[2], args[2:])
        print("Error exec-ing program. Failed with code: {}".format(error))

    else:
        maps_file_path = "/proc/{}/maps".format(pid)

        print("Running Program's PID is: {}. Name is: {}".format(pid, out_file), flush=True)
        # run loop updating regions from maps file as long as the
        # child is running.
        mem_regions = {}
        while(keep_running[0]):
            with open(maps_file_path, "r") as maps_file:
                for mem_region_line in maps_file:
                    found = False
                    for line in lines_to_look_for:
                        if line in mem_region_line:
                            found = True
                    if found:
                        writeable_addr_range = mem_region_line.split()[0].split('-')
                        if writeable_addr_range[0] not in mem_regions:
                            mem_regions[writeable_addr_range[0]] = writeable_addr_range[1]
                        elif mem_regions[writeable_addr_range[0]] < writeable_addr_range[1]:
                            # save only the longest address range starting from
                            # a specific address.
                            mem_regions[writeable_addr_range[0]] = writeable_addr_range[1]

        # reap child process
        pid, return_val = os.waitpid(pid, 0)
        print("done w/ tracing {}".format(out_file), flush=True)
        # make list of tuples of ranges and convert to ints (fom hex)
        mem_regions = list(mem_regions.items())
        mem_regions = list(map(
            lambda region: (int(region[0], 16), int(region[1], 16)),
            mem_regions))
        last_page = 0
        new_out_file = "{}.final".format(out_file)
        with open(out_file, "r") as out_file:
            with open(new_out_file, "w") as new_output_file:
                print("executing post processing for {}".format(new_out_file), flush=True)
                for line in out_file:
                    row = line.strip().split()
                    try:
                        addr = int(row[0], 16)
                    except ValueError as e:
                        # it's the end of file #eof line.
                        # or some othe non-hex value. Just skip the line.
                        continue
                    # if it's in the mem range, save the line to the out file.
                    found = False
                    for addr_range in mem_regions:
                        if addr_range[0] <= addr <= addr_range[1]:
                                found = True
                                break
                    if section == 'writeable':
                        found = not found
                    if found:
                        new_output_file.write(line)

if __name__ == "__main__":
    main(sys.argv)
