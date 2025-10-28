# React.js Frontend Architecture with shadcn/ui

## Overview

This document outlines the comprehensive React.js frontend architecture using shadcn/ui components for the student academics management system. The design emphasizes modularity, performance, and exceptional user experience while supporting individual-focused learning interfaces.

## Technology Stack

### Core Technologies
- **Frontend Framework**: React 18+ with TypeScript
- **Build Tool**: Vite 5+
- **UI Library**: shadcn/ui (Radix UI + Tailwind CSS)
- **State Management**: Zustand for global state, React Query for server state
- **Routing**: React Router v6
- **Forms**: React Hook Form with Zod validation
- **Styling**: Tailwind CSS with custom design system
- **Icons**: Lucide React
- **Charts**: Recharts
- **Date Handling**: date-fns
- **Animations**: Framer Motion

### Supporting Technologies
- **Development**: ESLint, Prettier, Husky
- **Testing**: Vitest, React Testing Library
- **Type Safety**: TypeScript with strict mode
- **Performance**: React.memo, useMemo, useCallback optimizations
- **Accessibility**: React Aria, built-in shadcn/ui accessibility

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── table.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── form.tsx
│   │   │   ├── card.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── avatar.tsx
│   │   │   ├── dropdown-menu.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── select.tsx
│   │   │   ├── checkbox.tsx
│   │   │   ├── radio-group.tsx
│   │   │   ├── toast.tsx
│   │   │   └── index.ts
│   │   ├── layout/               # Layout components
│   │   │   ├── header.tsx
│   │   │   ├── sidebar.tsx
│   │   │   ├── footer.tsx
│   │   │   ├── navigation.tsx
│   │   │   └── main-layout.tsx
│   │   ├── auth/                 # Authentication components
│   │   │   ├── login-form.tsx
│   │   │   ├── register-form.tsx
│   │   │   ├── forgot-password.tsx
│   │   │   └── auth-guard.tsx
│   │   ├── student/              # Student components
│   │   │   ├── student-card.tsx
│   │   │   ├── student-profile.tsx
│   │   │   ├── progress-chart.tsx
│   │   │   ├── attendance-record.tsx
│   │   │   └── student-list.tsx
│   │   ├── faculty/              # Faculty components
│   │   │   ├── faculty-card.tsx
│   │   │   ├── faculty-schedule.tsx
│   │   │   ├── performance-dashboard.tsx
│   │   │   └── time-tracker.tsx
│   │   ├── attendance/           # Attendance components
│   │   │   ├── attendance-marking.tsx
│   │   │   ├── quick-attendance.tsx
│   │   │   ├── attendance-report.tsx
│   │   │   └── topic-selector.tsx
│   │   ├── crm/                  # CRM components
│   │   │   ├── inquiry-card.tsx
│   │   │   ├── follow-up-scheduler.tsx
│   │   │   ├── lead-scoring.tsx
│   │   │   └── conversion-funnel.tsx
│   │   ├── analytics/            # Analytics components
│   │   │   ├── progress-analytics.tsx
│   │   │   ├── performance-metrics.tsx
│   │   │   ├── trend-charts.tsx
│   │   │   └── predictive-analytics.tsx
│   │   ├── feedback/             # Feedback components
│   │   │   ├── feedback-form.tsx
│   │   │   ├── rating-component.tsx
│   │   │   ├── sentiment-analysis.tsx
│   │   │   └── feedback-dashboard.tsx
│   │   └── common/               # Common components
│   │       ├── data-table.tsx
│   │       ├── loading-spinner.tsx
│   │       ├── error-boundary.tsx
│   │       ├── search-bar.tsx
│   │       ├── filter-panel.tsx
│   │       ├── pagination.tsx
│   │       └── export-button.tsx
│   ├── pages/                   # Page components
│   │   ├── auth/
│   │   │   ├── login.tsx
│   │   │   ├── register.tsx
│   │   │   └── forgot-password.tsx
│   │   ├── dashboard/
│   │   │   ├── student-dashboard.tsx
│   │   │   ├── faculty-dashboard.tsx
│   │   │   ├── counselor-dashboard.tsx
│   │   │   └── admin-dashboard.tsx
│   │   ├── students/
│   │   │   ├── student-list.tsx
│   │   │   ├── student-details.tsx
│   │   │   ├── student-progress.tsx
│   │   │   └── create-student.tsx
│   │   ├── attendance/
│   │   │   ├── mark-attendance.tsx
│   │   │   ├── attendance-history.tsx
│   │   │   └── attendance-reports.tsx
│   │   ├── crm/
│   │   │   ├── inquiries.tsx
│   │   │   ├── follow-ups.tsx
│   │   │   ├── pipeline.tsx
│   │   │   └── analytics.tsx
│   │   ├── analytics/
│   │   │   ├── student-analytics.tsx
│   │   │   ├── faculty-analytics.tsx
│   │   │   ├── institute-analytics.tsx
│   │   │   └── reports.tsx
│   │   └── settings/
│   │       ├── profile.tsx
│   │       ├── preferences.tsx
│   │       └── system-settings.tsx
│   ├── hooks/                   # Custom hooks
│   │   ├── use-auth.ts
│   │   ├── use-api.ts
│   │   ├── use-local-storage.ts
│   │   ├── use-debounce.ts
│   │   ├── use-websocket.ts
│   │   ├── use-permissions.ts
│   │   └── use-offline.ts
│   ├── stores/                  # Zustand stores
│   │   ├── auth-store.ts
│   │   ├── ui-store.ts
│   │   ├── notification-store.ts
│   │   ├── attendance-store.ts
│   │   └── analytics-store.ts
│   ├── services/                # API services
│   │   ├── api.ts
│   │   ├── auth-service.ts
│   │   ├── student-service.ts
│   │   ├── faculty-service.ts
│   │   ├── attendance-service.ts
│   │   ├── crm-service.ts
│   │   ├── analytics-service.ts
│   │   └── websocket-service.ts
│   ├── types/                   # TypeScript types
│   │   ├── auth.ts
│   │   ├── student.ts
│   │   ├── faculty.ts
│   │   ├── attendance.ts
│   │   ├── crm.ts
│   │   ├── analytics.ts
│   │   └── api.ts
│   ├── utils/                   # Utility functions
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   ├── validators.ts
│   │   ├── formatters.ts
│   │   ├── permissions.ts
│   │   └── date-utils.ts
│   ├── styles/                  # Custom styles
│   │   ├── globals.css
│   │   ├── components.css
│   │   └── animations.css
│   ├── lib/                     # External library configurations
│   │   ├── utils.ts
│   │   ├── validations.ts
│   │   ├── api-client.ts
│   │   └── toast.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── components.json
└── .env.example
```

## Core Components

### 1. Attendance Marking Component

#### Quick Attendance Interface
```tsx
// components/attendance/quick-attendance.tsx
import React, { useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';
import { useAttendanceStore } from '@/stores/attendance-store';
import { Student, Topic } from '@/types';

interface QuickAttendanceProps {
  sessionId: number;
  students: Student[];
  availableTopics: Topic[];
}

export function QuickAttendance({ sessionId, students, availableTopics }: QuickAttendanceProps) {
  const [attendanceData, setAttendanceData] = useState<Record<number, {
    present: boolean;
    topics: number[];
    notes: string;
    understanding: number;
  }>>({});
  
  const [selectedTopics, setSelectedTopics] = useState<number[]>([]);
  const { markAttendance, isMarking } = useAttendanceStore();
  const { toast } = useToast();

  const handleAttendanceChange = useCallback((studentId: number, present: boolean) => {
    setAttendanceData(prev => ({
      ...prev,
      [studentId]: { ...prev[studentId], present }
    }));
  }, []);

  const handleTopicSelection = useCallback((studentId: number, topicId: number) => {
    setAttendanceData(prev => {
      const currentTopics = prev[studentId]?.topics || [];
      const newTopics = currentTopics.includes(topicId)
        ? currentTopics.filter(id => id !== topicId)
        : [...currentTopics, topicId];
      
      return {
        ...prev,
        [studentId]: { ...prev[studentId], topics: newTopics }
      };
    });
  }, []);

  const handleSubmit = async () => {
    try {
      await markAttendance(sessionId, attendanceData);
      toast({
        title: "Attendance marked successfully",
        description: `Marked attendance for ${Object.keys(attendanceData).length} students`,
      });
    } catch (error) {
      toast({
        title: "Error marking attendance",
        description: "Please try again later",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Mark Attendance - Session {sessionId}</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="individual" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="individual">Individual</TabsTrigger>
              <TabsTrigger value="bulk">Bulk Actions</TabsTrigger>
            </TabsList>
            
            <TabsContent value="individual" className="space-y-4">
              {students.map((student) => (
                <Card key={student.id} className="p-4">
                  <div className="flex items-center space-x-4">
                    <Avatar>
                      <AvatarImage src={student.avatar} />
                      <AvatarFallback>{student.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-medium">{student.name}</h3>
                          <p className="text-sm text-muted-foreground">{student.email}</p>
                        </div>
                        <Checkbox
                          checked={attendanceData[student.id]?.present || false}
                          onCheckedChange={(checked) => handleAttendanceChange(student.id, checked as boolean)}
                        />
                      </div>
                      
                      {attendanceData[student.id]?.present && (
                        <div className="mt-4 space-y-3">
                          <div>
                            <Label className="text-sm font-medium">Topics Covered</Label>
                            <div className="flex flex-wrap gap-2 mt-1">
                              {availableTopics.map((topic) => (
                                <Badge
                                  key={topic.id}
                                  variant={attendanceData[student.id]?.topics?.includes(topic.id) ? "default" : "outline"}
                                  className="cursor-pointer"
                                  onClick={() => handleTopicSelection(student.id, topic.id)}
                                >
                                  {topic.name}
                                </Badge>
                              ))}
                            </div>
                          </div>
                          
                          <div>
                            <Label className="text-sm font-medium">Understanding Level</Label>
                            <Select
                              value={attendanceData[student.id]?.understanding?.toString()}
                              onValueChange={(value) => setAttendanceData(prev => ({
                                ...prev,
                                [student.id]: { ...prev[student.id], understanding: parseInt(value) }
                              }))}
                            >
                              <SelectTrigger className="w-full">
                                <SelectValue placeholder="Select understanding level" />
                              </SelectTrigger>
                              <SelectContent>
                                <SelectItem value="1">1 - No Understanding</SelectItem>
                                <SelectItem value="2">2 - Basic Awareness</SelectItem>
                                <SelectItem value="3">3 - Partial Understanding</SelectItem>
                                <SelectItem value="4">4 - Good Understanding</SelectItem>
                                <SelectItem value="5">5 - Complete Mastery</SelectItem>
                              </SelectContent>
                            </Select>
                          </div>
                          
                          <div>
                            <Label className="text-sm font-medium">Notes</Label>
                            <Textarea
                              placeholder="Add notes about student's progress..."
                              value={attendanceData[student.id]?.notes || ''}
                              onChange={(e) => setAttendanceData(prev => ({
                                ...prev,
                                [student.id]: { ...prev[student.id], notes: e.target.value }
                              }))}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              ))}
            </TabsContent>
            
            <TabsContent value="bulk" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="p-4">
                  <h3 className="font-medium mb-3">Bulk Actions</h3>
                  <div className="space-y-2">
                    <Button
                      variant="outline"
                      className="w-full justify-start"
                      onClick={() => {
                        const allPresent = students.reduce((acc, student) => ({
                          ...acc,
                          [student.id]: { present: true, topics: [], notes: '', understanding: 3 }
                        }), {});
                        setAttendanceData(allPresent);
                      }}
                    >
                      Mark All Present
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full justify-start"
                      onClick={() => {
                        const allAbsent = students.reduce((acc, student) => ({
                          ...acc,
                          [student.id]: { present: false, topics: [], notes: '', understanding: 0 }
                        }), {});
                        setAttendanceData(allAbsent);
                      }}
                    >
                      Mark All Absent
                    </Button>
                  </div>
                </Card>
                
                <Card className="p-4">
                  <h3 className="font-medium mb-3">Common Topics</h3>
                  <div className="flex flex-wrap gap-2">
                    {availableTopics.map((topic) => (
                      <Badge
                        key={topic.id}
                        variant={selectedTopics.includes(topic.id) ? "default" : "outline"}
                        className="cursor-pointer"
                        onClick={() => {
                          const newSelected = selectedTopics.includes(topic.id)
                            ? selectedTopics.filter(id => id !== topic.id)
                            : [...selectedTopics, topic.id];
                          setSelectedTopics(newSelected);
                          
                          // Apply to all present students
                          setAttendanceData(prev => {
                            const updated = { ...prev };
                            students.forEach(student => {
                              if (updated[student.id]?.present) {
                                updated[student.id] = {
                                  ...updated[student.id],
                                  topics: newSelected
                                };
                              }
                            });
                            return updated;
                          });
                        }}
                      >
                        {topic.name}
                      </Badge>
                    ))}
                  </div>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
          
          <div className="flex justify-end space-x-2 mt-6">
            <Button variant="outline">Save as Draft</Button>
            <Button onClick={handleSubmit} disabled={isMarking}>
              {isMarking ? "Marking..." : "Submit Attendance"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

### 2. Student Progress Dashboard

#### Progress Analytics Component
```tsx
// components/student/progress-chart.tsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { StudentProgress, SubjectProgress } from '@/types';

interface ProgressChartProps {
  studentId: number;
  progressData: StudentProgress;
}

export function ProgressChart({ studentId, progressData }: ProgressChartProps) {
  const velocityData = progressData.learningVelocity.map(item => ({
    week: item.week,
    topics: item.topicsCompleted,
    target: 2, // Target: 2 topics per week
  }));

  const competencyData = progressData.subjects.map(subject => ({
    subject: subject.name,
    competency: subject.competencyLevel,
    completion: subject.completionPercentage,
  }));

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Overall Progress</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progressData.overallProgress}%</div>
            <Progress value={progressData.overallProgress} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-2">
              {progressData.status === 'on_track' ? 'On Track' : 'Behind Schedule'}
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Learning Velocity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progressData.currentVelocity}</div>
            <p className="text-xs text-muted-foreground mt-2">
              topics per week
            </p>
            <Badge variant={progressData.velocityTrend === 'increasing' ? 'default' : 'secondary'}>
              {progressData.velocityTrend === 'increasing' ? '↗ Improving' : '→ Stable'}
            </Badge>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Time to Completion</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progressData.estimatedWeeksRemaining}</div>
            <p className="text-xs text-muted-foreground mt-2">
              weeks remaining
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="velocity" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="velocity">Learning Velocity</TabsTrigger>
          <TabsTrigger value="subjects">Subject Progress</TabsTrigger>
          <TabsTrigger value="topics">Topic Details</TabsTrigger>
        </TabsList>
        
        <TabsContent value="velocity">
          <Card>
            <CardHeader>
              <CardTitle>Learning Velocity Trends</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={velocityData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="topics" stroke="#8884d8" strokeWidth={2} />
                  <Line type="monotone" dataKey="target" stroke="#82ca9d" strokeDasharray="5 5" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="subjects">
          <Card>
            <CardHeader>
              <CardTitle>Subject-wise Progress</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={competencyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="subject" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="competency" fill="#8884d8" />
                  <Bar dataKey="completion" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="topics">
          <div className="space-y-4">
            {progressData.subjects.map((subject) => (
              <Card key={subject.id}>
                <CardHeader>
                  <CardTitle className="text-lg">{subject.name}</CardTitle>
                  <div className="flex items-center space-x-2">
                    <Progress value={subject.completionPercentage} className="flex-1" />
                    <span className="text-sm font-medium">{subject.completionPercentage}%</span>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {subject.topics.map((topic) => (
                      <div key={topic.id} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <h4 className="font-medium text-sm">{topic.name}</h4>
                          <p className="text-xs text-muted-foreground">
                            {topic.status === 'completed' ? 'Completed' : 
                             topic.status === 'in_progress' ? 'In Progress' : 'Not Started'}
                          </p>
                        </div>
                        <Badge variant={
                          topic.competencyLevel >= 4 ? 'default' :
                          topic.competencyLevel >= 2 ? 'secondary' : 'destructive'
                        }>
                          {topic.competencyLevel}/5
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
```

### 3. CRM Pipeline Component

#### Lead Management Interface
```tsx
// components/crm/conversion-funnel.tsx
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Inquiry, FollowUp } from '@/types';
import { format } from 'date-fns';

interface ConversionFunnelProps {
  inquiries: Inquiry[];
  onInquiryUpdate: (inquiryId: number, updates: Partial<Inquiry>) => void;
}

export function ConversionFunnel({ inquiries, onInquiryUpdate }: ConversionFunnelProps) {
  const [selectedInquiry, setSelectedInquiry] = useState<Inquiry | null>(null);

  const pipelineStages = [
    { key: 'new', label: 'New', color: 'bg-blue-500' },
    { key: 'contacted', label: 'Contacted', color: 'bg-yellow-500' },
    { key: 'follow_up_scheduled', label: 'Follow-up', color: 'bg-orange-500' },
    { key: 'negotiation', label: 'Negotiation', color: 'bg-purple-500' },
    { key: 'enrolled', label: 'Enrolled', color: 'bg-green-500' },
    { key: 'lost', label: 'Lost', color: 'bg-red-500' },
  ];

  const getInquiriesByStage = (stage: string) => {
    return inquiries.filter(inquiry => inquiry.status === stage);
  };

  const getConversionRate = () => {
    const totalInquiries = inquiries.length;
    const enrolledCount = inquiries.filter(i => i.status === 'enrolled').length;
    return totalInquiries > 0 ? ((enrolledCount / totalInquiries) * 100).toFixed(1) : '0';
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        {pipelineStages.map((stage) => {
          const stageInquiries = getInquiriesByStage(stage.key);
          const stagePercentage = inquiries.length > 0 
            ? (stageInquiries.length / inquiries.length) * 100 
            : 0;

          return (
            <Card key={stage.key} className="relative">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium flex items-center justify-between">
                  {stage.label}
                  <Badge variant="secondary">{stageInquiries.length}</Badge>
                </CardTitle>
                <Progress value={stagePercentage} className="mt-2" />
              </CardHeader>
              <CardContent className="space-y-3">
                {stageInquiries.slice(0, 3).map((inquiry) => (
                  <Dialog key={inquiry.id}>
                    <DialogTrigger asChild>
                      <div 
                        className="flex items-center space-x-2 p-2 border rounded-lg cursor-pointer hover:bg-muted/50 transition-colors"
                        onClick={() => setSelectedInquiry(inquiry)}
                      >
                        <Avatar className="h-6 w-6">
                          <AvatarImage src={inquiry.avatar} />
                          <AvatarFallback className="text-xs">
                            {inquiry.studentName.split(' ').map(n => n[0]).join('')}
                          </AvatarFallback>
                        </Avatar>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium truncate">{inquiry.studentName}</p>
                          <p className="text-xs text-muted-foreground">
                            {inquiry.interestedSubjects.join(', ')}
                          </p>
                        </div>
                        <Badge variant="outline" className="text-xs">
                          {inquiry.leadScore}
                        </Badge>
                      </div>
                    </DialogTrigger>
                    <DialogContent className="max-w-2xl">
                      <DialogHeader>
                        <DialogTitle>{inquiry.studentName}</DialogTitle>
                      </DialogHeader>
                      <InquiryDetails 
                        inquiry={inquiry} 
                        onUpdate={onInquiryUpdate}
                      />
                    </DialogContent>
                  </Dialog>
                ))}
                
                {stageInquiries.length > 3 && (
                  <Button variant="ghost" size="sm" className="w-full">
                    +{stageInquiries.length - 3} more
                  </Button>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Conversion Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold">{getConversionRate()}%</div>
              <p className="text-sm text-muted-foreground">Overall Conversion Rate</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">
                {inquiries.filter(i => i.status === 'new').length}
              </div>
              <p className="text-sm text-muted-foreground">New Inquiries</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">
                {inquiries.filter(i => i.status === 'follow_up_scheduled').length}
              </div>
              <p className="text-sm text-muted-foreground">Follow-ups Pending</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">
                {inquiries.filter(i => i.status === 'enrolled').length}
              </div>
              <p className="text-sm text-muted-foreground">Enrolled This Month</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Inquiry Details Component
function InquiryDetails({ inquiry, onUpdate }: { 
  inquiry: Inquiry; 
  onUpdate: (id: number, updates: Partial<Inquiry>) => void;
}) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h4 className="font-medium">Contact Information</h4>
          <p className="text-sm text-muted-foreground">{inquiry.email}</p>
          <p className="text-sm text-muted-foreground">{inquiry.phone}</p>
        </div>
        <div>
          <h4 className="font-medium">Lead Details</h4>
          <p className="text-sm text-muted-foreground">Source: {inquiry.source}</p>
          <p className="text-sm text-muted-foreground">Lead Score: {inquiry.leadScore}/10</p>
        </div>
      </div>
      
      <div>
        <h4 className="font-medium mb-2">Interested Subjects</h4>
        <div className="flex flex-wrap gap-2">
          {inquiry.interestedSubjects.map((subject, index) => (
            <Badge key={index} variant="outline">{subject}</Badge>
          ))}
        </div>
      </div>
      
      <div>
        <h4 className="font-medium mb-2">Follow-up History</h4>
        <div className="space-y-2">
          {inquiry.followUps?.map((followUp) => (
            <div key={followUp.id} className="flex items-center justify-between p-3 border rounded-lg">
              <div>
                <p className="text-sm font-medium">{followUp.type}</p>
                <p className="text-xs text-muted-foreground">
                  {format(new Date(followUp.followUpDate), 'MMM dd, yyyy HH:mm')}
                </p>
              </div>
              <Badge variant={followUp.status === 'completed' ? 'default' : 'secondary'}>
                {followUp.status}
              </Badge>
            </div>
          ))}
        </div>
      </div>
      
      <div className="flex justify-end space-x-2">
        <Button variant="outline">Schedule Follow-up</Button>
        <Button>Convert to Enrollment</Button>
      </div>
    </div>
  );
}
```

## State Management

### Zustand Store for Attendance
```typescript
// stores/attendance-store.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { attendanceService } from '@/services/attendance-service';

interface AttendanceState {
  // State
  isMarking: boolean;
  currentSession: number | null;
  attendanceData: Record<number, any>;
  
  // Actions
  markAttendance: (sessionId: number, data: any) => Promise<void>;
  setCurrentSession: (sessionId: number) => void;
  updateAttendanceData: (studentId: number, data: any) => void;
  clearAttendanceData: () => void;
}

export const useAttendanceStore = create<AttendanceState>()(
  devtools(
    (set, get) => ({
      // Initial state
      isMarking: false,
      currentSession: null,
      attendanceData: {},
      
      // Actions
      markAttendance: async (sessionId, data) => {
        set({ isMarking: true });
        try {
          await attendanceService.markBulkAttendance(sessionId, data);
          set({ attendanceData: {}, currentSession: null });
        } catch (error) {
          console.error('Error marking attendance:', error);
          throw error;
        } finally {
          set({ isMarking: false });
        }
      },
      
      setCurrentSession: (sessionId) => {
        set({ currentSession: sessionId });
      },
      
      updateAttendanceData: (studentId, data) => {
        set((state) => ({
          attendanceData: {
            ...state.attendanceData,
            [studentId]: { ...state.attendanceData[studentId], ...data }
          }
        }));
      },
      
      clearAttendanceData: () => {
        set({ attendanceData: {}, currentSession: null });
      },
    }),
    {
      name: 'attendance-store',
    }
  )
);
```

## Custom Hooks

### API Hook with React Query
```typescript
// hooks/use-api.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { authService } from '@/services/auth-service';
import { studentService } from '@/services/student-service';
import { facultyService } from '@/services/faculty-service';

export const useAuth = () => {
  return useQuery({
    queryKey: ['auth', 'user'],
    queryFn: authService.getCurrentUser,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useStudents = (filters?: any) => {
  return useQuery({
    queryKey: ['students', filters],
    queryFn: () => studentService.getStudents(filters),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
};

export const useStudentProgress = (studentId: number) => {
  return useQuery({
    queryKey: ['student', studentId, 'progress'],
    queryFn: () => studentService.getStudentProgress(studentId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useMarkAttendance = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ sessionId, data }: { sessionId: number; data: any }) =>
      attendanceService.markAttendance(sessionId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['attendance'] });
      queryClient.invalidateQueries({ queryKey: ['student-progress'] });
    },
  });
};
```

## Responsive Design

### Mobile-First Approach
```typescript
// utils/responsive.ts
export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

export const useResponsive = () => {
  const [screenSize, setScreenSize] = useState(getCurrentScreenSize());
  
  useEffect(() => {
    const handleResize = () => {
      setScreenSize(getCurrentScreenSize());
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  return {
    isMobile: screenSize === 'sm' || screenSize === 'xs',
    isTablet: screenSize === 'md',
    isDesktop: screenSize === 'lg' || screenSize === 'xl' || screenSize === '2xl',
    screenSize,
  };
};
```

This React.js architecture with shadcn/ui provides a comprehensive, modern frontend solution that emphasizes user experience, performance, and maintainability while supporting all the complex requirements of the student academics management system.