FROM maven:3.8.1-jdk-11-slim as build
WORKDIR /home/app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src/ /home/app/src
RUN mvn package

FROM quay.io/strimzi/kafka:0.22.1-kafka-2.7.0
USER root:root
COPY --from=build /home/app/target/airqo-measurements-connector.jar /opt/kafka/plugins/airqo/
COPY --from=build /home/app/target/kcca-measurements-connector.jar /opt/kafka/plugins/airqo/
USER 1001