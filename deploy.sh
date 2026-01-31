#!/bin/bash

# Quick Deploy Script for Gary's Lead Generation Engine

echo "=================================="
echo "🚀 DEPLOYING TO GITHUB"
echo "=================================="
echo ""

# Add all files
echo "📦 Adding files..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Deploy: Gary's Lead Generation Engine with web UI"

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push origin main

echo ""
echo "=================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Go to https://render.com"
echo "2. Sign up with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your repository"
echo "5. Deploy!"
echo ""
echo "Your app will be live in ~3 minutes! 🎉"
echo ""
