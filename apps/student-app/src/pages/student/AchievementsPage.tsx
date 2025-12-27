import { useEffect, useState } from 'react';
import { Trophy, Star, Flame, Target, BookOpen, Award, Lock } from 'lucide-react';
import Card, { CardBody, CardHeader } from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import ProgressBar from '../../components/common/ProgressBar';

interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: 'learning' | 'streak' | 'mastery' | 'social';
  unlockedAt?: string;
  progress?: number;
  isLocked: boolean;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
}

export default function AchievementsPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const categories = [
    { id: 'all', label: 'All', icon: Trophy },
    { id: 'learning', label: 'Learning', icon: BookOpen },
    { id: 'streak', label: 'Streaks', icon: Flame },
    { id: 'mastery', label: 'Mastery', icon: Target },
    { id: 'social', label: 'Social', icon: Award },
  ];

  // Sample achievements data
  const achievements: Achievement[] = [
    {
      id: '1',
      title: 'First Steps',
      description: 'Complete your first lesson',
      icon: '🎯',
      category: 'learning',
      unlockedAt: '2024-01-15',
      isLocked: false,
      rarity: 'common',
    },
    {
      id: '2',
      title: 'Knowledge Seeker',
      description: 'Complete 10 lessons',
      icon: '📚',
      category: 'learning',
      unlockedAt: '2024-01-20',
      isLocked: false,
      rarity: 'common',
    },
    {
      id: '3',
      title: 'Dedicated Learner',
      description: 'Complete 50 lessons',
      icon: '🎓',
      category: 'learning',
      progress: 72,
      isLocked: false,
      rarity: 'rare',
    },
    {
      id: '4',
      title: 'Week Warrior',
      description: 'Maintain a 7-day learning streak',
      icon: '🔥',
      category: 'streak',
      unlockedAt: '2024-01-22',
      isLocked: false,
      rarity: 'common',
    },
    {
      id: '5',
      title: 'Month Master',
      description: 'Maintain a 30-day learning streak',
      icon: '⚡',
      category: 'streak',
      progress: 45,
      isLocked: false,
      rarity: 'epic',
    },
    {
      id: '6',
      title: 'Perfect Score',
      description: 'Get 100% on a quiz',
      icon: '💯',
      category: 'mastery',
      unlockedAt: '2024-01-18',
      isLocked: false,
      rarity: 'rare',
    },
    {
      id: '7',
      title: 'Math Whiz',
      description: 'Complete all math courses',
      icon: '🧮',
      category: 'mastery',
      progress: 65,
      isLocked: false,
      rarity: 'epic',
    },
    {
      id: '8',
      title: 'Physics Pro',
      description: 'Complete all physics courses',
      icon: '⚛️',
      category: 'mastery',
      progress: 40,
      isLocked: false,
      rarity: 'epic',
    },
    {
      id: '9',
      title: 'Early Bird',
      description: 'Complete a lesson before 7 AM',
      icon: '🌅',
      category: 'learning',
      isLocked: true,
      rarity: 'rare',
    },
    {
      id: '10',
      title: 'Night Owl',
      description: 'Complete a lesson after 11 PM',
      icon: '🦉',
      category: 'learning',
      isLocked: true,
      rarity: 'rare',
    },
    {
      id: '11',
      title: 'Helpful Hero',
      description: 'Answer 10 questions in discussions',
      icon: '🤝',
      category: 'social',
      isLocked: true,
      rarity: 'rare',
    },
    {
      id: '12',
      title: 'Legend',
      description: 'Achieve a 100-day streak',
      icon: '👑',
      category: 'streak',
      progress: 15,
      isLocked: false,
      rarity: 'legendary',
    },
  ];

  const filteredAchievements = selectedCategory === 'all'
    ? achievements
    : achievements.filter(a => a.category === selectedCategory);

  const unlockedCount = achievements.filter(a => !a.isLocked).length;
  const totalCount = achievements.length;

  const rarityColors = {
    common: 'from-secondary-400 to-secondary-500',
    rare: 'from-blue-400 to-blue-600',
    epic: 'from-purple-400 to-purple-600',
    legendary: 'from-amber-400 to-orange-500',
  };

  const rarityBorderColors = {
    common: 'border-secondary-300',
    rare: 'border-blue-300',
    epic: 'border-purple-300',
    legendary: 'border-amber-300',
  };

  return (
    <div className={`space-y-6 ${mounted ? 'animate-in' : ''}`}>
      {/* Header */}
      <div>
        <h1 className="page-title">Achievements</h1>
        <p className="page-subtitle">
          Track your accomplishments and earn badges
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardBody className="text-center">
            <div className="w-16 h-16 mx-auto rounded-full bg-amber-100 flex items-center justify-center mb-3">
              <Trophy className="w-8 h-8 text-amber-600" />
            </div>
            <p className="text-3xl font-bold text-secondary-900">
              {unlockedCount}/{totalCount}
            </p>
            <p className="text-sm text-secondary-500">Achievements</p>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="w-16 h-16 mx-auto rounded-full bg-green-100 flex items-center justify-center mb-3">
              <Star className="w-8 h-8 text-green-600" />
            </div>
            <p className="text-3xl font-bold text-secondary-900">12</p>
            <p className="text-sm text-secondary-500">Badges Earned</p>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="w-16 h-16 mx-auto rounded-full bg-orange-100 flex items-center justify-center mb-3">
              <Flame className="w-8 h-8 text-orange-600" />
            </div>
            <p className="text-3xl font-bold text-secondary-900">7</p>
            <p className="text-sm text-secondary-500">Day Streak</p>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="w-16 h-16 mx-auto rounded-full bg-purple-100 flex items-center justify-center mb-3">
              <Target className="w-8 h-8 text-purple-600" />
            </div>
            <p className="text-3xl font-bold text-secondary-900">1450</p>
            <p className="text-sm text-secondary-500">Total XP</p>
          </CardBody>
        </Card>
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              selectedCategory === category.id
                ? 'bg-primary-600 text-white'
                : 'bg-secondary-100 text-secondary-700 hover:bg-secondary-200'
            }`}
          >
            <category.icon className="w-4 h-4" />
            {category.label}
          </button>
        ))}
      </div>

      {/* Achievement Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {filteredAchievements.map((achievement, index) => (
          <div
            key={achievement.id}
            className={mounted ? 'animate-in' : ''}
            style={{ animationDelay: `${index * 50}ms` }}
          >
            <Card
              hover
              className={`h-full ${achievement.isLocked ? 'opacity-60' : ''}`}
            >
              <CardBody className="text-center">
                <div className="relative inline-block mb-4">
                  <div
                    className={`w-20 h-20 rounded-full bg-gradient-to-br ${
                      rarityColors[achievement.rarity]
                    } flex items-center justify-center text-3xl shadow-lg ${
                      achievement.isLocked ? 'grayscale' : ''
                    }`}
                  >
                    {achievement.isLocked ? (
                      <Lock className="w-8 h-8 text-secondary-400" />
                    ) : (
                      achievement.icon
                    )}
                  </div>
                  {achievement.unlockedAt && (
                    <div className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                </div>

                <Badge
                  variant={
                    achievement.rarity === 'legendary'
                      ? 'warning'
                      : achievement.rarity === 'epic'
                      ? 'primary'
                      : achievement.rarity === 'rare'
                      ? 'secondary'
                      : 'secondary'
                  }
                  size="sm"
                  className="mb-2"
                >
                  {achievement.rarity}
                </Badge>

                <h3 className="font-semibold text-secondary-900 mb-1">
                  {achievement.title}
                </h3>
                <p className="text-sm text-secondary-600 mb-3">
                  {achievement.description}
                </p>

                {achievement.progress !== undefined && achievement.isLocked === false && (
                  <ProgressBar value={achievement.progress} size="sm" />
                )}
              </CardBody>
            </Card>
          </div>
        ))}
      </div>

      {/* Rarity Guide */}
      <Card>
        <CardHeader>
          <h2 className="section-title">Rarity Guide</h2>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-secondary-400 to-secondary-500" />
              <div>
                <p className="font-medium text-secondary-900">Common</p>
                <p className="text-sm text-secondary-500">Easy to unlock</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600" />
              <div>
                <p className="font-medium text-secondary-900">Rare</p>
                <p className="text-sm text-secondary-500">Requires effort</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-purple-600" />
              <div>
                <p className="font-medium text-secondary-900">Epic</p>
                <p className="text-sm text-secondary-500">Significant dedication</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-400 to-orange-500" />
              <div>
                <p className="font-medium text-secondary-900">Legendary</p>
                <p className="text-sm text-secondary-500">Exceptional achievement</p>
              </div>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  );
}
