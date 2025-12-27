import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Search,
  Filter,
  Grid,
  List,
  ChevronDown,
  Star,
  Clock,
  BookOpen,
} from 'lucide-react';
import { useCourseStore } from '../../store/courseStore';
import Card, { CardBody } from '../../components/common/Card';
import Button from '../../components/common/Button';
import Badge from '../../components/common/Badge';
import Input from '../../components/common/Input';
import LoadingSpinner from '../../components/common/LoadingSpinner';

const categories = [
  'All',
  'Mathematics',
  'Physics',
  'Chemistry',
  'Biology',
  'Computer Science',
  'Engineering',
];

const difficulties = [
  { value: '', label: 'All Levels' },
  { value: 'beginner', label: 'Beginner' },
  { value: 'intermediate', label: 'Intermediate' },
  { value: 'advanced', label: 'Advanced' },
];

export default function CoursesPage() {
  const { courses, filters, setFilters, fetchCourses, isLoading } = useCourseStore();
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    fetchCourses();
  }, [fetchCourses]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setFilters({
      ...filters,
      search: searchQuery,
    });
    fetchCourses({ ...filters, search: searchQuery });
  };

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category);
    setFilters({
      ...filters,
      category: category === 'All' ? undefined : category.toLowerCase(),
    });
    fetchCourses({
      ...filters,
      category: category === 'All' ? undefined : category.toLowerCase(),
    });
  };

  const handleDifficultyChange = (difficulty: string) => {
    setSelectedDifficulty(difficulty);
    setFilters({
      ...filters,
      difficulty: difficulty || undefined,
    });
    fetchCourses({
      ...filters,
      difficulty: difficulty || undefined,
    });
  };

  // Sample courses data
  const sampleCourses = [
    {
      id: '1',
      title: 'Mathematics Fundamentals',
      description: 'Master the basics of algebra, calculus, and geometry with interactive visualizations.',
      instructor: { name: 'Dr. Sarah Chen', avatar: '' },
      category: 'Mathematics',
      difficulty: 'beginner',
      duration: 1200,
      lessonsCount: 48,
      rating: 4.8,
      enrollmentsCount: 15420,
      price: 0,
      thumbnail: '/api/placeholder/400/225',
    },
    {
      id: '2',
      title: 'Physics: Classical Mechanics',
      description: 'Explore motion, forces, and energy through stunning animations and real-world examples.',
      instructor: { name: 'Prof. James Wilson', avatar: '' },
      category: 'Physics',
      difficulty: 'intermediate',
      duration: 1800,
      lessonsCount: 64,
      rating: 4.9,
      enrollmentsCount: 12850,
      price: 29.99,
      thumbnail: '/api/placeholder/400/225',
    },
    {
      id: '3',
      title: 'Organic Chemistry Essentials',
      description: 'Understand molecular structures and reactions with 3D visualizations.',
      instructor: { name: 'Dr. Emily Roberts', avatar: '' },
      category: 'Chemistry',
      difficulty: 'intermediate',
      duration: 1500,
      lessonsCount: 52,
      rating: 4.7,
      enrollmentsCount: 8920,
      price: 0,
      thumbnail: '/api/placeholder/400/225',
    },
    {
      id: '4',
      title: 'Calculus Mastery',
      description: 'Deep dive into derivatives, integrals, and their applications.',
      instructor: { name: 'Dr. Michael Lee', avatar: '' },
      category: 'Mathematics',
      difficulty: 'advanced',
      duration: 2400,
      lessonsCount: 80,
      rating: 4.9,
      enrollmentsCount: 6540,
      price: 49.99,
      thumbnail: '/api/placeholder/400/225',
    },
    {
      id: '5',
      title: 'Quantum Physics Introduction',
      description: 'Discover the fascinating world of quantum mechanics.',
      instructor: { name: 'Dr. Lisa Anderson', avatar: '' },
      category: 'Physics',
      difficulty: 'advanced',
      duration: 2000,
      lessonsCount: 72,
      rating: 4.8,
      enrollmentsCount: 5230,
      price: 39.99,
      thumbnail: '/api/placeholder/400/225',
    },
    {
      id: '6',
      title: 'Biology: Cell Structure',
      description: 'Explore the building blocks of life through detailed animations.',
      instructor: { name: 'Dr. Robert Kim', avatar: '' },
      category: 'Biology',
      difficulty: 'beginner',
      duration: 900,
      lessonsCount: 36,
      rating: 4.6,
      enrollmentsCount: 11200,
      price: 0,
      thumbnail: '/api/placeholder/400/225',
    },
  ];

  const displayCourses = courses.length > 0 ? courses : sampleCourses;

  if (isLoading && courses.length === 0) {
    return <LoadingSpinner fullScreen />;
  }

  return (
    <div className={`space-y-6 ${mounted ? 'animate-in' : ''}`}>
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="page-title">Explore Courses</h1>
          <p className="page-subtitle">
            Discover interactive courses in mathematics, physics, and chemistry
          </p>
        </div>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardBody>
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search */}
            <form onSubmit={handleSearch} className="flex-1">
              <Input
                placeholder="Search courses..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                leftIcon={<Search className="w-5 h-5" />}
              />
            </form>

            {/* Filter Toggle (Mobile) */}
            <Button
              variant="secondary"
              onClick={() => setShowFilters(!showFilters)}
              className="lg:hidden"
              leftIcon={<Filter className="w-4 h-4" />}
            >
              Filters
            </Button>

            {/* View Mode Toggle */}
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
          </div>

          {/* Filters */}
          <div className={`mt-4 pt-4 border-t border-secondary-200 ${showFilters ? 'block' : 'hidden lg:block'}`}>
            {/* Categories */}
            <div className="flex flex-wrap gap-2 mb-4">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => handleCategoryChange(category)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    selectedCategory === category
                      ? 'bg-primary-600 text-white'
                      : 'bg-secondary-100 text-secondary-700 hover:bg-secondary-200'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>

            {/* Difficulty Dropdown */}
            <div className="relative inline-block">
              <select
                value={selectedDifficulty}
                onChange={(e) => handleDifficultyChange(e.target.value)}
                className="appearance-none px-4 py-2 pr-10 rounded-lg border border-secondary-200 bg-white text-secondary-700 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                {difficulties.map((diff) => (
                  <option key={diff.value} value={diff.value}>
                    {diff.label}
                  </option>
                ))}
              </select>
              <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary-400 pointer-events-none" />
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-secondary-600">
          Showing <span className="font-medium text-secondary-900">{displayCourses.length}</span> courses
        </p>
      </div>

      {/* Course Grid/List */}
      <div
        className={
          viewMode === 'grid'
            ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
            : 'space-y-4'
        }
      >
        {displayCourses.map((course, index) => (
          <div
            key={course.id}
            className={mounted ? 'animate-in' : ''}
            style={{ animationDelay: `${index * 50}ms` }}
          >
            <Card hover className="h-full">
              {viewMode === 'grid' ? (
                <>
                  {/* Grid View */}
                  <div className="relative aspect-video bg-gradient-to-br from-primary-400 to-accent-500">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <BookOpen className="w-12 h-12 text-white/50" />
                    </div>
                    {course.price === 0 ? (
                      <Badge variant="success" className="absolute top-3 left-3">
                        Free
                      </Badge>
                    ) : (
                      <Badge variant="warning" className="absolute top-3 left-3">
                        ${course.price}
                      </Badge>
                    )}
                  </div>
                  <CardBody className="flex flex-col flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant="secondary">{course.category}</Badge>
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
                    </div>
                    <h3 className="font-semibold text-secondary-900 mb-2 line-clamp-2">
                      {course.title}
                    </h3>
                    <p className="text-sm text-secondary-600 mb-4 line-clamp-2 flex-1">
                      {course.description}
                    </p>
                    <div className="flex items-center gap-2 mb-4">
                      <div className="flex items-center gap-1 text-amber-500">
                        <Star className="w-4 h-4 fill-current" />
                        <span className="text-sm font-medium">{course.rating}</span>
                      </div>
                      <span className="text-secondary-300">|</span>
                      <span className="text-sm text-secondary-600">
                        {course.enrollmentsCount.toLocaleString()} students
                      </span>
                    </div>
                    <div className="flex items-center justify-between pt-4 border-t border-secondary-100">
                      <div className="flex items-center gap-4 text-sm text-secondary-500">
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {Math.round(course.duration / 60)}h
                        </span>
                        <span className="flex items-center gap-1">
                          <BookOpen className="w-4 h-4" />
                          {course.lessonsCount} lessons
                        </span>
                      </div>
                      <Link to={`/courses/${course.id}`}>
                        <Button variant="primary" size="sm">
                          View Course
                        </Button>
                      </Link>
                    </div>
                  </CardBody>
                </>
              ) : (
                /* List View */
                <CardBody>
                  <div className="flex gap-4">
                    <div className="w-32 h-20 rounded-lg bg-gradient-to-br from-primary-400 to-accent-500 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant="secondary">{course.category}</Badge>
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
                          <Badge variant="success">Free</Badge>
                        ) : (
                          <Badge variant="warning">${course.price}</Badge>
                        )}
                      </div>
                      <h3 className="font-semibold text-secondary-900 mb-1">
                        {course.title}
                      </h3>
                      <p className="text-sm text-secondary-600 mb-2 line-clamp-1">
                        {course.description}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-secondary-500">
                        <span className="flex items-center gap-1 text-amber-500">
                          <Star className="w-4 h-4 fill-current" />
                          {course.rating}
                        </span>
                        <span>{course.enrollmentsCount.toLocaleString()} students</span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {Math.round(course.duration / 60)}h
                        </span>
                        <span className="flex items-center gap-1">
                          <BookOpen className="w-4 h-4" />
                          {course.lessonsCount} lessons
                        </span>
                      </div>
                    </div>
                    <Link to={`/courses/${course.id}`}>
                      <Button variant="primary">View Course</Button>
                    </Link>
                  </div>
                </CardBody>
              )}
            </Card>
          </div>
        ))}
      </div>

      {/* Load More */}
      <div className="text-center">
        <Button variant="secondary" size="lg">
          Load More Courses
        </Button>
      </div>
    </div>
  );
}
