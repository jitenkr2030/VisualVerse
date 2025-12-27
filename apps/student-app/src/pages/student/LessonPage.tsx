import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ChevronLeft,
  ChevronRight,
  Play,
  Pause,
  Volume2,
  VolumeX,
  Maximize,
  Check,
  SkipForward,
  SkipBack,
  BookOpen,
  MessageSquare,
  Download,
  Bookmark,
  MoreVertical,
} from 'lucide-react';
import { useProgressStore } from '../../store/progressStore';
import Card, { CardBody, CardHeader } from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import ProgressBar from '../../components/common/ProgressBar';

export default function LessonPage() {
  const { courseId, lessonId } = useParams();
  const { updateLessonProgress, markLessonComplete } = useProgressStore();
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [progress, setProgress] = useState(0);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleComplete = async () => {
    if (courseId && lessonId) {
      await markLessonComplete(lessonId, courseId);
    }
  };

  // Sample lesson data
  const lesson = {
    id: lessonId,
    title: 'Understanding Numbers',
    description: 'In this lesson, we explore the different types of numbers and their properties.',
    type: 'video',
    duration: 15,
    videoUrl: '/api/placeholder/1280/720',
    courseId: courseId,
    courseTitle: 'Mathematics Fundamentals',
    module: {
      id: 'm1',
      title: 'Numbers and Operations',
    },
    resources: [
      { name: 'Lesson Notes', type: 'pdf', size: '2.4 MB' },
      { name: 'Practice Problems', type: 'pdf', size: '1.1 MB' },
    ],
    nextLesson: {
      id: 'l6',
      title: 'Addition and Subtraction',
    },
    previousLesson: {
      id: 'l4',
      title: 'Course Overview',
    },
  };

  return (
    <div className={`min-h-screen bg-secondary-900 ${mounted ? 'animate-in' : ''}`}>
      {/* Video Player */}
      <div className="relative aspect-video bg-black">
        {/* Placeholder for video */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="w-20 h-20 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center hover:bg-white/30 transition-colors group mb-4"
            >
              {isPlaying ? (
                <Pause className="w-10 h-10 text-white" />
              ) : (
                <Play className="w-10 h-10 text-white ml-1" />
              )}
            </button>
            <p className="text-white/60 text-sm">
              {isPlaying ? 'Click to pause' : 'Click to play'}
            </p>
          </div>
        </div>

        {/* Video Controls */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
          {/* Progress Bar */}
          <div className="mb-4">
            <ProgressBar value={progress} variant="success" className="cursor-pointer" />
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="text-white hover:text-primary-400 transition-colors"
              >
                {isPlaying ? (
                  <Pause className="w-6 h-6" />
                ) : (
                  <Play className="w-6 h-6" />
                )}
              </button>
              <button className="text-white hover:text-primary-400 transition-colors">
                <SkipBack className="w-5 h-5" />
              </button>
              <button className="text-white hover:text-primary-400 transition-colors">
                <SkipForward className="w-5 h-5" />
              </button>
              <button
                onClick={() => setIsMuted(!isMuted)}
                className="text-white hover:text-primary-400 transition-colors"
              >
                {isMuted ? (
                  <VolumeX className="w-5 h-5" />
                ) : (
                  <Volume2 className="w-5 h-5" />
                )}
              </button>
              <span className="text-white text-sm">
                {Math.floor(progress * 15 / 100)}:00 / 15:00
              </span>
            </div>

            <div className="flex items-center gap-2">
              <button className="text-white hover:text-primary-400 transition-colors">
                <BookOpen className="w-5 h-5" />
              </button>
              <button className="text-white hover:text-primary-400 transition-colors">
                <Bookmark className="w-5 h-5" />
              </button>
              <button className="text-white hover:text-primary-400 transition-colors">
                <Download className="w-5 h-5" />
              </button>
              <button className="text-white hover:text-primary-400 transition-colors">
                <Maximize className="w-5 h-5" />
              </button>
              <button className="text-white hover:text-primary-400 transition-colors">
                <MoreVertical className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Lesson Content */}
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Navigation */}
            <div className="flex items-center justify-between">
              <Link
                to={`/courses/${courseId}`}
                className="flex items-center gap-2 text-white/70 hover:text-white transition-colors"
              >
                <ChevronLeft className="w-5 h-5" />
                <span>Back to Course</span>
              </Link>
              <div className="flex items-center gap-2">
                <span className="text-sm text-secondary-400">
                  {lesson.module.title}
                </span>
              </div>
            </div>

            {/* Lesson Header */}
            <div>
              <Badge variant="primary" className="mb-2">
                Lesson {lessonId?.slice(1)}
              </Badge>
              <h1 className="text-2xl font-bold text-white mb-2">{lesson.title}</h1>
              <p className="text-secondary-400">{lesson.description}</p>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-4">
              <Button
                variant="primary"
                onClick={handleComplete}
                leftIcon={<Check className="w-5 h-5" />}
              >
                Mark as Complete
              </Button>
              <Button variant="secondary" leftIcon={<MessageSquare className="w-5 h-5" />}>
                Discussion
              </Button>
            </div>

            {/* Resources */}
            <Card>
              <CardHeader>
                <h2 className="section-title text-white mb-0">Lesson Resources</h2>
              </CardHeader>
              <CardBody className="space-y-2">
                {lesson.resources.map((resource, index) => (
                  <a
                    key={index}
                    href="#"
                    className="flex items-center justify-between p-3 rounded-lg bg-secondary-800 hover:bg-secondary-700 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <Download className="w-5 h-5 text-primary-400" />
                      <span className="text-white">{resource.name}</span>
                      <Badge variant="secondary" size="sm">
                        {resource.type.toUpperCase()}
                      </Badge>
                    </div>
                    <span className="text-sm text-secondary-400">{resource.size}</span>
                  </a>
                ))}
              </CardBody>
            </Card>

            {/* Navigation Buttons */}
            <div className="flex items-center justify-between pt-4 border-t border-secondary-700">
              {lesson.previousLesson ? (
                <Link
                  to={`/courses/${courseId}/lesson/${lesson.previousLesson.id}`}
                  className="flex items-center gap-2 text-white/70 hover:text-white transition-colors"
                >
                  <ChevronLeft className="w-5 h-5" />
                  <div className="text-left">
                    <p className="text-xs text-secondary-400">Previous</p>
                    <p className="font-medium">{lesson.previousLesson.title}</p>
                  </div>
                </Link>
              ) : (
                <div />
              )}

              {lesson.nextLesson && (
                <Link
                  to={`/courses/${courseId}/lesson/${lesson.nextLesson.id}`}
                  className="flex items-center gap-2 text-white/70 hover:text-white transition-colors"
                >
                  <div className="text-right">
                    <p className="text-xs text-secondary-400">Next</p>
                    <p className="font-medium">{lesson.nextLesson.title}</p>
                  </div>
                  <ChevronRight className="w-5 h-5" />
                </Link>
              )}
            </div>
          </div>

          {/* Sidebar - Course Outline */}
          <div>
            <Card className="bg-secondary-800 border-secondary-700">
              <CardHeader className="border-secondary-700">
                <h2 className="section-title text-white mb-0">Course Content</h2>
              </CardHeader>
              <CardBody className="p-0">
                <div className="divide-y divide-secondary-700">
                  {['Welcome to the Course', 'What is Mathematics?', 'Setting Up Your Workspace', 'Course Overview', 'Understanding Numbers'].map((title, index) => (
                    <Link
                      key={index}
                      to={`/courses/${courseId}/lesson/l${index + 1}`}
                      className={`flex items-center gap-3 p-4 hover:bg-secondary-700 transition-colors ${
                        lessonId === `l${index + 1}` ? 'bg-secondary-700' : ''
                      }`}
                    >
                      <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                        index < 4
                          ? 'bg-green-500/20 text-green-400'
                          : lessonId === `l${index + 1}`
                          ? 'bg-primary-500 text-white'
                          : 'bg-secondary-600 text-secondary-400'
                      }`}>
                        {index < 4 ? (
                          <Check className="w-3 h-3" />
                        ) : (
                          index + 1
                        )}
                      </div>
                      <span className={`flex-1 text-sm ${
                        lessonId === `l${index + 1}` ? 'text-white' : 'text-secondary-300'
                      }`}>
                        {title}
                      </span>
                    </Link>
                  ))}
                </div>
              </CardBody>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
