#!/bin/bash

echo "Compiling all services..."
mvn clean compile -f discovery-service/pom.xml || exit 1
mvn clean compile -f passenger-service/pom.xml || exit 1
mvn clean compile -f ride-service/pom.xml || exit 1
mvn clean compile -f gateway-service/pom.xml || exit 1
echo "Compilation passed."

echo "Starting discovery-service..."
mvn spring-boot:run -f discovery-service/pom.xml > discovery.log 2>&1 &
PID1=$!

echo "Waiting for Eureka Server..."
for i in {1..30}; do
    if curl -s http://localhost:8761/actuator/health > /dev/null; then break; fi
    sleep 2
done

echo "Starting passenger, ride, and gateway services..."
mvn spring-boot:run -f passenger-service/pom.xml > passenger.log 2>&1 &
PID2=$!
mvn spring-boot:run -f ride-service/pom.xml > ride.log 2>&1 &
PID3=$!
mvn spring-boot:run -f gateway-service/pom.xml > gateway.log 2>&1 &
PID4=$!

echo "Waiting for clients to register with Eureka and gateway to boot (takes ~30-45s)..."
for i in {1..45}; do
    APPS=$(curl -s -H "Accept: application/json" http://localhost:8761/eureka/apps)
    
    # We expect 3 clients: PASSENGER-SERVICE, RIDE-SERVICE, GATEWAY-SERVICE
    if echo "$APPS" | grep -q "PASSENGER-SERVICE" && echo "$APPS" | grep -q "RIDE-SERVICE" && echo "$APPS" | grep -q "GATEWAY-SERVICE"; then
        echo -e "\n--- All services registered! ---\n"
        break
    fi
    sleep 2
done

# Wait an extra 5 seconds for routes to settle
sleep 5

echo "--- Testing through API Gateway (Port 8080) ---"

echo -e "\n1. Create Passenger through Gateway..."
CREATE_PASS=$(curl -s -X POST http://localhost:8080/api/passengers \
    -H "Content-Type: application/json" \
    -d '{"name": "Gateway User", "email": "gateway@example.com"}')
echo "Response: $CREATE_PASS"

echo -e "\n2. Fetch Passengers through Gateway..."
curl -s http://localhost:8080/api/passengers

echo -e "\n\n3. Create Ride through Gateway..."
# Assuming passenger ID is 1
CREATE_RIDE=$(curl -s -X POST http://localhost:8080/api/rides \
    -H "Content-Type: application/json" \
    -d '{"passengerId": 1, "driverId": 99}')
echo "Response: $CREATE_RIDE"

echo -e "\n\n4. Fetch Rides through Gateway..."
curl -s http://localhost:8080/api/rides

echo -e "\n\nShutting down everything..."
kill -9 $PID1 $PID2 $PID3 $PID4
