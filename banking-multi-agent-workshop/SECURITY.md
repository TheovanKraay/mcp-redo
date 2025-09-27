# Security Documentation
## MCP Banking Server Authentication

This document provides comprehensive security guidance for the MCP Banking Server, covering both **Simple Token Authentication** (ready out-of-the-box) and **GitHub OAuth** (production-grade security).

---

## � **Quick Start - Default Authentication**

**Your server is ready to use immediately with Simple Token Authentication!**

### **1. Start the Servers (No Setup Required)**

```bash
# Terminal 1: Start MCP Server (with Simple Token Auth)
cd /path/to/banking-multi-agent-workshop/python
source .venv/bin/activate
python3 -m src.app.tools.mcp_server

# Terminal 2: Start FastAPI Server  
source .venv/bin/activate
uvicorn src.app.banking_agents_api:app --host 0.0.0.0 --port 8001 --reload
```

### **2. Authentication Status**
You'll see this output confirming simple token auth is active:
```
✅ SIMPLE TOKEN MODE ENABLED (Development)
   Token: banking-...
   🚀 Ready to use - no setup required!
   💡 For production, configure GitHub OAuth (see below)
```

**That's it! Your banking server is secured and ready to use.**

---

## 🔐 **Architecture Overview**

The MCP Banking Server implements **layered authentication** with automatic fallback:

```
┌─────────────────┐    Priority 1    ┌─────────────────┐    Priority 2    ┌─────────────────┐
│                 │ ──────────────→  │                 │ ──────────────→  │                 │
│  GitHub OAuth   │                  │  Simple Token   │                  │  No Auth       │
│  (Production)   │                  │  (Development)  │                  │  (Fallback)    │
│                 │                  │                 │                  │                 │
└─────────────────┘                  └─────────────────┘                  └─────────────────┘
     CONFIGURED                          DEFAULT                           DISABLED
```

### **Authentication Priority Logic:**

1. **GitHub OAuth** - If `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are configured
2. **Simple Token** - If `MCP_AUTH_TOKEN` is set (default)
3. **No Authentication** - If no credentials are configured

---

## 🔧 **Configuration Files**

### **Default Configuration (`.env.oauth`)**
```bash
# SIMPLE TOKEN AUTHENTICATION (DEFAULT - ACTIVE)
MCP_AUTH_TOKEN=banking-server-dev-token-2024

# GITHUB OAUTH AUTHENTICATION (PRODUCTION - COMMENTED OUT)  
# GITHUB_CLIENT_ID=your_github_client_id_here
# GITHUB_CLIENT_SECRET=your_github_client_secret_here

MCP_SERVER_BASE_URL=http://localhost:8000
```

---

## 🛡️ **Simple Token Authentication (Default)**

### **How It Works:**
- ✅ **Active by Default** - No setup required
- 🔑 **Bearer Token** - Uses `Authorization: Bearer <token>` header
- 🚀 **Development Ready** - Perfect for development and testing
- 🔐 **Configurable** - Change token in `.env.oauth`

### **Security Features:**
- Request validation on all banking operations
- Configurable token (change from default)
- Debug logging for authentication events
- Ready for development and testing

### **Customizing the Token:**
```bash
# Edit .env.oauth
MCP_AUTH_TOKEN=your-custom-secure-token-here
```

**⚠️ For Production:** Use a long, random, secure token and consider GitHub OAuth instead.

---

---

## 🏭 **GitHub OAuth Authentication (Production)**

### **When to Upgrade:**
- Moving to production environment
- Need user-based access control
- Require audit trails and user identification
- Enterprise security requirements

### **Setup Steps:**

#### **1. Register GitHub OAuth Application**

1. **Navigate to GitHub Developer Settings**
   - Go to: [GitHub OAuth Apps](https://github.com/settings/applications/new)
   - Login to your GitHub account

2. **Create New OAuth Application**
   ```
   Application name: MCP Banking Server Production
   Homepage URL: https://your-domain.com (or http://localhost:8000 for testing)
   Authorization callback URL: https://your-domain.com/auth/github/callback
   Application description: Production MCP server for banking operations
   ```

3. **Save Credentials Securely**
   - Copy the **Client ID** 
   - Generate and copy a **Client Secret**
   - **🔒 Store in secure credential management system**

#### **2. Enable GitHub OAuth**

Edit `.env.oauth` and uncomment the GitHub OAuth section:
```bash
# SIMPLE TOKEN AUTHENTICATION (WILL BE DISABLED)
MCP_AUTH_TOKEN=banking-server-dev-token-2024

# GITHUB OAUTH AUTHENTICATION (PRODUCTION - ENABLE THIS)
GITHUB_CLIENT_ID=your_actual_github_client_id
GITHUB_CLIENT_SECRET=your_actual_github_client_secret

MCP_SERVER_BASE_URL=https://your-domain.com
```

#### **3. Restart Server**
The server will automatically detect GitHub OAuth credentials and switch modes:
```
✅ GITHUB OAUTH MODE ENABLED
   Callback URL: https://your-domain.com/auth/github/callback
   🔒 Production-grade authentication active
