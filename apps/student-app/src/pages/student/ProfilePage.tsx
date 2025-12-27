import { useState } from 'react';
import {
  User,
  Mail,
  Calendar,
  Edit2,
  Camera,
  Save,
  X,
  Award,
  BookOpen,
  Clock,
  Trophy,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import Card, { CardBody, CardHeader } from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Badge from '../../components/common/Badge';
import ProgressBar from '../../components/common/ProgressBar';

export default function ProfilePage() {
  const { user } = useAuthStore();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    email: user?.email || '',
  });

  const handleSave = () => {
    // Save profile changes
    setIsEditing(false);
  };

  // Sample user stats
  const stats = {
    coursesEnrolled: 4,
    coursesCompleted: 1,
    lessonsCompleted: 145,
    totalHours: 48,
    achievements: 12,
    streak: 7,
    rank: 156,
  };

  // Sample recent activity
  const recentActivity = [
    { type: 'lesson', title: 'Understanding Numbers', course: 'Mathematics Fundamentals', time: '2 hours ago' },
    { type: 'achievement', title: 'Week Warrior', description: '7-day streak achieved', time: '1 day ago' },
    { type: 'quiz', title: 'Basic Operations Quiz', course: 'Mathematics Fundamentals', score: '92%', time: '2 days ago' },
    { type: 'lesson', title: 'Newton\'s Laws', course: 'Physics: Classical Mechanics', time: '3 days ago' },
  ];

  return (
    <div className="space-y-6">
      {/* Profile Header */}
      <Card>
        <div className="relative h-32 bg-gradient-to-r from-primary-500 to-accent-500">
          <button className="absolute bottom-4 right-4 p-2 rounded-full bg-white/20 hover:bg-white/30 transition-colors">
            <Camera className="w-5 h-5 text-white" />
          </button>
        </div>
        <CardBody>
          <div className="flex flex-col md:flex-row gap-6 -mt-16">
            <div className="relative">
              <div className="w-32 h-32 rounded-2xl bg-gradient-to-br from-primary-400 to-accent-500 flex items-center justify-center text-white text-4xl font-bold shadow-lg">
                {user?.firstName?.[0]}{user?.lastName?.[0]}
              </div>
              <button className="absolute bottom-2 right-2 p-2 rounded-full bg-secondary-900 text-white hover:bg-secondary-800 transition-colors">
                <Camera className="w-4 h-4" />
              </button>
            </div>

            <div className="flex-1 pt-4 md:pt-16">
              <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                <div>
                  {isEditing ? (
                    <div className="flex gap-4 mb-4">
                      <Input
                        value={formData.firstName}
                        onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                        placeholder="First Name"
                        className="w-40"
                      />
                      <Input
                        value={formData.lastName}
                        onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                        placeholder="Last Name"
                        className="w-40"
                      />
                    </div>
                  ) : (
                    <h1 className="text-2xl font-bold text-secondary-900 mb-1">
                      {user?.firstName} {user?.lastName}
                    </h1>
                  )}
                  <p className="text-secondary-600 mb-2">{user?.email}</p>
                  <Badge variant="primary">Student</Badge>
                </div>

                <div className="flex gap-2">
                  {isEditing ? (
                    <>
                      <Button variant="secondary" onClick={() => setIsEditing(false)} leftIcon={<X className="w-4 h-4" />}>
                        Cancel
                      </Button>
                      <Button variant="primary" onClick={handleSave} leftIcon={<Save className="w-4 h-4" />}>
                        Save Changes
                      </Button>
                    </>
                  ) : (
                    <Button variant="secondary" onClick={() => setIsEditing(true)} leftIcon={<Edit2 className="w-4 h-4" />}>
                      Edit Profile
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardBody className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-primary-100">
              <BookOpen className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-secondary-900">{stats.coursesEnrolled}</p>
              <p className="text-sm text-secondary-500">Courses Enrolled</p>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-green-100">
              <Award className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-secondary-900">{stats.coursesCompleted}</p>
              <p className="text-sm text-secondary-500">Completed</p>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-amber-100">
              <Clock className="w-6 h-6 text-amber-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-secondary-900">{stats.totalHours}h</p>
              <p className="text-sm text-secondary-500">Learning Time</p>
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="flex items-center gap-4">
            <div className="p-3 rounded-xl bg-purple-100">
              <Trophy className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-secondary-900">#{stats.rank}</p>
              <p className="text-sm text-secondary-500">Global Rank</p>
            </div>
          </CardBody>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <h2 className="section-title">Recent Activity</h2>
            </CardHeader>
            <CardBody className="p-0">
              <div className="divide-y divide-secondary-100">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-center gap-4 p-4 hover:bg-secondary-50 transition-colors">
                    <div className={`p-2 rounded-lg ${
                      activity.type === 'lesson' ? 'bg-primary-100' :
                      activity.type === 'achievement' ? 'bg-amber-100' :
                      'bg-green-100'
                    }`}>
                      {activity.type === 'lesson' && <BookOpen className="w-5 h-5 text-primary-600" />}
                      {activity.type === 'achievement' && <Trophy className="w-5 h-5 text-amber-600" />}
                      {activity.type === 'quiz' && <Award className="w-5 h-5 text-green-600" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-secondary-900">{activity.title}</p>
                      <p className="text-sm text-secondary-600">{activity.course}</p>
                      {activity.score && (
                        <p className="text-sm text-green-600 font-medium">{activity.score}</p>
                      )}
                    </div>
                    <span className="text-sm text-secondary-400">{activity.time}</span>
                  </div>
                ))}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Progress Overview */}
        <div>
          <Card>
            <CardHeader>
              <h2 className="section-title">Weekly Goal</h2>
            </CardHeader>
            <CardBody className="space-y-6">
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
                      strokeDashoffset="251.2 - (251.2 * 75 / 100)"
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-2xl font-bold text-secondary-900">75%</span>
                  </div>
                </div>
                <p className="text-sm text-secondary-600">45 of 60 minutes daily</p>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-secondary-600">Lessons This Week</span>
                  <span className="font-medium text-secondary-900">12/15</span>
                </div>
                <ProgressBar value={80} />

                <div className="flex items-center justify-between">
                  <span className="text-sm text-secondary-600">Quiz Average</span>
                  <span className="font-medium text-secondary-900">88%</span>
                </div>
                <ProgressBar value={88} />

                <div className="flex items-center justify-between">
                  <span className="text-sm text-secondary-600">Learning Days</span>
                  <span className="font-medium text-secondary-900">5/7</span>
                </div>
                <ProgressBar value={71} />
              </div>
            </CardBody>
          </Card>

          {/* Streak Card */}
          <Card className="mt-6">
            <CardBody className="text-center">
              <div className="w-16 h-16 mx-auto rounded-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center mb-3">
                <span className="text-2xl">🔥</span>
              </div>
              <p className="text-3xl font-bold text-secondary-900">{stats.streak} Days</p>
              <p className="text-sm text-secondary-500 mb-3">Current Streak</p>
              <p className="text-xs text-secondary-400">Longest: 14 days</p>
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
}
