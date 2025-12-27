import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  Clock,
  Trophy,
  TrendingUp,
  Play,
  ArrowRight,
  Flame,
  Target,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { useProgressStore } from '../../store/progressStore';
import Card, { CardBody, CardHeader } from '../../components/common/Card';
import Button from '../../components/common/Button';
import ProgressBar from '../../components/common/ProgressBar';
import Badge from '../../components/common/Badge';
import LoadingSpinner from '../../components/common/LoadingSpinner';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle: string;
  icon: React.ReactNode;
  trend?: { value: number; label: string };
  color: 'primary' | 'green' | 'amber' | 'purple';
}

const StatCard = ({ title, value, subtitle, icon, trend, color }: StatCardProps) => {
  const colorClasses = {
    primary: 'bg-primary-100 text-primary-600',
    green: 'bg-green-100 text-green-600',
    amber: 'bg-amber-100 text-amber-600',
    purple: 'bg-purple-100 text-purple-600',
  };

  return (
    <Card hover>
      <CardBody>
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm font-medium text-secondary-600">{title}</p>
            <p className="text-3xl font-bold text-secondary-900 mt-1">{value}</p>
            <p className="text-sm text-secondary-500 mt-1">{subtitle}</p>
            {trend && (
              <div className="flex items-center gap-1 mt-2 text-green-600">
                <TrendingUp className="w-4 h-4" />
                <span className="text-sm font-medium">+{trend.value}%</span>
                <span className="text-sm text-secondary-500">{trend.label}</span>
              </div>
            )}
          </div>
          <div className={`p-3 rounded-xl ${colorClasses[color]}`}>
            {icon}
          </div>
        </div>
      </CardBody>
    </Card>
  );
};

