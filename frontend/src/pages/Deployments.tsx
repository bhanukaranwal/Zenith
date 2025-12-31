import { useQuery } from '@tanstack/react-query'
import { deploymentsApi } from '../lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Rocket, Activity, TrendingUp, Clock } from 'lucide-react'

export default function Deployments() {
  const { data: deployments, isLoading } = useQuery({
    queryKey: ['deployments'],
    queryFn: async () => (await deploymentsApi.list()).data,
  })

  const mockDeployments = [
    { 
      id: 1, 
      name: 'sentiment-prod', 
      model: 'sentiment-classifier v1.5.0',
      status: 'running',
      requests: 12450,
      latency: 45,
      uptime: '99.9%'
    },
    { 
      id: 2, 
      name: 'recommendation-staging', 
      model: 'recommendation-engine v2.1.3',
      status: 'running',
      requests: 3420,
      latency: 78,
      uptime: '99.5%'
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Deployments</h1>
          <p className="text-muted-foreground">Manage model deployments and endpoints</p>
        </div>
        <Button>
          <Rocket className="mr-2 h-4 w-4" />
          New Deployment
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Requests</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">15,870</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="inline h-3 w-3 mr-1" />
              +18% from last hour
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Latency</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">52ms</div>
            <p className="text-xs text-muted-foreground">
              -5ms from average
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">99.8%</div>
            <p className="text-xs text-muted-foreground">
              Excellent performance
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4">
        {mockDeployments.map((deployment) => (
          <Card key={deployment.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <Rocket className="h-8 w-8 text-primary" />
                  <div>
                    <CardTitle>{deployment.name}</CardTitle>
                    <CardDescription>{deployment.model}</CardDescription>
                  </div>
                </div>
                <span className="flex items-center gap-1 text-sm px-3 py-1 rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  <Activity className="h-3 w-3" />
                  {deployment.status}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-sm text-muted-foreground">Requests</p>
                  <p className="text-xl font-bold">{deployment.requests.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Latency</p>
                  <p className="text-xl font-bold">{deployment.latency}ms</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Uptime</p>
                  <p className="text-xl font-bold">{deployment.uptime}</p>
                </div>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">Logs</Button>
                <Button variant="outline" size="sm">Metrics</Button>
                <Button variant="outline" size="sm">Scale</Button>
                <Button variant="destructive" size="sm">Stop</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
