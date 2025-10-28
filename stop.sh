#!/bin/bash

# Solar PV Dashboard Stop Script

echo "🛑 Stopping Solar PV Dashboard..."
echo ""

cd ~/solar-pv-dashboard
docker compose down

echo ""
echo "✅ Dashboard stopped successfully!"
echo ""
echo "🚀 To start again, run:"
echo "   bash ~/solar-pv-dashboard/start.sh"
echo ""
