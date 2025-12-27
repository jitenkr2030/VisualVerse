import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  Clock,
  Play,
  Filter,
  Grid,
  List,
  Calendar,
  TrendingUp,
  ChevronRight,
} from 'lucide-react';
import { useCourseStore } from '../../store/courseStore';
import Card, { CardBody, CardHeader } from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import ProgressBar from '../../components/common/ProgressBar';

type ViewMode = 'grid' | 'list';
type FilterType = 'all' | 'in-progress' | 'completed';

export default function MyLearningPage() {
  const { enrolledCourses, fetchEnrolledCourses, isLoading } = useCourseStore();
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [filter, setFilter] = useState<FilterType>('all');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    fetchEnrolledCourses();
  }, [fetchEnrolledCourses]);

  // Sample enrolled courses
  const sampleCourses = [
    {
      id: '1',
      title: 'Mathematics Fundamentals',
      instructor: 'Dr. Sarah Chen',
      progress: 65,
      lastAccessed: '2 hours ago',
      totalLessons: 48,
      completedLessons: 31,
      nextLesson: 'Calculus Basics',
      thumbnail: '/api/placeholder/400/225',
      category: 'Mathematics',
    },
    {
      id: '2',
      title: 'Physics: Classical Mechanics',
      instructor: 'Prof. James Wilson',
      progress: 40,
      lastAccessed: '1 day ago',
      totalLessons: 64,
      completedLessons: 26,
      nextLesson: 'Newton\'s Laws',
      thumbnail: '/api/placeholder/400/225',
      category: 'Physics',
    },
    {
      id: '3',
      title: 'Chemistry Essentials',
      instructor: 'Dr. Emily Roberts',
      progress: 85,
      lastAccessed: '3 days ago',
      totalLessons: 52,
      completedLessons: 44,
      nextLesson: 'Organic Compounds',
      thumbnail: '/api/placeholder/400/225',
      category: 'Chemistry',
    },
    {
      id: '4',
      title: 'Calculus Mastery',
      instructor: 'Dr. Michael Lee',
      progress: 100,
      lastAccessed: '1 week ago',
      totalLessons: 80,
      completedLessons: 80,
      nextLesson: null,
      thumbnail: '/api/placeholder/400/225',
      category: 'Mathematics',
    },
  ];

  const displayCourses = enrolledCourses.length > 0 ? enrolledCourses : sampleCourses;

  const filteredCourses = displayCourses.filter((course) => {
    if (filter === 'in-progress') return course.progress > 0 && course.progress < 100;
    if (filter === 'completed') return course.progress === 100;
    return true;
  });

  if (isLoading && enrolledCourses.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${mounted ? 'animate-in' : ''}`}>
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="page-title">My Learning</h1>
          <p className="page-subtitle">
            Track your progress and continue where you left off
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardBody className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-primary-100">
              <BookOpen className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-secondary-900">
                {displayCourses.length}
              </p>
              <p className="text-sm text-secondary-500">Enrolled Courses</p>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-amber-100">
              <Clock className="w-6 h-6 text-amber-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-secondary-900">
                {displayCourses.filter(c => c.progress > 0 && c.progress < 100).length}
              </p>
              <p className="text-sm text-secondary-500">In Progress</p>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-green-100">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-secondary-900">
                {displayCourses.filter(c => c.progress === 100).length}
              </p>
              <p className="text-sm text-secondary-500">Completed</p>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-purple-100">
              <Calendar className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-secondary-900">5</p>
              <p className="text-sm text-secondary-500">Learning Days</p>
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Filters and View Toggle */}
      <Card>
        <CardBody className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-secondary-400" />
            <div className="flex gap-2">
              {(['all', 'in-progress', 'completed'] as FilterType[]).map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    filter === f
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-secondary-600 hover:bg-secondary-100'
                  }`}
                >
                  {f === 'all' ? 'All Courses' : f === 'in-progress' ? 'In Progress' : 'Completed'}
                </button>
              ))}
            </div>
          </div>

          <div className="flex items-center gap-2 border border-secondary-200 rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg transition-colors ${
                viewMode === 'grid'
                  ? 'bg-primary-100 text-primary-600'
                  : 'text-secondary-500 hover:bg-secondary-100'
              }`}
            >
              <Grid className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-lg transition-colors ${
                viewMode === 'list'
                  ? 'bg-primary-100 text-primary-600'
                  : 'text-secondary-500 hover:bg-secondary-100'
              }`}
            >
              <List className="w-5 h-5" />
            </button>
          </div>
        </CardBody>
      </Card>

      {/* Course List */}
      {filteredCourses.length === 0 ? (
        <Card>
          <CardBody className="text-center py-12">
            <BookOpen className="w-16 h-16 mx-auto text-secondary-300 mb-4" />
            <h3 className="text-lg font-semibold text-secondary-900 mb-2">No courses found</h3>
            <p className="text-secondary-600 mb-4">
              {filter === 'all'
                ? "You haven't enrolled in any courses yet."
                : filter === 'in-progress'
                ? "You don't have any courses in progress."
                : "You haven't completed any courses yet."}
            </p>
            <Link to="/courses">
              <Button variant="primary">Browse Courses</Button>
            </Link>
          </CardBody>
        </Card>
      ) : (
        <div
          className={
            viewMode === 'grid'
              ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
              : 'space-y-4'
          }
        >
          {filteredCourses.map((course, index) => (
            <div
              key={course.id}
              className={mounted ? 'animate-in' : ''}
              style={{ animationDelay: `${index * 50}ms` }}
            >
              {viewMode === 'grid' ? (
                <Card hover className="h-full">
                  <div className="relative aspect-video bg-gradient-to-br from-primary-400 to-accent-500">
                    {course.progress === 100 && (
                      <div className="absolute top-3 right-3">
                        <Badge variant="success">Completed</Badge>
                      </div>
                    )}
                    <div className="absolute bottom-3 left-3">
                      <Badge variant="secondary">{course.category}</Badge>
                    </div>
                  </div>
                  <CardBody className="flex flex-col flex-1">
                    <h3 className="font-semibold text-secondary-900 mb-1 line-clamp-2">
                      {course.title}
                    </h3>
                    <p className="text-sm text-secondary-500 mb-4">
                      By {course.instructor}
                    </p>

                    <div className="mt-auto">
                      <div className="flex items-center justify-between text-sm mb-2">
                        <span className="text-secondary-600">
                          {course.completedLessons}/{course.totalLessons} lessons
                        </span>
                        <span className="font-medium text-secondary-900">{course.progress}%</span>
                      </div>
                      <ProgressBar value={course.progress} className="mb-4" />

                      {course.progress < 100 ? (
                        <>
                          <p className="text-sm text-secondary-600 mb-3">
                            Next: {course.nextLesson}
                          </p>
                          <Link to={`/courses/${course.id}/lesson/l1`}>
                            <Button variant="primary" size="sm" className="w-full" leftIcon={<Play className="w-4 h-4" />}>
                              Continue Learning
                            </Button>
                          </Link>
                        </>
                      ) : (
                        <Link to={`/courses/${course.id}`}>
                          <Button variant="secondary" size="sm" className="w-full">
                            Review Course
                          </Button>
                        </Link>
                      )}
                    </div>
                  </CardBody>
                </Card>
              ) : (
                <Card hover>
                  <CardBody>
                    <div className="flex gap-4">
                      <div className="w-32 h-20 rounded-lg bg-gradient-to-br from-primary-400 to-accent-500 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant="secondary">{course.category}</Badge>
                          {course.progress === 100 && <Badge variant="success">Completed</Badge>}
                        </div>
                        <h3 className="font-semibold text-secondary-900 mb-1">
                          {course.title}
                        </h3>
                        <p className="text-sm text-secondary-500 mb-2">By {course.instructor}</p>
                        <div className="flex items-center gap-4">
                          <ProgressBar value={course.progress} className="flex-1 max-w-xs" />
                          <span className="text-sm text-secondary-600">
                            {course.completedLessons}/{course.totalLessons} lessons
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center">
                        {course.progress < 100 ? (
                          <Link to={`/courses/${course.id}/lesson/l1`}>
                            <Button variant="primary" leftIcon={<Play className="w-4 h-4" />}>
                              Continue
                            </Button>
                          </Link>
                        ) : (
                          <Link to={`/courses/${course.id}`}>
                            <Button variant="secondary">
                              Review
                            </Button>
                          </Link>
                        )}
                      </div>
                    </div>
                  </CardBody>
                </Card>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
