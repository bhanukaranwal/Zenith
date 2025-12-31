import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Database, Upload, Calendar } from 'lucide-react'

export default function Datasets() {
  const datasets = [
    { id: 1, name: 'customer_data_v1', rows: 125000, features: 45, size: '2.3 GB', created: '2025-12-15' },
    { id: 2, name: 'transaction_logs', rows: 890000, features: 23, size: '8.1 GB', created: '2025-12-10' },
    { id: 3, name: 'user_behavior', rows: 450000, features: 67, size: '5.2 GB', created: '2025-12-05' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Datasets</h1>
          <p className="text-muted-foreground">Manage versioned datasets with lineage tracking</p>
        </div>
        <Button>
          <Upload className="mr-2 h-4 w-4" />
          Upload Dataset
        </Button>
      </div>

      <div className="grid gap-4">
        {datasets.map((dataset) => (
          <Card key={dataset.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <Database className="h-8 w-8 text-primary" />
                  <div>
                    <CardTitle>{dataset.name}</CardTitle>
                    <CardDescription className="flex items-center gap-4 mt-1">
                      <span>{dataset.rows.toLocaleString()} rows</span>
                      <span>•</span>
                      <span>{dataset.features} features</span>
                      <span>•</span>
                      <span>{dataset.size}</span>
                    </CardDescription>
                  </div>
                </div>
                <div className="flex items-center text-sm text-muted-foreground">
                  <Calendar className="mr-2 h-4 w-4" />
                  {dataset.created}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">View Schema</Button>
                <Button variant="outline" size="sm">Statistics</Button>
                <Button variant="outline" size="sm">Lineage</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
