import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { 
  Activity, 
  Bot, 
  Code, 
  Database, 
  Globe, 
  Monitor, 
  Plus, 
  Play, 
  Pause, 
  Settings, 
  Terminal,
  CheckCircle,
  Clock,
  AlertCircle,
  XCircle,
  GitBranch,
  Zap,
  BarChart3,
  Users,
  Server
} from 'lucide-react'
import './App.css'

function App() {
  const [tasks, setTasks] = useState([])
  const [newTask, setNewTask] = useState({
    description: '',
    type: 'general',
    priority: 'medium'
  })
  const [agentStatus, setAgentStatus] = useState('running')
  const [systemStats, setSystemStats] = useState({
    totalTasks: 0,
    completedTasks: 0,
    activeTasks: 0,
    failedTasks: 0
  })

  // Mock data for demonstration
  useEffect(() => {
    const mockTasks = [
      {
        id: '1',
        description: 'Create a responsive landing page for a tech startup',
        type: 'website_creation',
        priority: 'high',
        status: 'completed',
        progress: 100,
        created_at: '2024-12-25T10:00:00Z',
        completed_at: '2024-12-25T11:30:00Z'
      },
      {
        id: '2',
        description: 'Build a REST API for user management',
        type: 'app_development',
        priority: 'medium',
        status: 'in_progress',
        progress: 65,
        created_at: '2024-12-25T12:00:00Z'
      },
      {
        id: '3',
        description: 'Analyze website performance metrics',
        type: 'data_analysis',
        priority: 'low',
        status: 'planning',
        progress: 10,
        created_at: '2024-12-25T13:00:00Z'
      }
    ]
    setTasks(mockTasks)
    setSystemStats({
      totalTasks: mockTasks.length,
      completedTasks: mockTasks.filter(t => t.status === 'completed').length,
      activeTasks: mockTasks.filter(t => t.status === 'in_progress').length,
      failedTasks: mockTasks.filter(t => t.status === 'failed').length
    })
  }, [])

  const handleCreateTask = () => {
    if (!newTask.description.trim()) return

    const task = {
      id: Date.now().toString(),
      ...newTask,
      status: 'created',
      progress: 0,
      created_at: new Date().toISOString()
    }

    setTasks(prev => [task, ...prev])
    setNewTask({ description: '', type: 'general', priority: 'medium' })
    setSystemStats(prev => ({ ...prev, totalTasks: prev.totalTasks + 1 }))
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'in_progress': return <Clock className="h-4 w-4 text-blue-500" />
      case 'failed': return <XCircle className="h-4 w-4 text-red-500" />
      case 'planning': return <AlertCircle className="h-4 w-4 text-yellow-500" />
      default: return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
      case 'in_progress': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
      case 'failed': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
      case 'planning': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm dark:bg-slate-900/80 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                <Bot className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI Agent Dashboard
                </h1>
                <p className="text-sm text-muted-foreground">
                  Intelligent Task Management & Automation
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Badge variant="outline" className="flex items-center space-x-1">
                <div className={`w-2 h-2 rounded-full ${agentStatus === 'running' ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="capitalize">{agentStatus}</span>
              </Badge>
              <Button variant="outline" size="sm">
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100 text-sm font-medium">Total Tasks</p>
                  <p className="text-3xl font-bold">{systemStats.totalTasks}</p>
                </div>
                <BarChart3 className="h-8 w-8 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100 text-sm font-medium">Completed</p>
                  <p className="text-3xl font-bold">{systemStats.completedTasks}</p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-yellow-500 to-yellow-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-yellow-100 text-sm font-medium">Active</p>
                  <p className="text-3xl font-bold">{systemStats.activeTasks}</p>
                </div>
                <Zap className="h-8 w-8 text-yellow-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100 text-sm font-medium">Success Rate</p>
                  <p className="text-3xl font-bold">
                    {systemStats.totalTasks > 0 ? Math.round((systemStats.completedTasks / systemStats.totalTasks) * 100) : 0}%
                  </p>
                </div>
                <Activity className="h-8 w-8 text-purple-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="tasks" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="tasks" className="flex items-center space-x-2">
              <Terminal className="h-4 w-4" />
              <span>Tasks</span>
            </TabsTrigger>
            <TabsTrigger value="create" className="flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Create</span>
            </TabsTrigger>
            <TabsTrigger value="monitoring" className="flex items-center space-x-2">
              <Monitor className="h-4 w-4" />
              <span>Monitor</span>
            </TabsTrigger>
            <TabsTrigger value="capabilities" className="flex items-center space-x-2">
              <Code className="h-4 w-4" />
              <span>Capabilities</span>
            </TabsTrigger>
            <TabsTrigger value="system" className="flex items-center space-x-2">
              <Server className="h-4 w-4" />
              <span>System</span>
            </TabsTrigger>
          </TabsList>

          {/* Tasks Tab */}
          <TabsContent value="tasks" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Terminal className="h-5 w-5" />
                  <span>Task Management</span>
                </CardTitle>
                <CardDescription>
                  Monitor and manage all AI agent tasks
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96">
                  <div className="space-y-4">
                    {tasks.map((task) => (
                      <Card key={task.id} className="p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-2">
                              {getStatusIcon(task.status)}
                              <h3 className="font-semibold">{task.description}</h3>
                            </div>
                            <div className="flex items-center space-x-4 mb-3">
                              <Badge className={getStatusColor(task.status)}>
                                {task.status.replace('_', ' ')}
                              </Badge>
                              <Badge className={getPriorityColor(task.priority)}>
                                {task.priority}
                              </Badge>
                              <Badge variant="outline">
                                {task.type.replace('_', ' ')}
                              </Badge>
                            </div>
                            <div className="space-y-2">
                              <div className="flex items-center justify-between text-sm">
                                <span>Progress</span>
                                <span>{task.progress}%</span>
                              </div>
                              <Progress value={task.progress} className="h-2" />
                            </div>
                            <p className="text-sm text-muted-foreground mt-2">
                              Created: {new Date(task.created_at).toLocaleString()}
                            </p>
                          </div>
                          <div className="flex space-x-2 ml-4">
                            <Button variant="outline" size="sm">
                              <Play className="h-4 w-4" />
                            </Button>
                            <Button variant="outline" size="sm">
                              <Pause className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      </Card>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Create Task Tab */}
          <TabsContent value="create" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Plus className="h-5 w-5" />
                  <span>Create New Task</span>
                </CardTitle>
                <CardDescription>
                  Define a new task for the AI agent to execute
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Task Description</label>
                  <Textarea
                    placeholder="Describe what you want the AI agent to do..."
                    value={newTask.description}
                    onChange={(e) => setNewTask(prev => ({ ...prev, description: e.target.value }))}
                    className="min-h-24"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Task Type</label>
                    <Select value={newTask.type} onValueChange={(value) => setNewTask(prev => ({ ...prev, type: value }))}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="website_creation">Website Creation</SelectItem>
                        <SelectItem value="app_development">App Development</SelectItem>
                        <SelectItem value="data_analysis">Data Analysis</SelectItem>
                        <SelectItem value="planning">Planning</SelectItem>
                        <SelectItem value="deployment">Deployment</SelectItem>
                        <SelectItem value="general">General</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Priority</label>
                    <Select value={newTask.priority} onValueChange={(value) => setNewTask(prev => ({ ...prev, priority: value }))}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="high">High</SelectItem>
                        <SelectItem value="medium">Medium</SelectItem>
                        <SelectItem value="low">Low</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <Button onClick={handleCreateTask} className="w-full">
                  <Plus className="h-4 w-4 mr-2" />
                  Create Task
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Monitoring Tab */}
          <TabsContent value="monitoring" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Activity className="h-5 w-5" />
                    <span>System Health</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>CPU Usage</span>
                      <span>23%</span>
                    </div>
                    <Progress value={23} />
                    <div className="flex items-center justify-between">
                      <span>Memory Usage</span>
                      <span>45%</span>
                    </div>
                    <Progress value={45} />
                    <div className="flex items-center justify-between">
                      <span>Task Queue</span>
                      <span>2 pending</span>
                    </div>
                    <Progress value={20} />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <GitBranch className="h-5 w-5" />
                    <span>Version Control</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span>Current Branch</span>
                      <Badge variant="outline">main</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Last Commit</span>
                      <span className="text-sm text-muted-foreground">2 hours ago</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Repository Status</span>
                      <Badge className="bg-green-100 text-green-800">Clean</Badge>
                    </div>
                    <Button variant="outline" className="w-full">
                      <GitBranch className="h-4 w-4 mr-2" />
                      View Repository
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Capabilities Tab */}
          <TabsContent value="capabilities" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Globe className="h-5 w-5" />
                    <span>Website Creation</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">
                    Create responsive websites using modern frameworks
                  </p>
                  <div className="space-y-2">
                    <Badge variant="outline">React</Badge>
                    <Badge variant="outline">HTML/CSS/JS</Badge>
                    <Badge variant="outline">Static Sites</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Code className="h-5 w-5" />
                    <span>App Development</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">
                    Develop web applications and APIs
                  </p>
                  <div className="space-y-2">
                    <Badge variant="outline">Flask</Badge>
                    <Badge variant="outline">FastAPI</Badge>
                    <Badge variant="outline">Node.js</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Database className="h-5 w-5" />
                    <span>Data Analysis</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-4">
                    Analyze data and generate insights
                  </p>
                  <div className="space-y-2">
                    <Badge variant="outline">Python</Badge>
                    <Badge variant="outline">Pandas</Badge>
                    <Badge variant="outline">Plotly</Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* System Tab */}
          <TabsContent value="system" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Server className="h-5 w-5" />
                  <span>System Information</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-3">
                    <h4 className="font-semibold">Agent Information</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Version</span>
                        <span>1.0.0</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Uptime</span>
                        <span>2h 34m</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Tasks Processed</span>
                        <span>127</span>
                      </div>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <h4 className="font-semibold">Environment</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Python Version</span>
                        <span>3.11.0</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Node.js Version</span>
                        <span>20.18.0</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Git Version</span>
                        <span>2.34.1</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

