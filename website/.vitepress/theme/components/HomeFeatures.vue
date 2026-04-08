<script setup lang="ts">
import { computed } from 'vue'
import { Code2, GitBranch, FileText, Wrench, Server, ChevronRight } from 'lucide-vue-next'
import pluginData from '../../../data/plugins.json'

const props = defineProps<{
  lang?: 'ko' | 'en'
}>()

const plugins = pluginData.plugins

const features = computed(() => {
  const lang = props.lang || 'en'
  const countByCategory = (catId: string) => plugins.filter(p => p.category === catId).length

  return [
    {
      icon: Code2,
      catId: 'code-review',
      title: lang === 'ko' ? '코드 리뷰 & 품질' : 'Code Review & Quality',
      details: lang === 'ko' ? 'DRY, KISS, Clean Code 원칙 기반의 자동 코드 리뷰' : 'Automated code review based on DRY, KISS, Clean Code principles',
      count: countByCategory('code-review'),
      browseLabel: lang === 'ko' ? '둘러보기' : 'Browse',
    },
    {
      icon: GitBranch,
      catId: 'workflow',
      title: lang === 'ko' ? '개발 워크플로우' : 'Development Workflow',
      details: lang === 'ko' ? 'Git 커밋, PR 생성, 워킹트리 관리 자동화' : 'Automate Git commits, PR creation, worktree management',
      count: countByCategory('workflow'),
      browseLabel: lang === 'ko' ? '둘러보기' : 'Browse',
    },
    {
      icon: FileText,
      catId: 'specification',
      title: lang === 'ko' ? '사양 & 계획' : 'Specification & Planning',
      details: lang === 'ko' ? 'SDD 워크플로우, 스펙 파일 관리' : 'SDD workflow, spec file management',
      count: countByCategory('specification'),
      browseLabel: lang === 'ko' ? '둘러보기' : 'Browse',
    },
    {
      icon: Wrench,
      catId: 'utility',
      title: lang === 'ko' ? '유틸리티' : 'Utilities',
      details: lang === 'ko' ? '세션 리포트, 알림, 에이전트 팀 관리 등' : 'Session reports, notifications, agent team management, and more',
      count: countByCategory('utility'),
      browseLabel: lang === 'ko' ? '둘러보기' : 'Browse',
    },
    {
      icon: Server,
      catId: 'infrastructure',
      title: lang === 'ko' ? '인프라' : 'Infrastructure',
      details: lang === 'ko' ? '공유 MCP 서버 및 도구 통합' : 'Shared MCP servers and tool integrations',
      count: countByCategory('infrastructure'),
      browseLabel: lang === 'ko' ? '둘러보기' : 'Browse',
    }
  ]
})

const getPluginPagePath = (catId: string) => {
  const base = props.lang === 'ko' ? '/ko/plugins/' : '/en/plugins/'
  return `${base}?category=${catId}`
}

const sectionTitle = computed(() =>
  props.lang === 'ko' ? '플러그인으로 무엇을 할 수 있나요?' : 'What can plugins do?'
)
</script>

<template>
  <div class="home-features">
    <h2 class="features-section-title">{{ sectionTitle }}</h2>
    <div class="features-container">
      <a
        v-for="feature in features"
        :key="feature.catId"
        :href="getPluginPagePath(feature.catId)"
        class="feature-card"
        :data-cat="feature.catId"
      >
        <div class="feature-icon" :data-cat="feature.catId">
          <component :is="feature.icon" :size="26" />
        </div>
        <div class="feature-header">
          <h3 class="feature-title">{{ feature.title }}</h3>
          <span class="feature-count">{{ feature.count }}</span>
        </div>
        <p class="feature-details">{{ feature.details }}</p>
        <span class="feature-link">
          {{ feature.browseLabel }}
          <ChevronRight :size="14" />
        </span>
      </a>
    </div>
  </div>
</template>
