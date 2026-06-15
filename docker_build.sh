#!/bin/bash
docker build -t gavingilchrist76/dash-app --secret id=dotenv,src=.env .
