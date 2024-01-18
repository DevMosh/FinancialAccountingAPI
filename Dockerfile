FROM python:3.10

COPY requirements.txt /temp/requirements.txt
COPY FinancialAccountingAPI /service
WORKDIR /service
EXPOSE 8000

RUN pip install -r /temp/requirements.txt
#
#RUN adduser --disabled-password FinancialAccountingAPI-user
#
#USER FinancialAccountingAPI-user
