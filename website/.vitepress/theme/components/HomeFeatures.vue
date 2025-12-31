<script setup lang="ts">
import { Code2, GitBranch, FileText, Wrench } from 'lucide-vue-next'

const props = defineProps<{
  lang?: 'ko' | 'en'
}>()

const features = {
  ko: [
    {
      icon: Code2,
      title: '코드 리뷰 & 품질',
      details: 'DRY, KISS, Clean Code 원칙 기반의 자동 코드 리뷰'
    },
    {
      icon: GitBranch,
      title: '개발 워크플로우',
      details: 'Git 커밋, PR 생성, 워킹트리 관리 자동화'
    },
    {
      icon: FileText,
      title: '사양 & 계획',
      details: 'SDD 워크플로우, 스펙 파일 관리'
    },
    {
      icon: Wrench,
      title: '유틸리티',
      details: '세션 리포트, 알림 등 편의 기능'
    }
  ],
  en: [
    {
      icon: Code2,
      title: 'Code Review & Quality',
      details: 'Automated code review based on DRY, KISS, Clean Code principles'
    },
    {
      icon: GitBranch,
      title: 'Development Workflow',
      details: 'Automate Git commits, PR creation, worktree management'
    },
    {
      icon: FileText,
      title: 'Specification & Planning',
      details: 'SDD workflow, spec file management'
    },
    {
      icon: Wrench,
      title: 'Utilities',
      details: 'Session reports, notifications, and more'
    }
  ]
}

const currentFeatures = props.lang === 'en' ? features.en : features.ko
</script>

<template>
  <div class="home-features">
    <div class="features-container">
      <div v-for="(feature, index) in currentFeatures" :key="index" class="feature-card">
        <div class="feature-icon">
          <component :is="feature.icon" :size="24" />
        </div>
        <h3 class="feature-title">{{ feature.title }}</h3>
        <p class="feature-details">{{ feature.details }}</p>
      </div>
    </div>
  </div>
</template>
