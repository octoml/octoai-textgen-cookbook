# Use an official Python runtime as the parent image
FROM public.ecr.aws/lambda/python:3.11
ENV LANG=en_US.UTF-8
ENV TZ=:/etc/localtime
ENV PATH=/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin
ENV LD_LIBRARY_PATH=/var/lang/lib:/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib
ENV LAMBDA_TASK_ROOT=/var/task
ENV LAMBDA_RUNTIME_DIR=/var/runtime

WORKDIR /var/task

# Copy the requirements file into the container
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN yum install -y gcc-c++ pkgconfig poppler-cpp-devel
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -U

# Copy the main python file
COPY main.py ${LAMBDA_TASK_ROOT}

# Specify the command to run on container start
CMD ["main.handler"]
