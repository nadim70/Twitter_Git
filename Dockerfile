FROM centos
RUN yum install python36 -y
RUN yum install python3-pip -y
RUN pip3 install numpy
RUN pip3 install pandas
RUN yum install httpd -y
RUN pip3 install tweepy
