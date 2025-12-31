import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Package, ArrowUpCircle, CheckCircle, Clock } from 'lucide-react'

export default function ModelRegistry() {
  const models = [
    { 
      id: 1, 
      name: 'sentiment-classifier', 
      versions: 5, 
      latestVersion: 'v1.5.0', 
      stage: 'production',
      framework: 'PyTorch',
      accuracy: 0.94
    },
    { 
      id: 2, 
      name: 'recommendation-engine', 
      versions: 8, 
      latestVersion: 'v2.1.3', 
      stage: 'staging',
      framework: 'TensorFlow',
      accuracy: 0.89
    },
    { 
      id: 3, 
      name: 'fraud-detection', 
      versions: 12, 
      latestVersion: 'v3.0.0', 
      stage: 'production',
      framework: 'XGBoost',
      accuracy: 0.97
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Model Registry</h1>
          <p className="text-muted-foreground">Manage model versions and deployments</p>
        </div>
        <Button>
          <ArrowUpCircle className="mr-2 h-4 w-4" />
          Register Model
        </Button>
      </div>

      <div className="grid gap-4">
        {models.map((model) => (
          <Card key={model.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <Package className="h-8 w-8 text-primary" />
                  <div>
                    <CardTitle>{model.name}</CardTitle>
                    <CardDescription className="flex items-center gap-3 mt-1">
                      <span>{model.latestVersion}</span>
                      <span>•</span>
                      <span>{model.framework}</span>
                      <span>•</span>
                      <span>{model.versions} versions</span>
                    </CardDescription>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {model.stage === 'production' ? (
                    <span className="flex items-center gap-1 text-sm px-3 py-1 rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                      <CheckCircle className="h-3 w-3" />
                      Production
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-sm px-3 py-1 rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                      <Clock className="h-3 w-3" />
                      Staging
                    </span>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-sm text-muted-foreground">Accuracy</p>
                  <p className="text-2xl font-bold">{(model.accuracy * 100).toFixed(1)}%</p>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">View Versions</Button>
                  <Button variant="outline" size="sm">Promote</Button>
                  <Button size="sm">Deploy</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
