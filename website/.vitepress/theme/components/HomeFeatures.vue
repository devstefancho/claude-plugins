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
          <component :is="feature.icon" :size="32" />
        </div>
        <h3 class="feature-title">{{ feature.title }}</h3>
        <p class="feature-details">{{ feature.details }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-features {
  padding: 2rem 0 4rem;
  max-width: 1152px;
  margin: 0 auto;
}

.features-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  padding: 0 24px;
}

.feature-card {
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
  padding: 24px;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 48px;
  height: 48px;
  background: var(--vp-c-brand-soft);
  border-radius: 8px;
  color: var(--vp-c-brand-1);
  margin-bottom: 16px;
}

.feature-title {
  font-size: 1.1em;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 8px 0;
}

.feature-details {
  font-size: 0.95em;
  color: var(--vp-c-text-2);
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 768px) {
  .features-container {
    grid-template-columns: 1fr;
  }
}
</style>
