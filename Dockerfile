FROM ubuntu:18.04

RUN apt-get update && apt-get install make gcc gdb python3 python3-pip systemd -y
RUN pip3 install numpy pandas

# Compiling pin utility
COPY pin/ pin/
RUN cd /pin/source/tools/ManualExamples/ && make clean && make obj-intel64/pinatrace.so
RUN mkdir /pin_bin/
RUN cp /pin/source/tools/ManualExamples/obj-intel64/pinatrace.so \
/pin/pin /pin/pin.sig /pin_bin && cp -a pin/ia32 \
pin/intel64 pin/extras pin_bin/

COPY run_traces.sh /run_traces.sh
COPY run_programs.py /run_program.py
RUN chmod +x run_traces.sh && chmod +x run_program.py

CMD ./run_traces.sh
