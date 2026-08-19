#!/bin/bash

echo "Starting passenger-service on port 8081..."
mvn spring-boot:run -f pasenger-service/pom.xml > passenger.log 2>&1 &
PASSENGER_PID=$!

echo "Starting ride-service on port 8082..."
mvn spring-boot:run -f ride-service/pom.xml > ride.log 2>&1 &
RIDE_PID=$!

echo "Waiting for services to start..."
for i in {1..30}; do
    if curl -s http://localhost:8081/actuator/health > /dev/null && curl -s http://localhost:8082/actuator/health > /dev/null; then
        echo -e "\n--- Both services are up! ---\n"
        break
    fi
    sleep 3
done

echo "1. Requesting a new ride (POST /api/rides) with passengerId 1..."
# Create ride uses OpenFeign to call passenger-service
RIDE_RESPONSE=$(curl -s -X POST http://localhost:8082/api/rides \
    -H "Content-Type: application/json" \
    -d '{"passengerId": 1, "driverId": 2}')
echo "Response: $RIDE_RESPONSE"

RIDE_ID=$(echo $RIDE_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ -z "$RIDE_ID" ]; then
    echo "Failed to create ride. Exiting."
    kill -9 $PASSENGER_PID $RIDE_PID
    exit 1
fi

echo -e "\n2. Fetching the created ride (GET /api/rides/$RIDE_ID)..."
curl -s http://localhost:8082/api/rides/$RIDE_ID

echo -e "\n\n--- Testing Circuit Breaker Fallback ---"
echo "Killing passenger-service to simulate outage..."
kill -9 $PASSENGER_PID
sleep 3

echo "3. Requesting a new ride while passenger-service is down..."
FALLBACK_RESPONSE=$(curl -s -X POST http://localhost:8082/api/rides \
    -H "Content-Type: application/json" \
    -d '{"passengerId": 2, "driverId": 3}')
echo "Response: $FALLBACK_RESPONSE"

echo -e "\n\n--- Tests Completed. Shutting down ride-service ---"
kill -9 $RIDE_PID
