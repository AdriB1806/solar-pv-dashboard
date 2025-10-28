#!/bin/bash

# Solar PV Dashboard Startup Script
# This script makes it easy to start your dashboard

echo "🌞 Solar PV Dashboard Startup Script"
echo "===================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "⚠️  Docker is not running!"
    echo "📱 Opening Docker Desktop..."
    open -a Docker
    echo "⏳ Waiting for Docker to start (this may take 30-60 seconds)..."
    
    # Wait for Docker to be ready
    while ! docker info > /dev/null 2>&1; do
        sleep 2
        echo -n "."
    done
    echo ""
    echo "✅ Docker is now running!"
    sleep 3
fi

echo ""
echo "🏗️  Building and starting containers..."
echo ""

# Navigate to project directory
cd ~/solar-pv-dashboard

# Start Docker Compose
docker compose up --build -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if containers are running
if docker compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Dashboard is ready!"
    echo ""
    echo "🌐 Open your browser and go to:"
    echo "   📊 Dashboard: http://localhost:8501"
    echo "   📈 Prometheus: http://localhost:9090"
    echo "   📉 Metrics: http://localhost:8000/metrics"
    echo ""
    echo "🛑 To stop the dashboard, run:"
    echo "   cd ~/solar-pv-dashboard && docker compose down"
    echo ""
    echo "📖 For more information, see README.md"
    echo ""
    
    # Open dashboard in browser
    sleep 3
    open http://localhost:8501
else
    echo ""
    echo "❌ Something went wrong. Check the logs with:"
    echo "   cd ~/solar-pv-dashboard && docker compose logs"
fi
