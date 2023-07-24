#!/bin/bash

lxterminal -e ~/kafka_2.13-3.4.0/bin/zookeeper-server-start.sh ~/kafka_2.13-3.4.0/config/zookeeper.properties
lxterminal -e ~/kafka_2.13-3.4.0/bin/kafka-server-start.sh ~/kafka_2.13-3.4.0/config/server.properties
