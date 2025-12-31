import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter } from 'recharts'
import { AlertTriangle, TrendingUp, Activity, Zap } from 'lucide-react'

export default function Monitoring() {
  const driftData = [
    { feature: 'age', drift: 0.02 },
    { feature: 'income', drift: 0.15 },
    { feature: 'location', drift: 0.08 },
    { feature: 'score', drift: 0.23 },
    { feature: 'frequency', drift: 0.05 },
  ]

  const performanceData = [
    { time: '00:00', latency: 45, throughput: 120 },
    { time: '04:00', latency: 42, throughput: 115 },
    { time: '08:00', latency: 52, throughput: 145 },
    { time: '12:00', latency: 48, throughput: 138 },
    { time: '16:00', latency: 55, throughput: 152 },
    { time: '20:00', latency: 50, throughput: 140 },
  ]

  const predictionDistribution = [
    { actual: 0.1, predicted: 0.12 },
    { actual: 0.3, predicted: 0.28 },
    { actual: 0.5, predicted: 0.52 },
    { actual: 0.7, predicted: 0.68 },
    { actual: 0.9, predicted: 0.91 },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Monitoring</h1>
          <p className="text-muted-foreground">Real-time model performance and drift detection</p>
        </div>
        <Button>
          <Activity className="mr-2 h-4 w-4" />
          Run Drift Check
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Drift Score</CardTitle>
            <AlertTriangle className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0.23</div>
            <p className="text-xs text-yellow-600">
              Moderate drift detected
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Latency</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">48ms</div>
            <p className="text-xs text-muted-foreground">
              Within SLA target
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Throughput</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">138/s</div>
            <p className="text-xs text-muted-foreground">
              +12% from baseline
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Error Rate</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0.2%</div>
            <p className="text-xs text-green-600">
              Excellent performance
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Feature Drift Detection</CardTitle>
            <CardDescription>Drift scores by feature</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={driftData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="feature" className="text-xs" />
                <YAxis className="text-xs" />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }} />
                <Bar dataKey="drift" fill="hsl(var(--primary))" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Performance Metrics</CardTitle>
            <CardDescription>Latency and throughput over time</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="time" className="text-xs" />
                <YAxis className="text-xs" />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }} />
                <Line type="monotone" dataKey="latency" stroke="hsl(var(--primary))" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Prediction Quality</CardTitle>
          <CardDescription>Actual vs predicted values distribution</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis dataKey="actual" name="Actual" className="text-xs" />
              <YAxis dataKey="predicted" name="Predicted" className="text-xs" />
              <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }} />
              <Scatter data={predictionDistribution} fill="hsl(var(--primary))" />
            </ScatterChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Active Alerts</CardTitle>
          <CardDescription>Recent monitoring alerts</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { severity: 'warning', message: 'Feature drift detected on "score" (0.23)', time: '5 minutes ago' },
              { severity: 'info', message: 'Model performance within normal range', time: '1 hour ago' },
              { severity: 'warning', message: 'Increased latency on deployment "sentiment-prod"', time: '2 hours ago' },
            ].map((alert, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 border border-border rounded-lg">
                <AlertTriangle className={`h-5 w-5 mt-0.5 ${alert.severity === 'warning' ? 'text-yellow-600' : 'text-blue-600'}`} />
                <div className="flex-1">
                  <p className="text-sm font-medium">{alert.message}</p>
                  <p className="text-xs text-muted-foreground">{alert.time}</p>
                </div>
                <Button variant="ghost" size="sm">Dismiss</Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
