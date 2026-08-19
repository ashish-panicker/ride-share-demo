#!/bin/bash

echo "Starting passenger-service..."
# Start the service in the background
mvn spring-boot:run -f pasenger-service/pom.xml > passenger.log 2>&1 &
PID=$!

echo "Waiting for service to start on port 8081..."
for i in {1..30}; do
    if curl -s http://localhost:8081/actuator/health > /dev/null; then
        echo -e "\n--- passenger-service is up! ---\n"
        break
    fi
    sleep 2
done

echo "1. Creating a new passenger (POST /api/passengers)..."
CREATE_RESPONSE=$(curl -s -X POST http://localhost:8081/api/passengers \
    -H "Content-Type: application/json" \
    -d '{"name": "Alice Wonderland", "email": "alice@example.com"}')
echo "Response: $CREATE_RESPONSE"

# Extract ID for the next steps (assuming response has 'id' field, e.g. {"id":1,...})
PASSENGER_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ -z "$PASSENGER_ID" ]; then
    echo "Failed to create passenger. Exiting."
    kill -9 $PID
    exit 1
fi

echo -e "\n2. Fetching all passengers (GET /api/passengers)..."
curl -s http://localhost:8081/api/passengers

echo -e "\n\n3. Fetching the created passenger by ID (GET /api/passengers/$PASSENGER_ID)..."
curl -s http://localhost:8081/api/passengers/$PASSENGER_ID

echo -e "\n\n4. Updating the passenger (PUT /api/passengers/$PASSENGER_ID)..."
curl -s -X PUT http://localhost:8081/api/passengers/$PASSENGER_ID \
    -H "Content-Type: application/json" \
    -d '{"name": "Alice W.", "email": "alice.w@example.com"}'

echo -e "\n\n5. Verifying the update (GET /api/passengers/$PASSENGER_ID)..."
curl -s http://localhost:8081/api/passengers/$PASSENGER_ID

echo -e "\n\n--- Tests Completed. Shutting down service ---"
kill -9 $PID
