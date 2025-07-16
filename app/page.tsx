"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Progress } from "@/components/ui/progress"
import { Globe, Clock, HardDrive, CheckCircle, XCircle, Play, RefreshCw } from "lucide-react"

interface UrlResult {
  url: string
  status_code: number
  response_size: number
  fetch_time: number
  content_preview: string
  error?: string
}

interface FetchSummary {
  total_requests: number
  successful_fetches: number
  failed_fetches: number
  total_response_size_bytes: number
  total_response_size_mb: number
  average_fetch_time: number
  status_codes: number[]
}

export default function ConcurrentUrlFetcherDashboard() {
  const [isRunning, setIsRunning] = useState(false)
  const [summary, setSummary] = useState<FetchSummary | null>(null)
  const [recentResults, setRecentResults] = useState<UrlResult[]>([])
  const [progress, setProgress] = useState(0)

  // Simulate the async URL fetching process
  const simulateUrlFetching = async () => {
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
      const mockSummary: FetchSummary = {
        total_requests: 100,
        successful_fetches: 95,
        failed_fetches: 5,
        total_response_size_bytes: 5120000, // 5MB
        total_response_size_mb: 5.12,
        average_fetch_time: 0.125,
        status_codes: [200, 200, 404, 200, 500, 200, 200, 301, 200, 200],
      }

      const mockResults: UrlResult[] = Array.from({ length: 10 }, (_, i) => {
        const isError = Math.random() > 0.9
        const statusCode = isError ? (Math.random() > 0.5 ? 404 : 500) : 200
        const responseSize = Math.floor(Math.random() * 10000) + 1000 // 1KB to 11KB
        return {
          url: `https://example.com/page/${String(i).padStart(3, "0")}`,
          status_code: statusCode,
          response_size: responseSize,
          fetch_time: Math.random() * 0.2 + 0.05,
          content_preview: `<!DOCTYPE html><html><head><title>Page ${i}</title></head><body><h1>Welcome to Page ${i}</h1><p>This is a simulated response for URL ${i}.</p></body></html>`,
          error: isError ? (statusCode === 404 ? "Not Found" : "Internal Server Error") : undefined,
        }
      })

      setSummary(mockSummary)
      setRecentResults(mockResults)
    }, 3000)
  }

  const formatResponseSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-slate-900">Concurrent URL Fetcher</h1>
          <p className="text-slate-600 text-lg">High-performance web scraping with real-time results</p>
        </div>

        {/* Control Panel */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Play className="h-5 w-5" />
              Control Panel
            </CardTitle>
            <CardDescription>Start the concurrent URL fetching process to hit thousands of URLs</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-4">
              <Button onClick={simulateUrlFetching} disabled={isRunning} className="flex items-center gap-2">
                {isRunning ? (
                  <>
                    <RefreshCw className="h-4 w-4 animate-spin" />
                    Fetching URLs...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    Start URL Fetching
                  </>
                )}
              </Button>
            </div>

            {isRunning && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-slate-600">
                  <span>Fetching URLs...</span>
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
              <TabsTrigger value="requests">Request Results</TabsTrigger>
            </TabsList>

            <TabsContent value="summary" className="space-y-4">
              {/* Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-600">Total Requests</p>
                        <p className="text-2xl font-bold text-slate-900">{summary.total_requests}</p>
                      </div>
                      <Globe className="h-8 w-8 text-blue-500" />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-600">Success Rate</p>
                        <p className="text-2xl font-bold text-green-600">
                          {Math.round((summary.successful_fetches / summary.total_requests) * 100)}%
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
                        <p className="text-sm font-medium text-slate-600">Total Response Size</p>
                        <p className="text-2xl font-bold text-slate-900">{summary.total_response_size_mb} MB</p>
                      </div>
                      <HardDrive className="h-8 w-8 text-purple-500" />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-600">Avg Fetch Time</p>
                        <p className="text-2xl font-bold text-slate-900">{summary.average_fetch_time}s</p>
                      </div>
                      <Clock className="h-8 w-8 text-orange-500" />
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Status Codes */}
              <Card>
                <CardHeader>
                  <CardTitle>HTTP Status Codes Processed</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {Array.from(new Set(summary.status_codes)).map((code) => (
                      <Badge key={code} variant="secondary">
                        {code}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="requests">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Request Results (Stack View)</CardTitle>
                  <CardDescription>Most recently fetched URLs - showing last 10 results from the stack</CardDescription>
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
                              <span className="font-medium text-sm">{result.url}</span>
                            </div>
                            <div className="flex items-center gap-4 text-xs text-slate-500">
                              <span>Status: {result.status_code}</span>
                              <span>Size: {formatResponseSize(result.response_size)}</span>
                              <span>Time: {result.fetch_time.toFixed(3)}s</span>
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
              <code className="bg-slate-100 px-1 rounded">aiohttp</code> for concurrent URL fetching
            </p>
            <p>• A semaphore limits concurrent requests to prevent overwhelming target servers</p>
            <p>• Results are stored in a deque (double-ended queue) acting as our stack/bucket</p>
            <p>• The web interface provides real-time visualization of the fetching results</p>
            <p>• Run the Python script in the Scripts tab to see the actual concurrent URL fetching</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
