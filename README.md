# Mem Tracer
Mem Tracer is a system built to track access to different regions of a programs memory space. It uses Intel PIN to instrument source code to write the memory addresses accessed during a programs execution to an output file. Simultaneously, a python script polls the Linux proc filesystem of the same program to record which memory regions are in specific regions. Finally, it filters the output file so that only the accesses to the section of memory space specified are recorded. Currently Mem Tracer can filter the output to only accesses to all writeable pages, all readable pages, the stack, or the heap. The system produces output files that have the address accessed, and the number of times it was used before another address was accessed seperated by a space on each line. See the below example output file:
```
0x57778902 1.0
0x67999910 3.0
0x57778902 7.0
```
This output file means that the address `0x57778902` was accessed three times, then the address `0x67999910` was accessed 3 times, and finally `0x57778902` was accessed again 7 times.
## Installation
Download the source code from this repository. Then follow these steps:
1. Change the `configuration.yaml` file. This file has values for two directories. The `programs_volume` should be replaced with a file path to a directory with programs you would like to trace. The `output_volume` should hold a path to the directory you would like the traces put into. The `sections_to_trace` should hold one of `writeable`, `readable`, `stack`, or `heap`. Currently, tracing multiple sections is not supported. 
2. Run `./configure.sh`. This will generate a shell script called `run_traces.sh` and the docker-compose file `docker-compoes.yaml`.
3. Run `docker-compose build`

## Running Traces
To execute a trace, first follow the installation steps above. The instalation steps must be re-run if you change anything in `configuration.yaml`. Then add either C code files or python code files you would like traced to the programs directory specified in the `configuration.yaml`. Currently C and Python3 are supported. C will be compiled with gcc. Each python file must have a .py suffix and each C file must have a .c suffix. Every file with the .c or .py suffix in the programs directory will be traced. If you need to import other code into a file, place it outside the programs directory. Next, run `docker-compose up`. The container will spin up and your programs will be traced. Traces will be deposited into the output directory specified in `configuration.yaml`. 

### Licensing
A full copy of Intel's PIN utility is included in this repository. I've found that some versions of PIN have quirks, and old versions don't seem to stay hosted on Intel's site for very long, so I included the version I've found to work best. I do not own any of the code in the `pin/` directory. Intel's license for PIN can be found [here](https://software.intel.com/content/www/us/en/develop/articles/pin-a-binary-instrumentation-tool-license-agreement.html). 