```

### **GitHub OAuth Security Features:**
- ✅ **User Identity Verification** - Real GitHub user authentication
- 🔐 **OAuth 2.0 Standard** - Industry-standard security protocol  
- 🔄 **Automatic Token Refresh** - Handles token lifecycle
- 📊 **Audit Logging** - User actions tracked to GitHub identity
- 🛡️ **Scope-based Access** - Minimal required permissions

---

## 🧪 **Testing & Validation**

### **Test Simple Token Authentication**

1. **Check Server Status:**
   ```bash
   curl http://localhost:8000/mcp/tools/server_info
   ```

2. **Test Without Token (should fail):**
   ```bash
   curl http://localhost:8000/mcp/tools/create_account
   ```

3. **Test With Token (should succeed):**
   ```bash
   curl -H "Authorization: Bearer banking-server-dev-token-2024" \
        http://localhost:8000/mcp/tools/create_account
   ```

### **Test GitHub OAuth (Production)**

1. **Verify OAuth Endpoints:**
   ```bash
   curl http://localhost:8000/.well-known/oauth-authorization-server
   ```

2. **Test OAuth Flow:**
   - Navigate to server in browser
   - Should redirect to GitHub authentication
   - Complete OAuth flow and verify access

---

## 🚨 **Security Best Practices**

### **Simple Token (Development)**

✅ **Good for:**
- Local development
- Testing and debugging
- Internal team environments
- Rapid prototyping

⚠️ **Security considerations:**
- Change default token immediately
- Use long, random tokens (32+ characters)
- Never commit tokens to version control
- Rotate tokens regularly

### **GitHub OAuth (Production)**

✅ **Good for:**
- Production deployments
- User-facing applications
- Enterprise environments  
- Regulatory compliance requirements

🔒 **Security requirements:**
- HTTPS only (no HTTP in production)
- Secure client secret storage
- Regular security audits
- Monitor authentication logs

### **Production Deployment Checklist**

- [ ] **HTTPS Enabled** - No HTTP traffic allowed
- [ ] **Secure Secrets** - Use environment variables or secret management
- [ ] **Token Rotation** - Regular credential updates
- [ ] **Access Logging** - Monitor all authentication attempts
- [ ] **Error Handling** - No sensitive information in error messages
- [ ] **Rate Limiting** - Prevent brute force attacks
- [ ] **CORS Configuration** - Restrict allowed origins
- [ ] **Security Headers** - Implement security-focused HTTP headers

---

## 🔧 **Configuration Reference**

### **Environment Variables**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MCP_AUTH_TOKEN` | Optional | `banking-server-dev-token-2024` | Simple token for development |
| `GITHUB_CLIENT_ID` | Optional | - | GitHub OAuth App Client ID |
| `GITHUB_CLIENT_SECRET` | Optional | - | GitHub OAuth App Client Secret |
| `MCP_SERVER_BASE_URL` | Optional | `http://localhost:8000` | Base URL for callbacks |

### **Authentication Modes**

| Mode | Trigger | Security Level | Use Case |
|------|---------|---------------|----------|
| `github_oauth` | GitHub credentials set | High | Production |
| `simple_token` | MCP_AUTH_TOKEN set | Medium | Development |
| `none` | No credentials | None | Testing only |

---

## 🛠️ **Troubleshooting**

### **Simple Token Issues**

**"Token not found"**
- Check `.env.oauth` file exists
- Verify `MCP_AUTH_TOKEN` is set
- Restart server to reload configuration

**"Authentication failed"** 
- Ensure client sends `Authorization: Bearer <token>` header
- Verify token matches server configuration
- Check for typos in token value

### **GitHub OAuth Issues**

**"OAuth credentials not found"**
- Verify both `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are set
- Check credentials are not commented out
- Ensure no extra spaces in credential values

**"Callback URL mismatch"**
- GitHub OAuth app callback must match `MCP_SERVER_BASE_URL/auth/github/callback`
- Update GitHub OAuth app settings if URL changed
- Use exact URL (no trailing slashes)

### **Debug Mode**

Enable detailed authentication logging:
```bash
export LOG_LEVEL=DEBUG
python3 -m src.app.tools.mcp_server
```

---

## � **Migration Guide**

### **Development → Production**

1. **Backup Configuration**
   ```bash
   cp .env.oauth .env.oauth.backup
   ```

2. **Register GitHub OAuth App** (see steps above)

3. **Update Configuration**
   ```bash
   # Uncomment and set GitHub credentials
   GITHUB_CLIENT_ID=your_production_client_id
   GITHUB_CLIENT_SECRET=your_production_client_secret
   MCP_SERVER_BASE_URL=https://your-production-domain.com
   ```

4. **Deploy with HTTPS**
   - Use reverse proxy (nginx, Cloudflare)
   - Enable TLS/SSL certificates
   - Update callback URLs to HTTPS

5. **Test OAuth Flow**
   - Verify redirect to GitHub works
   - Complete authentication successfully
   - Confirm banking tools are accessible

---

*Last Updated: September 27, 2025*  
*Security Review: ✅ Simple Token Ready | ⚠️ GitHub OAuth Requires Production Setup*