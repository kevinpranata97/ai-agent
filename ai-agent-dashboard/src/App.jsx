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
  Server,
  Brain,
  TestTube,
  Upload,
  Download,
  FileText,
  Cpu,
  HardDrive
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
  
  // New state for LLM fine-tuning
  const [fineTuningJobs, setFineTuningJobs] = useState([])
  const [fineTunedModels, setFineTunedModels] = useState([])
  const [newFineTuningJob, setNewFineTuningJob] = useState({
    model: 'gpt-3.5-turbo',
    training_data: '',
    suffix: ''
  })
  
  // New state for application testing
  const [testSessions, setTestSessions] = useState([])
  const [projectPath, setProjectPath] = useState('')
  const [testResults, setTestResults] = useState(null)

  // Mock data for demonstration
  useEffect(() => {
    setTasks([
      {
        id: '1',
        description: 'Create a responsive landing page for a tech startup',
        type: 'website_creation',
        priority: 'high',
        status: 'completed',
        progress: 100,
        createdAt: '2024-12-25T10:00:00Z'
      },
      {
        id: '2',
        description: 'Build a REST API for user management',
        type: 'app_development',
        priority: 'medium',
        status: 'in_progress',
        progress: 65,
        createdAt: '2024-12-25T12:00:00Z'
      },
      {
        id: '3',
        description: 'Analyze website performance metrics',
        type: 'data_analysis',
        priority: 'low',
        status: 'planning',
        progress: 15,
        createdAt: '2024-12-25T13:00:00Z'
      }
    ])

    setSystemStats({
      totalTasks: 3,
      completedTasks: 1,
      activeTasks: 1,
      failedTasks: 0
    })
    
    // Mock fine-tuning data
    setFineTuningJobs([
      {
        id: 'ftjob-123',
        model: 'gpt-3.5-turbo',
        status: 'succeeded',
        created_at: '2024-12-25T09:00:00Z',
        fine_tuned_model: 'ft:gpt-3.5-turbo:custom:model-123'
      },
      {
        id: 'ftjob-124',
        model: 'gpt-3.5-turbo',
        status: 'running',
        created_at: '2024-12-25T14:00:00Z',
        fine_tuned_model: null
      }
    ])
    
    setFineTunedModels([
      {
        id: 'ft:gpt-3.5-turbo:custom:model-123',
        created: 1703505600,
        owned_by: 'user'
      }
    ])
    
    // Mock test sessions
    setTestSessions([
      {
        id: 'test_1703505600',
        project_path: '/projects/landing-page',
        overall_success: true,
        timestamp: '2024-12-25T15:00:00Z'
      }
    ])
  }, [])

  const handleCreateTask = () => {
    if (!newTask.description.trim()) return

    const task = {
      id: Date.now().toString(),
      ...newTask,
      status: 'created',
      progress: 0,
      createdAt: new Date().toISOString()
    }

    setTasks(prev => [task, ...prev])
    setNewTask({ description: '', type: 'general', priority: 'medium' })
  }
  
  const handleCreateFineTuningJob = () => {
    if (!newFineTuningJob.training_data.trim()) return

    const job = {
      id: `ftjob-${Date.now()}`,
      ...newFineTuningJob,
      status: 'pending',
      created_at: new Date().toISOString(),
      fine_tuned_model: null
    }

    setFineTuningJobs(prev => [job, ...prev])
    setNewFineTuningJob({ model: 'gpt-3.5-turbo', training_data: '', suffix: '' })
  }
  
  const handleRunTests = () => {
    if (!projectPath.trim()) return

    const session = {
      id: `test_${Date.now()}`,
      project_path: projectPath,
      overall_success: Math.random() > 0.3, // Random success for demo
      timestamp: new Date().toISOString()
    }

    setTestSessions(prev => [session, ...prev])
    setProjectPath('')
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
      case 'succeeded':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'in_progress':
      case 'running':
        return <Clock className="h-4 w-4 text-blue-500" />
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'planning':
      case 'pending':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
      case 'succeeded':
        return 'bg-green-100 text-green-800'
      case 'in_progress':
      case 'running':
        return 'bg-blue-100 text-blue-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      case 'planning':
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'website_creation':
        return <Globe className="h-4 w-4" />
      case 'app_development':
        return <Code className="h-4 w-4" />
      case 'data_analysis':
        return <BarChart3 className="h-4 w-4" />
      case 'llm_finetuning':
        return <Brain className="h-4 w-4" />
      case 'app_testing':
        return <TestTube className="h-4 w-4" />
      default:
        return <Terminal className="h-4 w-4" />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Bot className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">AI Agent Dashboard</h1>
              <p className="text-sm text-gray-500">Intelligent Task Management & Automation</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <div className="h-2 w-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600 capitalize">{agentStatus}</span>
            </div>
            <Button variant="outline" size="sm">
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </Button>
          </div>
        </div>
      </header>

      {/* Stats Cards */}
      <div className="px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Tasks</p>
                  <p className="text-3xl font-bold text-blue-600">{systemStats.totalTasks}</p>
                </div>
                <BarChart3 className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Completed</p>
                  <p className="text-3xl font-bold text-green-600">{systemStats.completedTasks}</p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active</p>
                  <p className="text-3xl font-bold text-orange-600">{systemStats.activeTasks}</p>
                </div>
                <Zap className="h-8 w-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Success Rate</p>
                  <p className="text-3xl font-bold text-purple-600">
                    {systemStats.totalTasks > 0 ? Math.round((systemStats.completedTasks / systemStats.totalTasks) * 100) : 0}%
                  </p>
                </div>
                <Activity className="h-8 w-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="tasks" className="space-y-6">
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="tasks" className="flex items-center space-x-2">
              <Terminal className="h-4 w-4" />
              <span>Tasks</span>
            </TabsTrigger>
            <TabsTrigger value="create" className="flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Create</span>
            </TabsTrigger>
            <TabsTrigger value="monitor" className="flex items-center space-x-2">
              <Monitor className="h-4 w-4" />
              <span>Monitor</span>
            </TabsTrigger>
            <TabsTrigger value="finetuning" className="flex items-center space-x-2">
              <Brain className="h-4 w-4" />
              <span>Fine-tuning</span>
            </TabsTrigger>
            <TabsTrigger value="testing" className="flex items-center space-x-2">
              <TestTube className="h-4 w-4" />
              <span>Testing</span>
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
                <CardDescription>Monitor and manage all AI agent tasks</CardDescription>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96">
                  <div className="space-y-4">
                    {tasks.map((task) => (
                      <div key={task.id} className="border rounded-lg p-4 space-y-3">
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-3">
                            {getStatusIcon(task.status)}
                            <div className="flex-1">
                              <h3 className="font-medium text-gray-900">{task.description}</h3>
                              <div className="flex items-center space-x-2 mt-1">
                                <Badge variant="secondary" className={getStatusColor(task.status)}>
                                  {task.status}
                                </Badge>
                                <Badge variant="outline" className={getPriorityColor(task.priority)}>
                                  {task.priority}
                                </Badge>
                                <Badge variant="outline" className="flex items-center space-x-1">
                                  {getTypeIcon(task.type)}
                                  <span>{task.type.replace('_', ' ')}</span>
                                </Badge>
                              </div>
                            </div>
                          </div>
                          <div className="flex space-x-2">
                            <Button variant="outline" size="sm">
                              <Play className="h-4 w-4" />
                            </Button>
                            <Button variant="outline" size="sm">
                              <FileText className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span>Progress</span>
                            <span>{task.progress}%</span>
                          </div>
                          <Progress value={task.progress} className="h-2" />
                        </div>
                        <p className="text-sm text-gray-500">
                          Created: {new Date(task.createdAt).toLocaleString()}
                        </p>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Create Tab */}
          <TabsContent value="create" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Plus className="h-5 w-5" />
                  <span>Create New Task</span>
                </CardTitle>
                <CardDescription>Define a new task for the AI agent to execute</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Task Description</label>
                  <Textarea
                    placeholder="Describe what you want the AI agent to do..."
                    value={newTask.description}
                    onChange={(e) => setNewTask(prev => ({ ...prev, description: e.target.value }))}
                    className="min-h-[100px]"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Task Type</label>
                    <Select value={newTask.type} onValueChange={(value) => setNewTask(prev => ({ ...prev, type: value }))}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="general">General</SelectItem>
                        <SelectItem value="website_creation">Website Creation</SelectItem>
                        <SelectItem value="app_development">App Development</SelectItem>
                        <SelectItem value="data_analysis">Data Analysis</SelectItem>
                        <SelectItem value="llm_finetuning">LLM Fine-tuning</SelectItem>
                        <SelectItem value="app_testing">App Testing</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Priority</label>
                    <Select value={newTask.priority} onValueChange={(value) => setNewTask(prev => ({ ...prev, priority: value }))}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="low">Low</SelectItem>
                        <SelectItem value="medium">Medium</SelectItem>
                        <SelectItem value="high">High</SelectItem>
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

          {/* Monitor Tab */}
          <TabsContent value="monitor" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Activity className="h-5 w-5" />
                    <span>System Health</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>CPU Usage</span>
                      <span>23%</span>
                    </div>
                    <Progress value={23} className="h-2" />
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Memory Usage</span>
                      <span>45%</span>
                    </div>
                    <Progress value={45} className="h-2" />
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Task Queue</span>
                      <span>2 pending</span>
                    </div>
                    <Progress value={20} className="h-2" />
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
                <CardContent className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Current Branch</span>
                    <span className="text-sm">main</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Last Commit</span>
                    <span className="text-sm">2 hours ago</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Repository Status</span>
                    <Badge className="bg-green-100 text-green-800">Clean</Badge>
                  </div>
                  <Button variant="outline" className="w-full">
                    <GitBranch className="h-4 w-4 mr-2" />
                    View Repository
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Fine-tuning Tab */}
          <TabsContent value="finetuning" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Plus className="h-5 w-5" />
                    <span>Create Fine-tuning Job</span>
                  </CardTitle>
                  <CardDescription>Train a custom LLM model with your data</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Base Model</label>
                    <Select value={newFineTuningJob.model} onValueChange={(value) => setNewFineTuningJob(prev => ({ ...prev, model: value }))}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                        <SelectItem value="gpt-4">GPT-4</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Training Data (JSONL)</label>
                    <Textarea
                      placeholder='{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}'
                      value={newFineTuningJob.training_data}
                      onChange={(e) => setNewFineTuningJob(prev => ({ ...prev, training_data: e.target.value }))}
                      className="min-h-[100px] font-mono text-sm"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Model Suffix (Optional)</label>
                    <Input
                      placeholder="custom-model"
                      value={newFineTuningJob.suffix}
                      onChange={(e) => setNewFineTuningJob(prev => ({ ...prev, suffix: e.target.value }))}
                    />
                  </div>
                  <Button onClick={handleCreateFineTuningJob} className="w-full">
                    <Upload className="h-4 w-4 mr-2" />
                    Start Fine-tuning
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Brain className="h-5 w-5" />
                    <span>Fine-tuning Jobs</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-64">
                    <div className="space-y-3">
                      {fineTuningJobs.map((job) => (
                        <div key={job.id} className="border rounded-lg p-3">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              {getStatusIcon(job.status)}
                              <span className="font-medium text-sm">{job.id}</span>
                            </div>
                            <Badge className={getStatusColor(job.status)}>
                              {job.status}
                            </Badge>
                          </div>
                          <div className="text-xs text-gray-500 space-y-1">
                            <div>Model: {job.model}</div>
                            <div>Created: {new Date(job.created_at).toLocaleString()}</div>
                            {job.fine_tuned_model && (
                              <div>Fine-tuned Model: {job.fine_tuned_model}</div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Download className="h-5 w-5" />
                  <span>Fine-tuned Models</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {fineTunedModels.map((model) => (
                    <div key={model.id} className="border rounded-lg p-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-sm">{model.id}</div>
                          <div className="text-xs text-gray-500">
                            Created: {new Date(model.created * 1000).toLocaleString()}
                          </div>
                        </div>
                        <div className="flex space-x-2">
                          <Button variant="outline" size="sm">
                            <Play className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <TestTube className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Testing Tab */}
          <TabsContent value="testing" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <TestTube className="h-5 w-5" />
                    <span>Run Application Tests</span>
                  </CardTitle>
                  <CardDescription>Test generated applications for quality and functionality</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Project Path</label>
                    <Input
                      placeholder="/path/to/your/project"
                      value={projectPath}
                      onChange={(e) => setProjectPath(e.target.value)}
                    />
                  </div>
                  <Button onClick={handleRunTests} className="w-full">
                    <Play className="h-4 w-4 mr-2" />
                    Run Comprehensive Tests
                  </Button>
                  <div className="text-xs text-gray-500">
                    Tests include: Unit tests, Integration tests, Performance tests, Security checks
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <FileText className="h-5 w-5" />
                    <span>Test Sessions</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-64">
                    <div className="space-y-3">
                      {testSessions.map((session) => (
                        <div key={session.id} className="border rounded-lg p-3">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              {session.overall_success ? 
                                <CheckCircle className="h-4 w-4 text-green-500" /> : 
                                <XCircle className="h-4 w-4 text-red-500" />
                              }
                              <span className="font-medium text-sm">{session.id}</span>
                            </div>
                            <Badge className={session.overall_success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                              {session.overall_success ? 'PASS' : 'FAIL'}
                            </Badge>
                          </div>
                          <div className="text-xs text-gray-500 space-y-1">
                            <div>Project: {session.project_path}</div>
                            <div>Run: {new Date(session.timestamp).toLocaleString()}</div>
                          </div>
                          <div className="flex space-x-2 mt-2">
                            <Button variant="outline" size="sm">
                              <FileText className="h-4 w-4 mr-1" />
                              Report
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5" />
                  <span>Testing Capabilities</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center p-4 border rounded-lg">
                    <TestTube className="h-8 w-8 mx-auto mb-2 text-blue-600" />
                    <h3 className="font-medium">Unit Testing</h3>
                    <p className="text-sm text-gray-500">Individual component validation</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <Zap className="h-8 w-8 mx-auto mb-2 text-orange-600" />
                    <h3 className="font-medium">Integration Testing</h3>
                    <p className="text-sm text-gray-500">Component interaction validation</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <Activity className="h-8 w-8 mx-auto mb-2 text-green-600" />
                    <h3 className="font-medium">Performance Testing</h3>
                    <p className="text-sm text-gray-500">Load and stress testing</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* System Tab */}
          <TabsContent value="system" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Server className="h-5 w-5" />
                    <span>System Information</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Version</span>
                    <span className="text-sm">2.0.0</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Uptime</span>
                    <span className="text-sm">2h 34m</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Environment</span>
                    <span className="text-sm">Development</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Python Version</span>
                    <span className="text-sm">3.11.0</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">Node.js Version</span>
                    <span className="text-sm">20.18.0</span>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Cpu className="h-5 w-5" />
                    <span>Resource Usage</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>CPU Cores</span>
                      <span>4 cores</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Memory</span>
                      <span>8 GB</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Disk Space</span>
                      <span>256 GB SSD</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="h-5 w-5" />
                  <span>AI Capabilities</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div className="text-center p-4 border rounded-lg">
                    <Globe className="h-8 w-8 mx-auto mb-2 text-blue-600" />
                    <h3 className="font-medium">Website Creation</h3>
                    <p className="text-sm text-gray-500">React, HTML/CSS/JS, Static Sites</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <Code className="h-8 w-8 mx-auto mb-2 text-green-600" />
                    <h3 className="font-medium">App Development</h3>
                    <p className="text-sm text-gray-500">Flask, FastAPI, Node.js</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <BarChart3 className="h-8 w-8 mx-auto mb-2 text-purple-600" />
                    <h3 className="font-medium">Data Analysis</h3>
                    <p className="text-sm text-gray-500">Python, Pandas, Plotly</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <Brain className="h-8 w-8 mx-auto mb-2 text-orange-600" />
                    <h3 className="font-medium">LLM Fine-tuning</h3>
                    <p className="text-sm text-gray-500">OpenAI GPT models</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <TestTube className="h-8 w-8 mx-auto mb-2 text-red-600" />
                    <h3 className="font-medium">App Testing</h3>
                    <p className="text-sm text-gray-500">Automated testing suites</p>
                  </div>
                  <div className="text-center p-4 border rounded-lg">
                    <GitBranch className="h-8 w-8 mx-auto mb-2 text-gray-600" />
                    <h3 className="font-medium">Version Control</h3>
                    <p className="text-sm text-gray-500">Git integration</p>
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

