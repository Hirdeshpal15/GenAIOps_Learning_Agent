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
