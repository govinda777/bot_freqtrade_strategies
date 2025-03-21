# Docker Hub Authentication for CI/CD Pipelines

This guide explains how to set up Docker Hub authentication using personal access tokens for your CI/CD pipelines. This method provides enhanced security by using tokens instead of your Docker Hub password.

## Benefits of Using Personal Access Tokens

- **Better security**: You can revoke tokens independently of your password
- **Fine-grained permissions**: Assign read, write, or delete permissions
- **Audit trail**: Track token usage for better security monitoring
- **Expiration control**: Set tokens to expire or use non-expiring tokens based on your security needs

## Setup Instructions

### 1. Create a Docker Hub Personal Access Token

1. Log in to your Docker Hub account at [hub.docker.com](https://hub.docker.com/)
2. Click on your username in the top-right corner and select "Account Settings"
3. In the left sidebar, click on "Security"
4. Select "New Access Token"
5. Fill in the required information:
   - **Access token description**: Choose a descriptive name (e.g., "bot_freqtrade_strategies")
   - **Access permissions**: Select appropriate permissions (e.g., "Read, Write, Delete")
   - **Expires**: Choose an expiration period or select "Never" for non-expiring tokens
6. Click "Generate" to create the token
7. **IMPORTANT**: Copy the token immediately - it will only be displayed once and cannot be retrieved later

### 2. Add the Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Create a new secret:
   - **Name**: `DOCKER_TOKEN`
   - **Value**: Paste the Docker Hub personal access token you created
5. Click "Add secret"

Make sure you also have the `DOCKER_USERNAME` secret set with your Docker Hub username.

### 3. How the CI/CD Pipeline Uses the Token

The CI/CD pipeline workflows `.github/workflows/frontend.yml` and `.github/workflows/backend.yml` are configured to use these secrets for Docker Hub authentication:

```yaml
- name: Login to Docker Hub
  if: github.event_name != 'pull_request'
  id: docker-login
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_TOKEN }}
  continue-on-error: true
```

## Testing Docker Hub Authentication Locally

You can verify that your token works by logging in to Docker Hub from the command line:

1. Run: `docker login -u your_username`
2. When prompted for a password, enter your personal access token
3. You should see a "Login Succeeded" message

## Token Security Best Practices

- Regularly rotate tokens, especially for production environments
- Use tokens with the minimum required permissions
- Set expiration dates on tokens unless there's a specific need for a non-expiring token
- Audit token usage regularly
- Revoke tokens immediately if they are compromised

## Troubleshooting

If authentication fails, check the following:

1. Verify that your token hasn't expired
2. Confirm that the token has the necessary permissions
3. Ensure the `DOCKER_USERNAME` and `DOCKER_TOKEN` secrets are correctly set in GitHub
4. Check if there are any Docker Hub service issues