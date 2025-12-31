import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Bot, Play, CheckCircle, Clock, XCircle } from 'lucide-react'

export default function Agents() {
  const [selectedAgent, setSelectedAgent] = useState<number | null>(null)

  const agents = [
    { id: 1, name: 'RAG Q&A Agent', type: 'rag', executions: 234, status: 'active' },
    { id: 2, name: 'Data Analysis Agent', type: 'tool', executions: 127, status: 'active' },
    { id: 3, name: 'Code Generator', type: 'llm', executions: 89, status: 'idle' },
  ]

  const executions = [
    { id: 1, input: 'What is the revenue trend?', status: 'completed', duration: '2.3s', timestamp: '2 mins ago' },
    { id: 2, input: 'Analyze customer churn', status: 'completed', duration: '3.1s', timestamp: '5 mins ago' },
    { id: 3, input: 'Generate quarterly report', status: 'running', duration: '-', timestamp: 'just now' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Agents</h1>
          <p className="text-muted-foreground">Build and orchestrate AI agents with RAG and tools</p>
        </div>
        <Button>
          <Bot className="mr-2 h-4 w-4" />
          Create Agent
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {agents.map((agent) => (
          <Card 
            key={agent.id} 
            className={`cursor-pointer hover:shadow-lg transition-all ${selectedAgent === agent.id ? 'ring-2 ring-primary' : ''}`}
            onClick={() => setSelectedAgent(agent.id)}
          >
            <CardHeader>
              <div className="flex items-center justify-between">
                <Bot className="h-8 w-8 text-primary" />
                <span className={`text-xs px-2 py-1 rounded-full ${
                  agent.status === 'active' 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                }`}>
                  {agent.status}
                </span>
              </div>
              <CardTitle className="mt-2">{agent.name}</CardTitle>
              <CardDescription className="capitalize">{agent.type} agent</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Executions</span>
                  <span className="font-medium">{agent.executions}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {selectedAgent && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Agent Playground</CardTitle>
              <CardDescription>Test your agent with custom inputs</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <Input placeholder="Enter your query or task..." className="flex-1" />
                <Button>
                  <Play className="mr-2 h-4 w-4" />
                  Execute
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Execution History</CardTitle>
              <CardDescription>Recent agent executions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {executions.map((execution) => (
                  <div key={execution.id} className="flex items-center justify-between p-3 border border-border rounded-lg">
                    <div className="flex items-center gap-3 flex-1">
                      {execution.status === 'completed' && <CheckCircle className="h-5 w-5 text-green-600" />}
                      {execution.status === 'running' && <Clock className="h-5 w-5 text-blue-600 animate-spin" />}
                      {execution.status === 'failed' && <XCircle className="h-5 w-5 text-red-600" />}
                      <div className="flex-1">
                        <p className="text-sm font-medium">{execution.input}</p>
                        <p className="text-xs text-muted-foreground">{execution.timestamp}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-sm text-muted-foreground">{execution.duration}</span>
                      <Button variant="ghost" size="sm">View</Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Agent Workflow</CardTitle>
              <CardDescription>Visual representation of agent steps</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-medium">1</div>
                  <div className="flex-1">
                    <p className="font-medium">Parse Input</p>
                    <p className="text-sm text-muted-foreground">Extract query and context</p>
                  </div>
                </div>
                <div className="ml-4 border-l-2 border-border pl-7 pb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-medium">2</div>
                    <div className="flex-1">
                      <p className="font-medium">Retrieve Context</p>
                      <p className="text-sm text-muted-foreground">Search vector database</p>
                    </div>
                  </div>
                </div>
                <div className="ml-4 border-l-2 border-border pl-7 pb-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-medium">3</div>
                    <div className="flex-1">
                      <p className="font-medium">Generate Response</p>
                      <p className="text-sm text-muted-foreground">Use LLM with context</p>
                    </div>
                  </div>
                </div>
                <div className="ml-4 pl-7">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-medium">4</div>
                    <div className="flex-1">
                      <p className="font-medium">Return Result</p>
                      <p className="text-sm text-muted-foreground">Format and validate output</p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}
