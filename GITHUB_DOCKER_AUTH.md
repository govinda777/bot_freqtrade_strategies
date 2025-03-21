# GitHub Container Registry Authentication for CI/CD Pipelines

This guide explains how to set up GitHub Container Registry (GHCR) authentication using Personal Access Tokens (PAT) for your CI/CD pipelines. GitHub Container Registry offers a secure alternative to Docker Hub for storing and managing your Docker images directly within your GitHub organization or account.

## Benefits of Using GitHub Container Registry

- **Integrated with GitHub**: Native integration with GitHub repositories, issues, and permissions
- **Private packages**: Store your Docker images privately within your GitHub account or organization
- **Fine-grained permissions**: Control access with GitHub's permission model
- **Free storage**: Free storage for public packages and generous allocation for private packages
- **Enhanced security**: Integrates with GitHub security features like Dependabot and CodeQL

## Setup Instructions

### 1. Create a GitHub Personal Access Token (PAT)

1. Log in to your GitHub account
2. Click on your profile picture in the top-right corner and select "Settings"
3. In the left sidebar, click on "Developer settings"
4. Select "Personal access tokens" → "Tokens (classic)"
5. Click "Generate new token" → "Generate new token (classic)"
6. Fill in the required information:
   - **Note**: Choose a descriptive name (e.g., "bot_freqtrade_strategies_ghcr")
   - **Expiration**: Choose an expiration period based on your security requirements
   - **Scopes**:
     - Select `repo` (full control)
     - Select `write:packages` (to publish packages)
     - Select `read:packages` (to download packages)
     - Select `delete:packages` (to delete packages)
7. Click "Generate token"
8. **IMPORTANT**: Copy the token immediately - it will only be displayed once and cannot be retrieved later

Example token format: `ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890` (This is an example - never share your actual token!)

### 2. Add the Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Create a new secret:
   - **Name**: `GITHUB_TOKEN_PAT`
   - **Value**: Paste the GitHub personal access token you created
5. Click "Add secret"

### 3. Update Your GitHub Workflow Files

Add or modify the Docker login action in your workflow files (`.github/workflows/frontend.yml` and `.github/workflows/backend.yml`) to use GitHub Container Registry:

```yaml
- name: Login to GitHub Container Registry
  if: github.event_name != 'pull_request'
  id: ghcr-login
  uses: docker/login-action@v2
  with:
    registry: ghcr.io
    username: ${{ github.repository_owner }}
    password: ${{ secrets.GITHUB_TOKEN_PAT }}
  continue-on-error: true
```

Update the image tags to use GitHub Container Registry format:

```yaml
tags: |
  ghcr.io/${{ github.repository_owner }}/freqtrade-frontend:latest
  ghcr.io/${{ github.repository_owner }}/freqtrade-frontend:${{ github.sha }}
```

### 4. Working with GitHub Container Registry

#### Pulling Images

To pull images from GitHub Container Registry:

```bash
docker pull ghcr.io/your-username/freqtrade-frontend:latest
```

#### Running Images

To run images from GitHub Container Registry:

```bash
docker run ghcr.io/your-username/freqtrade-frontend:latest
```

## Package Visibility and Permissions

GitHub Container Registry packages can have different visibility settings:

- **Public**: Anyone can view and download the package
- **Private**: Only users with appropriate permissions can view and download the package
- **Internal**: Only users within your organization can view and download the package

You can manage package visibility and permissions in the GitHub interface:

1. Go to your GitHub profile or organization
2. Click on "Packages"
3. Select the package you want to manage
4. Click on "Package settings"
5. Under "Danger Zone," you can change the visibility
6. Under "Manage Actions access," you can configure specific access controls

## Security Best Practices

- Use a dedicated PAT for CI/CD pipelines with the minimum required permissions
- Regularly rotate your PATs, especially if they have broad permissions
- Set expiration dates on PATs so they automatically become invalid
- Use GitHub's organization secrets for team environments
- Consider using GITHUB_TOKEN for public repositories when possible
- Audit your PATs and package permissions regularly

## Troubleshooting

If you encounter authentication issues:

1. Verify that your PAT hasn't expired
2. Confirm that the PAT has the necessary scopes (`write:packages`, `read:packages`)
3. Check that your secret is correctly set in GitHub Secrets
4. Ensure the repository visibility and package visibility settings are compatible
5. Verify that your workflow file is using the correct registry URL (`ghcr.io`)