export default function DashboardPage() {
  const { user } = useAuthStore();
  const { userStats, fetchUserStats, isLoading } = useProgressStore();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    fetchUserStats();
  }, [fetchUserStats]);

  if (isLoading && !userStats) {
    return <LoadingSpinner fullScreen />;
  }

  const stats = [
    {
      title: 'Courses Enrolled',
      value: userStats?.totalCoursesEnrolled || 0,
      subtitle: 'Active courses',
      icon: <BookOpen className="w-6 h-6" />,
      color: 'primary' as const,
      trend: { value: 12, label: 'this month' },
    },
    {
      title: 'Lessons Completed',
      value: userStats?.totalLessonsCompleted || 0,
      subtitle: 'Total lessons',
      icon: <Target className="w-6 h-6" />,
      color: 'green' as const,
    },
    {
      title: 'Learning Streak',
      value: `${userStats?.streak?.current || 0} days`,
      subtitle: 'Longest: 7 days',
      icon: <Flame className="w-6 h-6" />,
      color: 'amber' as const,
    },
    {
      title: 'Achievements',
      value: userStats?.achievements?.length || 0,
      subtitle: 'Badges earned',
      icon: <Trophy className="w-6 h-6" />,
      color: 'purple' as const,
    },
  ];

  const recentCourses = [
    {
      id: '1',
      title: 'Mathematics Fundamentals',
      progress: 65,
      nextLesson: 'Calculus Basics',
      duration: '15 min',
      thumbnail: '/api/placeholder/400/225',
    },
    {
      id: '2',
      title: 'Physics: Mechanics',
      progress: 40,
      nextLesson: 'Newton\'s Laws',
      duration: '20 min',
      thumbnail: '/api/placeholder/400/225',
    },
    {
      id: '3',
      title: 'Chemistry Essentials',
      progress: 85,
      nextLesson: 'Organic Compounds',
      duration: '10 min',
      thumbnail: '/api/placeholder/400/225',
    },
  ];

  return (
    <div className={`space-y-6 ${mounted ? 'animate-in' : ''}`}>
      {/* Welcome Section */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="page-title">
            Welcome back, {user?.firstName || 'Student'}!
          </h1>
          <p className="page-subtitle">
            Continue your learning journey where you left off
          </p>
        </div>
        <Link to="/courses">
          <Button variant="outline" rightIcon={<ArrowRight className="w-4 h-4" />}>
            Browse Courses
          </Button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <div
            key={stat.title}
            className={mounted ? 'animate-in' : ''}
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <StatCard {...stat} />
          </div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Continue Learning */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <h2 className="section-title mb-0">Continue Learning</h2>
              <Link to="/my-learning" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
                View All
              </Link>
            </CardHeader>
            <CardBody className="space-y-4">
              {recentCourses.map((course) => (
                <div
                  key={course.id}
                  className="flex gap-4 p-4 rounded-xl bg-secondary-50 hover:bg-secondary-100 transition-colors group"
                >
                  <div className="w-24 h-16 rounded-lg bg-secondary-200 overflow-hidden flex-shrink-0">
                    <div className="w-full h-full bg-gradient-to-br from-primary-400 to-primary-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-secondary-900 truncate">
                      {course.title}
                    </h3>
                    <p className="text-sm text-secondary-600 mt-0.5">
                      Next: {course.nextLesson}
                    </p>
                    <div className="flex items-center gap-4 mt-2">
                      <ProgressBar value={course.progress} size="sm" className="flex-1" />
                      <span className="text-sm font-medium text-secondary-700">
                        {course.progress}%
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <Link
                      to={`/courses/${course.id}/lesson/1`}
                      className="p-3 rounded-full bg-primary-600 text-white opacity-0 group-hover:opacity-100 transition-opacity hover:bg-primary-700"
                    >
                      <Play className="w-5 h-5" />
                    </Link>
                  </div>
                </div>
              ))}
            </CardBody>
          </Card>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Daily Goal */}
          <Card>
            <CardHeader>
              <h2 className="section-title">Daily Goal</h2>
            </CardHeader>
            <CardBody>
              <div className="text-center">
                <div className="relative inline-flex items-center justify-center w-24 h-24 mb-4">
                  <svg className="w-24 h-24 transform -rotate-90">
                    <circle
                      cx="48"
                      cy="48"
                      r="40"
                      stroke="#e5e7eb"
                      strokeWidth="8"
                      fill="none"
                    />
                    <circle
                      cx="48"
                      cy="48"
                      r="40"
                      stroke="#0ea5e9"
                      strokeWidth="8"
                      fill="none"
                      strokeDasharray="251.2"
                      strokeDashoffset="251.2 - (251.2 * 45 / 100)"
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <Clock className="w-5 h-5 text-primary-600 mb-0.5" />
                    <span className="text-lg font-bold text-secondary-900">45</span>
                    <span className="text-xs text-secondary-500">/60 min</span>
                  </div>
                </div>
                <p className="text-sm text-secondary-600">
                  You're 75% through your daily learning goal!
                </p>
                <Button variant="primary" size="sm" className="mt-4 w-full">
                  Continue Learning
                </Button>
              </div>
            </CardBody>
          </Card>

          {/* Recent Achievements */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <h2 className="section-title mb-0">Recent Achievements</h2>
              <Link to="/achievements" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
                View All
              </Link>
            </CardHeader>
            <CardBody>
              <div className="flex gap-3">
                {['🏆', '🔥', '📚', '⭐'].map((emoji, index) => (
                  <div
                    key={index}
                    className="flex-1 aspect-square rounded-xl bg-amber-100 flex items-center justify-center text-2xl hover:scale-110 transition-transform cursor-pointer"
                  >
                    {emoji}
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>

          {/* Upcoming */}
          <Card>
            <CardHeader>
              <h2 className="section-title">Upcoming</h2>
            </CardHeader>
            <CardBody className="space-y-3">
              <div className="flex items-center gap-3 p-2 rounded-lg bg-green-50">
                <div className="p-2 rounded-lg bg-green-100">
                  <Target className="w-4 h-4 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-secondary-900">New Module</p>
                  <p className="text-xs text-secondary-600">Physics: Thermodynamics</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-2 rounded-lg bg-purple-50">
                <div className="p-2 rounded-lg bg-purple-100">
                  <Trophy className="w-4 h-4 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-secondary-900">Weekly Quiz</p>
                  <p className="text-xs text-secondary-600">Mathematics</p>
                </div>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
}
