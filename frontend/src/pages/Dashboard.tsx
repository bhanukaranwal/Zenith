import { useQuery } from '@tanstack/react-query'
import { projectsApi, experimentsApi, modelsApi, deploymentsApi } from '../lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'
import { FolderKanban, FlaskConical, Package, Rocket, TrendingUp, Activity } from 'lucide-react'

export default function Dashboard() {
  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => (await projectsApi.list()).data,
  })

  const { data: deployments } = useQuery({
    queryKey: ['deployments'],
    queryFn: async () => (await deploymentsApi.list()).data,
  })

  const stats = [
    { name: 'Projects', value: projects?.length || 0, icon: FolderKanban, color: 'text-blue-600' },
    { name: 'Experiments', value: 127, icon: FlaskConical, color: 'text-purple-600' },
    { name: 'Models', value: 43, icon: Package, color: 'text-green-600' },
    { name: 'Deployments', value: deployments?.length || 0, icon: Rocket, color: 'text-orange-600' },
  ]

  const experimentData = [
    { name: 'Mon', experiments: 12 },
    { name: 'Tue', experiments: 19 },
    { name: 'Wed', experiments: 15 },
    { name: 'Thu', experiments: 25 },
    { name: 'Fri', experiments: 22 },
    { name: 'Sat', experiments: 18 },
    { name: 'Sun', experiments: 20 },
  ]

  const performanceData = [
    { name: '00:00', accuracy: 0.92 },
    { name: '04:00', accuracy: 0.94 },
    { name: '08:00', accuracy: 0.93 },
    { name: '12:00', accuracy: 0.95 },
    { name: '16:00', accuracy: 0.96 },
    { name: '20:00', accuracy: 0.94 },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">Welcome to Zenith ML Platform</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                <TrendingUp className="inline h-3 w-3 mr-1" />
                +12% from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Experiment Activity</CardTitle>
            <CardDescription>Experiments run this week</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={experimentData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="name" className="text-xs" />
                <YAxis className="text-xs" />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }} />
                <Bar dataKey="experiments" fill="hsl(var(--primary))" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Model Performance</CardTitle>
            <CardDescription>Average accuracy over time</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="name" className="text-xs" />
                <YAxis domain={[0.9, 1.0]} className="text-xs" />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))' }} />
                <Line type="monotone" dataKey="accuracy" stroke="hsl(var(--primary))" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Latest platform events</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              { type: 'experiment', name: 'LLM Fine-tuning Run #42', time: '2 minutes ago', status: 'completed' },
              { type: 'deployment', name: 'Production Model v1.5', time: '15 minutes ago', status: 'running' },
              { type: 'model', name: 'ResNet-50 Checkpoint', time: '1 hour ago', status: 'saved' },
              { type: 'drift', name: 'Drift detected on user-behavior', time: '2 hours ago', status: 'alert' },
            ].map((activity, idx) => (
              <div key={idx} className="flex items-center gap-4 border-b border-border pb-3 last:border-0">
                <Activity className="h-5 w-5 text-muted-foreground" />
                <div className="flex-1">
                  <p className="text-sm font-medium">{activity.name}</p>
                  <p className="text-xs text-muted-foreground">{activity.time}</p>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${
                  activity.status === 'completed' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                  activity.status === 'running' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
                  activity.status === 'alert' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                  'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                }`}>
                  {activity.status}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
