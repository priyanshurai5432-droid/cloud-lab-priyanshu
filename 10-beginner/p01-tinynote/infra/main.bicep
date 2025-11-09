// TinyNote Azure Infrastructure (Simplified for Students)
targetScope = 'subscription'

param location string = 'centralindia'
param projectName string = 'tinynote'

var resourceGroupName = 'rg-${projectName}'
var storageAccountName = 'st${projectName}${uniqueString(subscription().id)}'
var functionAppName = 'func-${projectName}-${uniqueString(subscription().id)}'
var functionPlanName = 'plan-${projectName}'

// Resource Group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
  tags: { project: projectName }
}

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-06-01' = {
  scope: resourceGroup
  name: storageAccountName
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: { accessTier: 'Hot' }
}

// Blob Container
resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-06-01' = {
  name: '${storageAccountName}/default/notes'
  properties: { publicAccess: 'None' }
}

// Function Plan
resource functionPlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  scope: resourceGroup
  name: functionPlanName
  location: location
  kind: 'functionapp'
  sku: { name: 'Y1', tier: 'Dynamic' }
}

// Function App
resource functionApp 'Microsoft.Web/sites@2021-02-01' = {
  scope: resourceGroup
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: functionPlan.id
    siteConfig: {
      appSettings: [
        { name: 'FUNCTIONS_WORKER_RUNTIME', value: 'python' }
        { name: 'NOTES_STORAGE_CONNECTION', value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net' }
        { name: 'NOTES_CONTAINER', value: 'notes' }
      ]
      linuxFxVersion: 'PYTHON|3.11'
    }
  }
}

output functionAppUrl string = 'https://${functionApp.properties.defaultHostName}'
output storageAccountName string = storageAccountName
