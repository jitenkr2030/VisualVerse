import { useState } from 'react';
import {
  User,
  Bell,
  Lock,
  Palette,
  Globe,
  Mail,
  Smartphone,
  Moon,
  Sun,
  Monitor,
  ChevronRight,
  ToggleLeft,
  ToggleRight,
  Save,
} from 'lucide-react';
import Card, { CardBody, CardHeader } from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import { useAuthStore } from '../../store/authStore';

type Theme = 'light' | 'dark' | 'system';

interface SettingSection {
  id: string;
  title: string;
  icon: React.ReactNode;
}

const settingSections: SettingSection[] = [
  { id: 'profile', title: 'Profile', icon: <User className="w-5 h-5" /> },
  { id: 'notifications', title: 'Notifications', icon: <Bell className="w-5 h-5" /> },
  { id: 'appearance', title: 'Appearance', icon: <Palette className="w-5 h-5" /> },
  { id: 'privacy', title: 'Privacy & Security', icon: <Lock className="w-5 h-5" /> },
  { id: 'language', title: 'Language & Region', icon: <Globe className="w-5 h-5" /> },
];

export default function SettingsPage() {
  const { user, updateProfile } = useAuthStore();
  const [activeSection, setActiveSection] = useState('profile');
  const [theme, setTheme] = useState<Theme>('system');
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    courseUpdates: true,
    achievements: true,
    weeklyDigest: false,
  });
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    setIsSaving(true);
    // Simulate save
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setIsSaving(false);
  };

  const toggleNotification = (key: keyof typeof notifications) => {
    setNotifications((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const renderContent = () => {
    switch (activeSection) {
      case 'profile':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-secondary-900 mb-4">Personal Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input label="First Name" defaultValue={user?.firstName} />
                <Input label="Last Name" defaultValue={user?.lastName} />
                <Input label="Email" type="email" defaultValue={user?.email} />
                <Input label="Phone" type="tel" placeholder="+1 (555) 000-0000" />
              </div>
            </div>

            <div className="border-t border-secondary-200 pt-6">
              <h2 className="text-lg font-semibold text-secondary-900 mb-4">Bio</h2>
              <textarea
                className="w-full px-4 py-3 rounded-lg border border-secondary-300 bg-white text-secondary-900 placeholder-secondary-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                rows={4}
                placeholder="Tell us about yourself..."
                defaultValue="Passionate learner exploring mathematics and physics."
              />
            </div>
          </div>
        );

      case 'notifications':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-secondary-900 mb-4">Notification Preferences</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Mail className="w-5 h-5 text-secondary-600" />
                    <div>
                      <p className="font-medium text-secondary-900">Email Notifications</p>
                      <p className="text-sm text-secondary-500">Receive updates via email</p>
                    </div>
                  </div>
                  <button
                    onClick={() => toggleNotification('email')}
                    className={notifications.email ? 'text-primary-600' : 'text-secondary-300'}
                  >
                    {notifications.email ? <ToggleRight className="w-8 h-8" /> : <ToggleLeft className="w-8 h-8" />}
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Smartphone className="w-5 h-5 text-secondary-600" />
                    <div>
                      <p className="font-medium text-secondary-900">Push Notifications</p>
                      <p className="text-sm text-secondary-500">Receive browser notifications</p>
                    </div>
                  </div>
                  <button
                    onClick={() => toggleNotification('push')}
                    className={notifications.push ? 'text-primary-600' : 'text-secondary-300'}
                  >
                    {notifications.push ? <ToggleRight className="w-8 h-8" /> : <ToggleLeft className="w-8 h-8" />}
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Bell className="w-5 h-5 text-secondary-600" />
                    <div>
                      <p className="font-medium text-secondary-900">Course Updates</p>
                      <p className="text-sm text-secondary-500">New lessons, content updates</p>
                    </div>
                  </div>
                  <button
                    onClick={() => toggleNotification('courseUpdates')}
                    className={notifications.courseUpdates ? 'text-primary-600' : 'text-secondary-300'}
                  >
                    {notifications.courseUpdates ? <ToggleRight className="w-8 h-8" /> : <ToggleLeft className="w-8 h-8" />}
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Award className="w-5 h-5 text-secondary-600" />
                    <div>
                      <p className="font-medium text-secondary-900">Achievement Notifications</p>
                      <p className="text-sm text-secondary-500">Badges, milestones, streaks</p>
                    </div>
                  </div>
                  <button
                    onClick={() => toggleNotification('achievements')}
                    className={notifications.achievements ? 'text-primary-600' : 'text-secondary-300'}
                  >
                    {notifications.achievements ? <ToggleRight className="w-8 h-8" /> : <ToggleLeft className="w-8 h-8" />}
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Mail className="w-5 h-5 text-secondary-600" />
                    <div>
                      <p className="font-medium text-secondary-900">Weekly Digest</p>
                      <p className="text-sm text-secondary-500">Summary of your learning progress</p>
                    </div>
                  </div>
                  <button
                    onClick={() => toggleNotification('weeklyDigest')}
                    className={notifications.weeklyDigest ? 'text-primary-600' : 'text-secondary-300'}
                  >
                    {notifications.weeklyDigest ? <ToggleRight className="w-8 h-8" /> : <ToggleLeft className="w-8 h-8" />}
                  </button>
                </div>
              </div>
            </div>
          </div>
        );

      case 'appearance':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-secondary-900 mb-4">Theme</h2>
              <div className="grid grid-cols-3 gap-4">
                {[
                  { value: 'light' as Theme, icon: Sun, label: 'Light', description: 'Always use light mode' },
                  { value: 'dark' as Theme, icon: Moon, label: 'Dark', description: 'Always use dark mode' },
                  { value: 'system' as Theme, icon: Monitor, label: 'System', description: 'Match system settings' },
                ].map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setTheme(option.value)}
                    className={`p-4 rounded-xl border-2 transition-all ${
                      theme === option.value
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-secondary-200 hover:border-secondary-300'
                    }`}
                  >
                    <option.icon className={`w-8 h-8 mx-auto mb-2 ${
                      theme === option.value ? 'text-primary-600' : 'text-secondary-400'
                    }`} />
                    <p className="font-medium text-secondary-900">{option.label}</p>
                    <p className="text-xs text-secondary-500">{option.description}</p>
                  </button>
                ))}
              </div>
            </div>

            <div className="border-t border-secondary-200 pt-6">
              <h2 className="text-lg font-semibold text-secondary-900 mb-4">Player Settings</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div>
                    <p className="font-medium text-secondary-900">Auto-play Next Lesson</p>
                    <p className="text-sm text-secondary-500">Automatically start the next lesson</p>
                  </div>
                  <button className="text-primary-600">
                    <ToggleRight className="w-8 h-8" />
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div>
                    <p className="font-medium text-secondary-900">Show Captions</p>
                    <p className="text-sm text-secondary-500">Display subtitles on videos</p>
                  </div>
                  <button className="text-primary-600">
                    <ToggleRight className="w-8 h-8" />
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg">
                  <div>
                    <p className="font-medium text-secondary-900">Playback Speed Default</p>
                    <p className="text-sm text-secondary-500">Set default video speed</p>
                  </div>
                  <select className="px-4 py-2 rounded-lg border border-secondary-200 bg-white text-secondary-700 focus:outline-none focus:ring-2 focus:ring-primary-500">
                    <option>0.5x</option>
                    <option>0.75x</option>
                    <option selected>1x</option>
                    <option>1.25x</option>
                    <option>1.5x</option>
                    <option>2x</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        );

      case 'privacy':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-secondary-900 mb-4">Security</h2>
              <div className="space-y-4">
                <button className="w-full flex items-center justify-between p-4 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors">
                  <div className="flex items-center gap-3">
                    <Lock className="w-5 h-5 text-secondary-600" />
                    <div className="text-left">
                      <p className="font-medium text-secondary-900">Change Password</p>
                      <p className="text-sm text-secondary-500">Update your password</p>
                    </div>
                  </div>
                  <ChevronRight className="w-5 h-5 text-secondary-400" />
                </button>

                <button className="w-full flex items-center justify-between p-4 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors">
                  <div className="flex items-center gap-3">
                    <Smartphone className="w-5 h-5 text-secondary-600" />
                    <div className="text-left">
                      <p className="font-medium text-secondary-900">Two-Factor Authentication</p>
                      <p className="text-sm text-secondary-500">Add an extra layer of security</p>
                    </div>
                  </div>
                  <Badge variant="warning">Enable</Badge>
                </button>

                <button className="w-full flex items-center justify-between p-4 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors">
                  <div className="flex items-center gap-3">
                    <Bell className="w-5 h-5 text-secondary-600" />
                    <div className="text-left">
                      <p className="font-medium text-secondary-900">Active Sessions</p>
                      <p className="text-sm text-secondary-500">Manage your active devices</p>
                    </div>
                  </div>
                  <ChevronRight className="w-5 h-5 text-secondary-400" />
                </button>
              </div>
            </div>

            <div className="border-t border-secondary-200 pt-6">
              <h2 className="text-lg font-semibold text-secondary-900 mb-4 text-error-600">Danger Zone</h2>
              <div className="space-y-4">
                <button className="w-full flex items-center justify-between p-4 bg-error-50 rounded-lg hover:bg-error-100 transition-colors">
                  <div className="flex items-center gap-3">
                    <Lock className="w-5 h-5 text-error-600" />
                    <div className="text-left">
                      <p className="font-medium text-error-600">Delete Account</p>
                      <p className="text-sm text-error-500">Permanently delete your account and data</p>
                    </div>
                  </div>
                  <ChevronRight className="w-5 h-5 text-error-400" />
                </button>
              </div>
            </div>
          </div>
        );

      case 'language':
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-secondary-900 mb-4">Language</h2>
              <select className="w-full px-4 py-3 rounded-lg border border-secondary-300 bg-white text-secondary-900 focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option>English (US)</option>
                <option>English (UK)</option>
                <option>Spanish</option>
                <option>French</option>
                <option>German</option>
                <option>Chinese</option>
                <option>Japanese</option>
                <option>Korean</option>
              </select>
            </div>

            <div className="border-t border-secondary-200 pt-6">
              <h2 className="text-lg font-semibold text-secondary-900 mb-4">Regional Format</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="label">Date Format</label>
                  <select className="input">
                    <option>MM/DD/YYYY</option>
                    <option>DD/MM/YYYY</option>
                    <option>YYYY-MM-DD</option>
                  </select>
                </div>
                <div>
                  <label className="label">Time Format</label>
                  <select className="input">
                    <option>12-hour (AM/PM)</option>
                    <option>24-hour</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title">Settings</h1>
        <p className="page-subtitle">Manage your account preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <Card className="lg:col-span-1 h-fit">
          <CardBody className="p-2">
            <nav className="space-y-1">
              {settingSections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                    activeSection === section.id
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-secondary-600 hover:bg-secondary-50'
                  }`}
                >
                  {section.icon}
                  <span className="font-medium">{section.title}</span>
                </button>
              ))}
            </nav>
          </CardBody>
        </Card>

        {/* Content */}
        <Card className="lg:col-span-3">
          <CardHeader className="border-b border-secondary-200">
            <h2 className="section-title">
              {settingSections.find((s) => s.id === activeSection)?.title}
            </h2>
          </CardHeader>
          <CardBody>
            {renderContent()}

            <div className="border-t border-secondary-200 mt-8 pt-6 flex justify-end">
              <Button variant="primary" onClick={handleSave} isLoading={isSaving}>
                Save Changes
              </Button>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
