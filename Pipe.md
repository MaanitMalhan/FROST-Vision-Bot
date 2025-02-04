# How to use make pipe for vision 

Make sure to first compile the c++ file

1. Create a pipe: `mkfifo /tmp/vision_pipe` 

2. Compile your controller.cpp: `g++ -o controller controller.cpp`

3. Run your command exe `./controller` & `main.py` simultaneously
