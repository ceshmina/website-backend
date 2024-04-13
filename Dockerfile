FROM amazonlinux:2023

RUN yum update && yum install -y python3.11 python3.11-pip
RUN pip3.11 install boto3==1.34 Pillow==10.3

RUN yum install -y zip
