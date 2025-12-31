import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { experimentsApi, projectsApi } from '../lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { FlaskConical, Play, TrendingUp, Clock, CheckCircle, XCircle } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function Experiments() {
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null)

  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => (await projectsApi.list()).data,
  })

  const runs = [
    { id: 1, name: 'baseline-v1', status: 'completed', accuracy: 0.92, loss: 0.15, duration: '12m 34s' },
    { id: 2, name: 'optimized-lr', status: 'completed', accuracy: 0.94, loss: 0.12, duration: '15m 21s' },
    { id: 3, name: 'batch-size-exp', status: 'running', accuracy: 0.93, loss: 0.13, duration: '8m 45s' },
    { id: 4, name: 'dropout-tuning', status: 'failed', accuracy: 0.87, loss: 0.22, duration: '5m 12s' },
  ]

  const metricsData = [
    { step: 0, accuracy: 0.65, loss: 0.45 },
    { step: 100, accuracy: 0.78, loss: 0.32 },
    { step: 200, accuracy: 0.85, loss: 0.24 },
    { step: 300, accuracy: 0.89, loss: 0.18 },
    { step: 400, accuracy: 0.92, loss: 0.15 },
    { step: 500, accuracy: 0.94, loss: 0.12 },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Experiments</h1>
          <p className="text-muted-foreground">Track and compare ML experiments</p>
        </div>
        <Button>
          <Play className="mr-2 h-4 w-4" />
          Start Experiment
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Training Progress</CardTitle>
            <CardDescription>Accuracy over training steps</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="step" className="text-xs" />
                <YAxis domain={[0.6, 1.0]} className="text-xs" />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }} />
                <Line type="monotone" dataKey="accuracy" stroke="hsl(var(--primary))" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Loss Curve</CardTitle>
            <CardDescription>Training loss over steps</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="step" className="text-xs" />
                <YAxis className="text-xs" />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }} />
                <Line type="monotone" dataKey="loss" stroke="#ef4444" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Experiment Runs</CardTitle>
          <CardDescription>All runs in this experiment</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {runs.map((run) => (
              <div key={run.id} className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-accent transition-colors">
                <div className="flex items-center gap-4">
                  {run.status === 'completed' && <CheckCircle className="h-5 w-5 text-green-600" />}
                  {run.status === 'running' && <Play className="h-5 w-5 text-blue-600" />}
                  {run.status === 'failed' && <XCircle className="h-5 w-5 text-red-600" />}
                  <div>
                    <p className="font-medium">{run.name}</p>
                    <div className="flex items-center gap-3 text-sm text-muted-foreground">
                      <span>Accuracy: {run.accuracy}</span>
                      <span>Loss: {run.loss}</span>
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {run.duration}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm">View</Button>
                  <Button variant="outline" size="sm">Compare</Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
