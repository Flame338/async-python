"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Progress } from "@/components/ui/progress"
import { FileText, Clock, HardDrive, CheckCircle, XCircle, Play, RefreshCw } from "lucide-react"

interface FileResult {
  filename: string
  size: number
  read_time: number
  content_preview: string
  error?: string
}

interface ResultsSummary {
  total_files: number
  successful_reads: number
  failed_reads: number
  total_size_bytes: number
  total_size_mb: number
  average_read_time: number
  file_extensions: string[]
}

export default function AsyncFileReaderDashboard() {
  const [isRunning, setIsRunning] = useState(false)
  const [summary, setSummary] = useState<ResultsSummary | null>(null)
  const [recentResults, setRecentResults] = useState<FileResult[]>([])
  const [progress, setProgress] = useState(0)

  // Simulate the async file reading process
  const simulateFileReading = async () => {
    setIsRunning(true)
    setProgress(0)

    // Simulate progress updates
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval)
          return 100
        }
        return prev + Math.random() * 10
      })
    }, 200)

    // Simulate completion after 3 seconds
    setTimeout(() => {
      clearInterval(progressInterval)
      setProgress(100)
      setIsRunning(false)

      // Mock results
      const mockSummary: ResultsSummary = {
        total_files: 100,
        successful_reads: 95,
        failed_reads: 5,
        total_size_bytes: 2048576,
        total_size_mb: 2.05,
        average_read_time: 0.045,
        file_extensions: [".txt", ".py", ".js", ".html", ".json"],
      }

      const mockResults: FileResult[] = Array.from({ length: 10 }, (_, i) => ({
        filename: `sample_files/sample_${String(i).padStart(3, "0")}.txt`,
        size: Math.floor(Math.random() * 5000) + 500,
        read_time: Math.random() * 0.1 + 0.02,
        content_preview: `Sample File ${i}\nThis is a test file created for demonstration purposes.\nFile number: ${i}\nContent length: ${"x".repeat(i * 2)}\nRandom data: ${Math.random().toString(36).substring(7)}`,
        error: Math.random() > 0.9 ? "Permission denied" : undefined,
      }))

      setSummary(mockSummary)
      setRecentResults(mockResults)
    }, 3000)
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-slate-900">Async File Reader</h1>
          <p className="text-slate-600 text-lg">Concurrent file processing with real-time results</p>
        </div>

        {/* Control Panel */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Play className="h-5 w-5" />
              Control Panel
            </CardTitle>
            <CardDescription>
              Start the async file reading process to read thousands of files concurrently
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-4">
              <Button onClick={simulateFileReading} disabled={isRunning} className="flex items-center gap-2">
                {isRunning ? (
                  <>
                    <RefreshCw className="h-4 w-4 animate-spin" />
                    Processing Files...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    Start File Reading
                  </>
                )}
              </Button>
            </div>

            {isRunning && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-slate-600">
                  <span>Reading files...</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="w-full" />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Results Dashboard */}
        {summary && (
          <Tabs defaultValue="summary" className="space-y-4">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="summary">Summary</TabsTrigger>
              <TabsTrigger value="files">File Results</TabsTrigger>
            </TabsList>

            <TabsContent value="summary" className="space-y-4">
              {/* Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-600">Total Files</p>
                        <p className="text-2xl font-bold text-slate-900">{summary.total_files}</p>
                      </div>
                      <FileText className="h-8 w-8 text-blue-500" />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-600">Success Rate</p>
                        <p className="text-2xl font-bold text-green-600">
                          {Math.round((summary.successful_reads / summary.total_files) * 100)}%
                        </p>
                      </div>
                      <CheckCircle className="h-8 w-8 text-green-500" />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-600">Total Size</p>
                        <p className="text-2xl font-bold text-slate-900">{summary.total_size_mb} MB</p>
                      </div>
                      <HardDrive className="h-8 w-8 text-purple-500" />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-600">Avg Time</p>
                        <p className="text-2xl font-bold text-slate-900">{summary.average_read_time}s</p>
                      </div>
                      <Clock className="h-8 w-8 text-orange-500" />
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* File Extensions */}
              <Card>
                <CardHeader>
                  <CardTitle>File Types Processed</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {summary.file_extensions.map((ext) => (
                      <Badge key={ext} variant="secondary">
                        {ext}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="files">
              <Card>
                <CardHeader>
                  <CardTitle>Recent File Results (Stack View)</CardTitle>
                  <CardDescription>
                    Most recently processed files - showing last 10 results from the stack
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-96">
                    <div className="space-y-3">
                      {recentResults.map((result, index) => (
                        <div
                          key={index}
                          className="border rounded-lg p-4 space-y-2 hover:bg-slate-50 transition-colors"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              {result.error ? (
                                <XCircle className="h-4 w-4 text-red-500" />
                              ) : (
                                <CheckCircle className="h-4 w-4 text-green-500" />
                              )}
                              <span className="font-medium text-sm">{result.filename.split("/").pop()}</span>
                            </div>
                            <div className="flex items-center gap-4 text-xs text-slate-500">
                              <span>{formatFileSize(result.size)}</span>
                              <span>{result.read_time.toFixed(3)}s</span>
                            </div>
                          </div>

                          {result.error ? (
                            <p className="text-sm text-red-600 bg-red-50 p-2 rounded">Error: {result.error}</p>
                          ) : (
                            <div className="text-xs text-slate-600 bg-slate-50 p-2 rounded font-mono">
                              {result.content_preview.substring(0, 150)}
                              {result.content_preview.length > 150 && "..."}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        )}

        {/* Instructions */}
        <Card>
          <CardHeader>
            <CardTitle>How It Works</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-slate-600">
            <p>
              • The Python script uses <code className="bg-slate-100 px-1 rounded">asyncio</code> and{" "}
              <code className="bg-slate-100 px-1 rounded">aiofiles</code> for concurrent file reading
            </p>
            <p>• A semaphore limits concurrent operations to prevent overwhelming the system</p>
            <p>• Results are stored in a deque (double-ended queue) acting as our stack/bucket</p>
            <p>• The web interface provides real-time visualization of the processing results</p>
            <p>• Run the Python script in the Scripts tab to see the actual async file processing</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
