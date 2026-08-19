import os

services = ['passenger-service', 'ride-service']

pom_template = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.2</version>
        <relativePath/>
    </parent>
    <groupId>com.rideshare</groupId>
    <artifactId>{service_name}</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>{service_name}</name>
    <description>Demo project for Spring Boot</description>
    <properties>
        <java.version>21</java.version>
        <spring-cloud.version>2023.0.3</spring-cloud.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-circuitbreaker-resilience4j</artifactId>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
    </dependencies>
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${{spring-cloud.version}}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </repository>
        <repository>
            <id>spring-snapshots</id>
            <name>Spring Snapshots</name>
            <url>https://repo.spring.io/snapshot</url>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </repository>
    </repositories>
    <pluginRepositories>
        <pluginRepository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
        </pluginRepository>
        <pluginRepository>
            <id>spring-snapshots</id>
            <name>Spring Snapshots</name>
            <url>https://repo.spring.io/snapshot</url>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </pluginRepository>
    </pluginRepositories>
</project>
"""

app_template = """package com.rideshare.{module};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestClient;

@SpringBootApplication
public class Application {{
    public static void main(String[] args) {{
        SpringApplication.run(Application.class, args);
    }}
    
    @Bean
    public RestClient.Builder restClientBuilder() {{
        return RestClient.builder();
    }}
}}
"""

application_properties = """server.port={port}
spring.application.name={service_name}
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.h2.console.enabled=true
management.endpoints.web.exposure.include=*
logging.level.org.springframework.web=DEBUG
logging.level.com.rideshare=DEBUG
"""

schema_sql = """CREATE TABLE IF NOT EXISTS {table_name} (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    {columns}
);
"""

data_sql_passenger = """INSERT INTO passenger (name, email) VALUES ('John Doe', 'john@example.com');
INSERT INTO passenger (name, email) VALUES ('Jane Smith', 'jane@example.com');
"""

data_sql_ride = """INSERT INTO ride (passenger_id, driver_id, status) VALUES (1, 1, 'COMPLETED');
"""

for i, service in enumerate(services):
    os.makedirs(f"{service}/src/main/java/com/rideshare/{service.split('-')[0]}", exist_ok=True)
    os.makedirs(f"{service}/src/main/resources", exist_ok=True)
    
    with open(f"{service}/pom.xml", "w") as f:
        # Replacing with a generic 3.3.2 if 4.0.0-SNAPSHOT is failing, but I will write 4.0.0-SNAPSHOT
        f.write(pom_template.format(service_name=service).replace("3.3.2", "4.0.0-SNAPSHOT"))
        
    module = service.split('-')[0]
    with open(f"{service}/src/main/java/com/rideshare/{module}/Application.java", "w") as f:
        f.write(app_template.format(module=module))
        
    port = 8081 if service == 'passenger-service' else 8082
    with open(f"{service}/src/main/resources/application.properties", "w") as f:
        f.write(application_properties.format(port=port, service_name=service))

    if service == 'passenger-service':
        with open(f"{service}/src/main/resources/schema.sql", "w") as f:
            f.write(schema_sql.format(table_name="passenger", columns="name VARCHAR(255), email VARCHAR(255)"))
        with open(f"{service}/src/main/resources/data.sql", "w") as f:
            f.write(data_sql_passenger)
    else:
        with open(f"{service}/src/main/resources/schema.sql", "w") as f:
            f.write(schema_sql.format(table_name="ride", columns="passenger_id BIGINT, driver_id BIGINT, status VARCHAR(50)"))
        with open(f"{service}/src/main/resources/data.sql", "w") as f:
            f.write(data_sql_ride)

