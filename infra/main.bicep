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