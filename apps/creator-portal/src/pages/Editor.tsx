import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { contentApi, syllabusApi } from '../services/api'

export default function Editor() {
  const { contentId } = useParams()
  const isEditing = Boolean(contentId)
  
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [platform, setPlatform] = useState('mathverse')
  const [difficulty, setDifficulty] = useState('beginner')
  const [isPremium, setIsPremium] = useState(false)
  const [animationScript, setAnimationScript] = useState('')
  const [syllabus, setSyllabus] = useState('')
  const [saving, setSaving] = useState(false)
  const [previewing, setPreviewing] = useState(false)
  
  const platforms = [
    { value: 'mathverse', label: 'MathVerse' },
    { value: 'physicsverse', label: 'PhysicsVerse' },
    { value: 'chemverse', label: 'ChemVerse' },
    { value: 'algverse', label: 'AlgoVerse' },
    { value: 'finverse', label: 'FinVerse' },
  ]
  
  const difficulties = [
    { value: 'beginner', label: 'Beginner' },
    { value: 'intermediate', label: 'Intermediate' },
    { value: 'advanced', label: 'Advanced' },
    { value: 'expert', label: 'Expert' },
  ]
  
  const sampleScript = `# Create a simple animation showing a circle growing
from manim import *

class GrowingCircle(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        self.add(circle)
        self.play(ApplyMethod(circle.scale, 2))
        self.wait(1)
`
  
  const handleSave = async () => {
    if (!title.trim()) {
      alert('Please enter a title')
      return
    }
    
    setSaving(true)
    try {
      const data = {
        title,
        description,
        platform,
        difficulty,
        is_premium: isPremium,
        animation_script: animationScript || sampleScript,
      }
      
      if (isEditing) {
        await contentApi.update(parseInt(contentId), data)
      } else {
        await contentApi.create(data)
      }
      
      alert('Content saved successfully!')
    } catch (error) {
      console.error('Save error:', error)
      alert('Failed to save content')
    } finally {
      setSaving(false)
    }
  }
  
  const handlePreview = async () => {
    setPreviewing(true)
    // Preview logic would be implemented here
    setTimeout(() => {
      setPreviewing(false)
      alert('Preview feature requires Manim integration')
    }, 1000)
  }
  
  const handleSubmitForReview = async () => {
    await handleSave()
    alert('Content submitted for moderation review')
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {isEditing ? 'Edit Content' : 'Create New Content'}
          </h1>
          <p className="text-gray-600 mt-1">
            {isEditing ? 'Update your animation content' : 'Create educational animations with Manim'}
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handlePreview}
            disabled={previewing}
            className="btn-secondary"
          >
            {previewing ? 'Loading...' : 'Preview'}
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="btn-secondary"
          >
            {saving ? 'Saving...' : 'Save Draft'}
          </button>
          <button
            onClick={handleSubmitForReview}
            className="btn-primary"
          >
            Submit for Review
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column - Content settings */}
        <div className="space-y-6">
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Content Details</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Title
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="input"
                  placeholder="Enter content title"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="input"
                  rows={3}
                  placeholder="Brief description of the content"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Platform
                </label>
                <select
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value)}
                  className="input"
                >
                  {platforms.map((p) => (
                    <option key={p.value} value={p.value}>
                      {p.label}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Difficulty
                </label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="input"
                >
                  {difficulties.map((d) => (
                    <option key={d.value} value={d.value}>
                      {d.label}
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="premium"
                  checked={isPremium}
                  onChange={(e) => setIsPremium(e.target.checked)}
                  className="w-4 h-4 text-primary-600 rounded"
                />
                <label htmlFor="premium" className="text-sm text-gray-700">
                  Premium content (requires license)
                </label>
              </div>
            </div>
          </div>
          
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Syllabus Tagging</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Syllabi
              </label>
              <select className="input" value={syllabus} onChange={(e) => setSyllabus(e.target.value)}>
                <option value="">Select a syllabus</option>
                <option value="1">High School Mathematics</option>
                <option value="2">IIT JEE Preparation</option>
                <option value="3">Undergraduate Physics</option>
              </select>
            </div>
          </div>
        </div>
        
        {/* Right column - Code editor */}
        <div className="lg:col-span-2">
          <div className="card h-full">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Animation Script</h2>
              <div className="flex gap-2">
                <button
                  onClick={() => setAnimationScript(sampleScript)}
                  className="text-sm text-primary-600 hover:text-primary-700"
                >
                  Load Sample
                </button>
              </div>
            </div>
            
            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <div className="bg-gray-900 text-gray-300 px-4 py-2 text-sm font-mono border-b border-gray-700">
                animation_script.py
              </div>
              <textarea
                value={animationScript}
                onChange={(e) => setAnimationScript(e.target.value)}
                className="w-full h-96 p-4 font-mono text-sm bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="# Write your Manim animation script here...
from manim import *

class MyAnimation(Scene):
    def construct(self):
        # Your code here
        pass
"
                spellCheck={false}
              />
            </div>
            
            <p className="mt-4 text-sm text-gray-500">
              Write Manim Python code to create animations. The script will be rendered using Manim Community Edition.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
