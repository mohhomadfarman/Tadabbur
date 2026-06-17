import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { progressApi } from '@/api/progress'

export const useProgressStore = defineStore('progress', () => {
  const completedLessons = ref(new Set())
  const enrolledTracks = ref([])
  const currentStreak = ref(0)
  const longestStreak = ref(0)
  const totalCompleted = ref(0)
  const continueLesson = ref(null)
  const lastActivity = ref(null)

  const trackProgressCache = ref({})

  const loaded = ref(false)
  const marking = ref(false)
  const enrolling = ref(false)

  async function fetchProgress() {
    if (loaded.value) return
    try {
      const data = await progressApi.getProgress()
      completedLessons.value = new Set(data.completed_lessons)
      totalCompleted.value = data.total_lessons_completed
      enrolledTracks.value = data.enrolled_tracks || []
      currentStreak.value = data.current_streak_days || 0
      longestStreak.value = data.longest_streak_days || 0
      continueLesson.value = data.continue_learning || null
      lastActivity.value = data.last_activity || null
      loaded.value = true
    } catch {
      // unauthenticated or network error — stay empty
    }
  }

  async function markComplete(slug) {
    if (marking.value) return
    marking.value = true
    try {
      await progressApi.markComplete(slug)
      completedLessons.value.add(slug)
      totalCompleted.value++
      // Refresh full progress to get updated streak and continue-learning
      loaded.value = false
      await fetchProgress()
    } finally {
      marking.value = false
    }
  }

  async function enrollTrack(trackSlug) {
    if (enrolling.value) return
    enrolling.value = true
    try {
      await progressApi.enrollTrack(trackSlug)
      if (!enrolledTracks.value.includes(trackSlug)) {
        enrolledTracks.value.push(trackSlug)
      }
    } finally {
      enrolling.value = false
    }
  }

  async function unenrollTrack(trackSlug) {
    await progressApi.unenrollTrack(trackSlug)
    enrolledTracks.value = enrolledTracks.value.filter(s => s !== trackSlug)
    delete trackProgressCache.value[trackSlug]
  }

  async function fetchTrackProgress(trackSlug) {
    if (trackProgressCache.value[trackSlug]) return trackProgressCache.value[trackSlug]
    try {
      const data = await progressApi.getTrackProgress(trackSlug)
      trackProgressCache.value[trackSlug] = data
      return data
    } catch {
      return null
    }
  }

  function isCompleted(slug) {
    return completedLessons.value.has(slug)
  }

  function isEnrolled(trackSlug) {
    return enrolledTracks.value.includes(trackSlug)
  }

  function reset() {
    completedLessons.value = new Set()
    enrolledTracks.value = []
    currentStreak.value = 0
    longestStreak.value = 0
    totalCompleted.value = 0
    continueLesson.value = null
    lastActivity.value = null
    trackProgressCache.value = {}
    loaded.value = false
  }

  return {
    completedLessons,
    enrolledTracks,
    currentStreak,
    longestStreak,
    totalCompleted,
    continueLesson,
    lastActivity,
    trackProgressCache,
    loaded,
    marking,
    enrolling,
    fetchProgress,
    markComplete,
    enrollTrack,
    unenrollTrack,
    fetchTrackProgress,
    isCompleted,
    isEnrolled,
    reset,
  }
})
