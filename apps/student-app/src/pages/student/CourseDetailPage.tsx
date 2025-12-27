import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Play,
  Clock,
  BookOpen,
  Star,
  Users,
  Award,
  ChevronDown,
  ChevronRight,
  Check,
  Lock,
  Globe,
  Certificate,
} from 'lucide-react';
import { useCourseStore } from '../../store/courseStore';
import Card, { CardBody, CardHeader } from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import ProgressBar from '../../components/common/ProgressBar';
import LoadingSpinner from '../../components/common/LoadingSpinner';

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const { currentCourse, fetchCourseById, enrollInCourse, isEnrolled, isLoading } = useCourseStore();
  const [expandedModules, setExpandedModules] = useState<string[]>([]);
  const [isEnrolling, setIsEnrolling] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (courseId) {
      fetchCourseById(courseId);
    }
  }, [courseId, fetchCourseById]);

  const toggleModule = (moduleId: string) => {
    setExpandedModules((prev) =>
      prev.includes(moduleId)
        ? prev.filter((id) => id !== moduleId)
        : [...prev, moduleId]
    );
  };

  const handleEnroll = async () => {
    if (!courseId) return;
    setIsEnrolling(true);
    try {
      await enrollInCourse(courseId);
    } finally {
      setIsEnrolling(false);
    }
  };

  // Sample course data
  const sampleCourse = {
    id: courseId,
    title: 'Mathematics Fundamentals',
    description: 'Master the basics of algebra, calculus, and geometry with interactive visualizations. This comprehensive course covers everything from basic arithmetic to advanced calculus concepts, all explained through stunning animations and real-world examples.',
    instructor: {
      id: '1',
      name: 'Dr. Sarah Chen',
      avatar: '',
      bio: 'Professor of Mathematics with 15+ years of teaching experience. PhD from MIT.',
      coursesCount: 12,
      studentsCount: 45000,
      rating: 4.8,
    },
    category: 'Mathematics',
    difficulty: 'beginner' as const,
    duration: 1200,
    lessonsCount: 48,
    rating: 4.8,
    enrollmentsCount: 15420,
    price: 0,
    isEnrolled: false,
    features: [
      '48 interactive lessons with animations',
      'Hands-on practice problems',
      'Progress tracking and certificates',
      'Access on mobile and desktop',
      'Lifetime access',
    ],
    modules: [
      {
        id: 'm1',
        title: 'Getting Started with Mathematics',
        description: 'Introduction to basic mathematical concepts',
        lessons: [
          { id: 'l1', title: 'Welcome to the Course', duration: 5, type: 'video' },
          { id: 'l2', title: 'What is Mathematics?', duration: 10, type: 'video' },
          { id: 'l3', title: 'Setting Up Your Workspace', duration: 8, type: 'video' },
          { id: 'l4', title: 'Course Overview', duration: 12, type: 'video' },
        ],
        isLocked: false,
      },
      {
        id: 'm2',
        title: 'Numbers and Operations',
        description: 'Learn about different types of numbers and basic operations',
        lessons: [
          { id: 'l5', title: 'Understanding Numbers', duration: 15, type: 'video' },
          { id: 'l6', title: 'Addition and Subtraction', duration: 20, type: 'video' },
          { id: 'l7', title: 'Multiplication and Division', duration: 25, type: 'video' },
          { id: 'l8', title: 'Practice: Basic Operations', duration: 30, type: 'interactive' },
        ],
        isLocked: false,
      },
      {
        id: 'm3',
        title: 'Algebra Basics',
        description: 'Introduction to algebraic thinking and expressions',
        lessons: [
          { id: 'l9', title: 'Variables and Expressions', duration: 18, type: 'video' },
          { id: 'l10', title: 'Solving Simple Equations', duration: 22, type: 'video' },
          { id: 'l11', title: 'Linear Equations', duration: 25, type: 'video' },
          { id: 'l12', title: 'Quiz: Algebra Basics', duration: 15, type: 'quiz' },
        ],
        isLocked: true,
      },
      {
        id: 'm4',
        title: 'Geometry Fundamentals',
        description: 'Explore shapes, sizes, and spatial relationships',
        lessons: [
          { id: 'l13', title: 'Introduction to Geometry', duration: 15, type: 'video' },
          { id: 'l14', title: 'Lines and Angles', duration: 20, type: 'video' },
          { id: 'l15', title: 'Triangles and Quadrilaterals', duration: 25, type: 'video' },
          { id: 'l16', title: 'Circles and Polygons', duration: 22, type: 'video' },
        ],
        isLocked: true,
      },
    ],
  };

  const course = currentCourse || sampleCourse;

  if (isLoading && !currentCourse) {
    return <LoadingSpinner fullScreen />;
  }

  return (
    <div className={`space-y-6 ${mounted ? 'animate-in' : ''}`}>
      {/* Course Header */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="relative aspect-video bg-gradient-to-br from-primary-500 to-accent-600 rounded-xl overflow-hidden">
            <div className="absolute inset-0 flex items-center justify-center">
              <button className="w-20 h-20 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center hover:bg-white/30 transition-colors group">
                <Play className="w-10 h-10 text-white ml-1" />
              </button>
            </div>
            <div className="absolute bottom-4 left-4">
              <Badge variant="primary" size="md">
                {course.category}
              </Badge>
            </div>
          </div>
        </div>

        <div>
          <Card>
            <CardBody className="space-y-4">
              <div>
                <h1 className="text-xl font-bold text-secondary-900 mb-2">
                  {course.title}
                </h1>
                <p className="text-secondary-600 text-sm">{course.description}</p>
              </div>

              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1 text-amber-500">
                  <Star className="w-5 h-5 fill-current" />
                  <span className="font-bold">{course.rating}</span>
                </div>
                <span className="text-secondary-300">|</span>
                <span className="text-sm text-secondary-600">
                  {course.enrollmentsCount.toLocaleString()} students
                </span>
              </div>

              <div className="flex items-center gap-4 text-sm text-secondary-500">
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {Math.round(course.duration / 60)} hours
                </span>
                <span className="flex items-center gap-1">
                  <BookOpen className="w-4 h-4" />
                  {course.lessonsCount} lessons
                </span>
              </div>

              <div className="flex items-center gap-2">
                <Badge
                  variant={
                    course.difficulty === 'beginner'
                      ? 'success'
                      : course.difficulty === 'intermediate'
                      ? 'warning'
                      : 'error'
                  }
                >
                  {course.difficulty}
                </Badge>
                {course.price === 0 ? (
                  <Badge variant="success" className="text-lg px-3 py-1">
                    FREE
                  </Badge>
                ) : (
                  <Badge variant="warning" className="text-lg px-3 py-1">
                    ${course.price}
                  </Badge>
                )}
              </div>

              {!course.isEnrolled ? (
                <Button
                  variant="primary"
                  size="lg"
                  className="w-full"
                  onClick={handleEnroll}
                  isLoading={isEnrolling}
                  leftIcon={<BookOpen className="w-5 h-5" />}
                >
                  {course.price === 0 ? 'Enroll for Free' : `Enroll Now - $${course.price}`}
                </Button>
              ) : (
                <Link to={`/courses/${courseId}/lesson/l1`}>
                  <Button variant="primary" size="lg" className="w-full" leftIcon={<Play className="w-5 h-5" />}>
                    Continue Learning
                  </Button>
                </Link>
              )}
            </CardBody>
          </Card>
        </div>
      </div>

      {/* Course Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* What You'll Learn */}
          <Card>
            <CardHeader>
              <h2 className="section-title">What You'll Learn</h2>
            </CardHeader>
            <CardBody>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {course.features.map((feature, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span className="text-secondary-700">{feature}</span>
                  </li>
                ))}
              </ul>
            </CardBody>
          </Card>

          {/* Course Curriculum */}
          <Card>
            <CardHeader>
              <h2 className="section-title">Course Curriculum</h2>
              <p className="text-sm text-secondary-500 mt-1">
                {course.modules.length} modules • {course.lessonsCount} lessons
              </p>
            </CardHeader>
            <CardBody className="p-0">
              <div className="divide-y divide-secondary-100">
                {course.modules.map((module) => (
                  <div key={module.id}>
                    <button
                      onClick={() => toggleModule(module.id)}
                      className="w-full flex items-center justify-between p-4 hover:bg-secondary-50 transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        {module.isLocked ? (
                          <Lock className="w-5 h-5 text-secondary-400" />
                        ) : (
                          <div className="w-5 h-5 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center">
                            <ChevronDown className="w-3 h-3" />
                          </div>
                        )}
                        <div className="text-left">
                          <h3 className="font-medium text-secondary-900">{module.title}</h3>
                          <p className="text-sm text-secondary-500">
                            {module.lessons.length} lessons
                          </p>
                        </div>
                      </div>
                      {expandedModules.includes(module.id) ? (
                        <ChevronDown className="w-5 h-5 text-secondary-400" />
                      ) : (
                        <ChevronRight className="w-5 h-5 text-secondary-400" />
                      )}
                    </button>

                    {expandedModules.includes(module.id) && (
                      <div className="bg-secondary-50 px-4 py-2 space-y-1">
                        {module.lessons.map((lesson) => (
                          <Link
                            key={lesson.id}
                            to={!module.isLocked ? `/courses/${courseId}/lesson/${lesson.id}` : '#'}
                            className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${
                              module.isLocked
                                ? 'opacity-50 cursor-not-allowed'
                                : 'hover:bg-white'
                            }`}
                          >
                            {lesson.type === 'video' && <Play className="w-4 h-4 text-primary-600" />}
                            {lesson.type === 'quiz' && <Award className="w-4 h-4 text-amber-600" />}
                            {lesson.type === 'interactive' && <Globe className="w-4 h-4 text-green-600" />}
                            <span className="flex-1 text-sm text-secondary-700">{lesson.title}</span>
                            <span className="text-sm text-secondary-400">{lesson.duration} min</span>
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Instructor */}
          <Card>
            <CardHeader>
              <h2 className="section-title">Your Instructor</h2>
            </CardHeader>
            <CardBody>
              <div className="flex items-center gap-4 mb-4">
                <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 text-xl font-bold">
                  {course.instructor.name.split(' ').map(n => n[0]).join('')}
                </div>
                <div>
                  <h3 className="font-semibold text-secondary-900">{course.instructor.name}</h3>
                  <p className="text-sm text-secondary-500">{course.instructor.bio}</p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4 text-center border-t border-secondary-100 pt-4">
                <div>
                  <p className="text-lg font-bold text-secondary-900">{course.instructor.coursesCount}</p>
                  <p className="text-xs text-secondary-500">Courses</p>
                </div>
                <div>
                  <p className="text-lg font-bold text-secondary-900">
                    {(course.instructor.studentsCount / 1000).toFixed(0)}K
                  </p>
                  <p className="text-xs text-secondary-500">Students</p>
                </div>
                <div>
                  <p className="text-lg font-bold text-secondary-900">{course.instructor.rating}</p>
                  <p className="text-xs text-secondary-500">Rating</p>
                </div>
              </div>
            </CardBody>
          </Card>

          {/* Certificate */}
          <Card>
            <CardBody className="text-center">
              <Certificate className="w-12 h-12 mx-auto text-amber-500 mb-3" />
              <h3 className="font-semibold text-secondary-900 mb-1">Certificate of Completion</h3>
              <p className="text-sm text-secondary-600">
                Earn a certificate when you complete this course
              </p>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
}
