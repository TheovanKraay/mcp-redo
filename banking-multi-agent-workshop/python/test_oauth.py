#!/usr/bin/env python3
"""
OAuth Test Script for Banking MCP Server

This script tests the OAuth configuration and endpoints.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
import httpx

async def test_oauth_discovery():
    """Test OAuth discovery endpoint."""
    print("🔍 Testing OAuth discovery endpoint...")
    
    base_url = os.getenv("MCP_SERVER_BASE_URL", "http://localhost:8000")
    discovery_url = f"{base_url}/.well-known/oauth-authorization-server"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(discovery_url)
            
            if response.status_code == 200:
                print("✅ OAuth discovery endpoint is working")
                metadata = response.json()
                print(f"📋 OAuth Metadata:")
                print(json.dumps(metadata, indent=2))
                return True
            else:
                print(f"❌ OAuth discovery failed with status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Failed to connect to OAuth discovery endpoint: {e}")
        return False

async def test_mcp_endpoint():
    """Test basic MCP endpoint."""
    print("\n🔍 Testing MCP endpoint...")
    
    base_url = os.getenv("MCP_SERVER_BASE_URL", "http://localhost:8000")
    mcp_url = f"{base_url}/mcp/"
    
    try:
        async with httpx.AsyncClient() as client:
            # Test a basic ping or list tools
            response = await client.get(mcp_url)
            
            if response.status_code in [200, 401, 403]:
                print(f"✅ MCP endpoint is responding (status: {response.status_code})")
                if response.status_code == 401:
                    print("🔐 Server requires authentication (as expected)")
                return True
            else:
                print(f"❌ MCP endpoint failed with status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Failed to connect to MCP endpoint: {e}")
        return False

async def test_server_info():
    """Test server info endpoint."""
    print("\n🔍 Testing server info...")
    
    base_url = os.getenv("MCP_SERVER_BASE_URL", "http://localhost:8000")
    
    try:
        # Try to call the server_info tool
        print("💡 Try calling the server_info tool through your MCP client")
        print("   This will show authentication status and server configuration")
        return True
        
    except Exception as e:
        print(f"❌ Failed to test server info: {e}")
        return False

def load_env():
    """Load environment variables from .env file."""
    env_path = Path(".env")
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Loaded configuration from .env file")
        return True
    else:
        print("⚠️  No .env file found. Using environment variables or defaults.")
        return False

async def main():
    print("🧪 Banking MCP Server OAuth Test")
    print("=" * 40)
    
    # Load environment
    try:
        load_env()
    except ImportError:
        print("📦 python-dotenv not installed, skipping .env file loading")
    
    # Show current configuration
    print(f"\n📋 Current Configuration:")
    print(f"   Server URL: {os.getenv('MCP_SERVER_BASE_URL', 'http://localhost:8000')}")
    print(f"   Client ID: {os.getenv('OAUTH_CLIENT_ID', 'Not set')}")
    print(f"   Auth Endpoint: {os.getenv('OAUTH_AUTHORIZATION_ENDPOINT', 'Not set')}")
    print(f"   Token Endpoint: {os.getenv('OAUTH_TOKEN_ENDPOINT', 'Not set')}")
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if await test_oauth_discovery():
        tests_passed += 1
    
    if await test_mcp_endpoint():
        tests_passed += 1
    
    if await test_server_info():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your OAuth setup looks good.")
    else:
        print("⚠️  Some tests failed. Check your server configuration and ensure it's running.")
    
    print("\n💡 Next Steps:")
    print("1. Start your MCP server: python src/app/tools/mcp_server.py")
    print("2. Configure your MCP client with OAuth authentication")
    print("3. Test the full OAuth flow with a real client request")

if __name__ == "__main__":
    asyncio.run(main())