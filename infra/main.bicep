@description('Azure region')
param location string = resourceGroup().location

@description('Azure OpenAI service name')
param openAIServiceName string = 'genaiops-openai'

resource openAI 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: openAIServiceName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    publicNetworkAccess: 'Enabled'
  }
}

output openAIEndpoint string = openAI.properties.endpoint

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'genaiops-appinsights'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

output applicationInsightsConnectionString string = appInsights.properties.ConnectionString

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'genaiops-loganalytics'
  location: location

  properties: {
    sku: {
      name: 'PerGB2018'
    }

    retentionInDays: 30
  }
}

output logAnalyticsWorkspaceId string = logAnalytics.id

@description('Key Vault name')
param keyVaultName string = 'genaiopskv${uniqueString(resourceGroup().id)}'

resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId

    sku: {
      family: 'A'
      name: 'standard'
    }

    enableRbacAuthorization: true

    accessPolicies: []

    publicNetworkAccess: 'Enabled'
  }
}

output keyVaultName string = keyVault.name

@description('Azure AI Search service name')
param searchServiceName string = 'genaiopssearch${uniqueString(resourceGroup().id)}'

resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServiceName
  location: location
  sku: {
    name: 'basic'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
  }
}

output searchServiceName string = searchService.name

resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'genaiops-managed-identity'
  location: location
}

output managedIdentityPrincipalId string = managedIdentity.properties.principalId

@description('Azure Container Registry name')
param acrName string = 'genaiopsacr${uniqueString(resourceGroup().id)}'

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location

  sku: {
    name: 'Basic'
  }

  properties: {
    adminUserEnabled: true
  }
}

output acrLoginServer string = acr.properties.loginServer

resource containerEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: 'genaiops-container-env'

  location: location

  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'

      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId

        sharedKey: listKeys(logAnalytics.id, '2022-10-01').primarySharedKey
      }
    }
  }
}

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'genaiops-api'

  location: location

  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentity.id}': {}
    }
  }

  properties: {
    managedEnvironmentId: containerEnv.id

    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }

      registries: [
        {
          server: acr.properties.loginServer
          username: acr.listCredentials().username
          passwordSecretRef: 'acr-password'
        }
      ]

      secrets: [
        {
          name: 'acr-password'
          value: acr.listCredentials().passwords[0].value
        }
      ]
    }

    template: {
      containers: [
        {
          name: 'genaiops-api'

          image: 'genaiopsacrgl362bkpewhfs.azurecr.io/genaiops-api:v1'

          env: [
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              value: 'AZURE_OPENAI_ENDPOINT'
            }
            {
              name: 'AZURE_OPENAI_API_KEY'
              value: 'AZURE_OPENAI_API_KEY'
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT'
              value: 'AZURE_OPENAI_DEPLOYMENT'
            }
            {
              name: 'AZURE_SEARCH_SERVICE'
              value: 'AZURE_SEARCH_SERVICE'
            }
            {
              name: 'AZURE_SEARCH_KEY'
              value: 'AZURE_SEARCH_KEY'
            }
          ]

          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
    }
  }
}

output containerAppUrl string = containerApp.properties.configuration.ingress.fqdn
