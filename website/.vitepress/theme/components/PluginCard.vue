<script setup lang="ts">
import { ref } from 'vue'
import {
  Code2,
  GitBranch,
  FileText,
  Wrench,
  Server,
  Brain,
  Terminal,
  Webhook,
  Plug,
  Copy,
  ExternalLink,
  Check
} from 'lucide-vue-next'

interface Plugin {
  id: string
  name: string
  version: string
  description: string
  author: string
  category: string
  components: {
    skills: string[]
    commands: string[]
    hooks: boolean
    mcpServers: string[]
  }
  features: string[]
  installCommand: string
  uninstallCommand: string
}

const props = defineProps<{
  plugin: Plugin
  lang?: 'ko' | 'en'
  view?: 'card' | 'list'
}>()

const copied = ref(false)

const categoryNames = {
  'code-review': { ko: '코드 리뷰', en: 'Code Review' },
  'workflow': { ko: '워크플로우', en: 'Workflow' },
  'specification': { ko: '사양 & 계획', en: 'Specification' },
  'utility': { ko: '유틸리티', en: 'Utility' },
  'infrastructure': { ko: '인프라', en: 'Infrastructure' }
}

const copyInstallCommand = async () => {
  try {
    await navigator.clipboard.writeText(props.plugin.installCommand)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}

const getCategoryName = (categoryId: string) => {
  const lang = props.lang || 'en'
  return categoryNames[categoryId]?.[lang] || categoryId
}

const getCategoryIcon = (categoryId: string) => {
  const icons = {
    'code-review': Code2,
    'workflow': GitBranch,
    'specification': FileText,
    'utility': Wrench,
    'infrastructure': Server
  }
  return icons[categoryId] || Wrench
}
</script>

<template>
  <!-- Card View -->
  <article v-if="view !== 'list'" class="plugin-card">
    <div class="plugin-card-header">
      <div class="plugin-card-meta">
        <span class="plugin-card-category">
          <component :is="getCategoryIcon(plugin.category)" :size="16" />
        </span>
        <span class="plugin-card-version">v{{ plugin.version }}</span>
      </div>
    </div>

    <div class="plugin-card-content">
      <h3 class="plugin-card-title">{{ plugin.name }}</h3>
      <p class="plugin-card-description">{{ plugin.description }}</p>
    </div>

    <ul v-if="plugin.features.length > 0" class="plugin-card-features">
      <li v-for="feature in plugin.features.slice(0, 3)" :key="feature">
        <span class="feature-bullet"></span>
        {{ feature }}
      </li>
    </ul>

    <div class="plugin-card-badges">
      <span v-if="plugin.components.skills.length > 0" class="badge badge-skill">
        <Brain :size="12" />
        Skills ({{ plugin.components.skills.length }})
      </span>
      <span v-if="plugin.components.commands.length > 0" class="badge badge-command">
        <Terminal :size="12" />
        Commands ({{ plugin.components.commands.length }})
      </span>
      <span v-if="plugin.components.hooks" class="badge badge-hook">
        <Webhook :size="12" />
        Hooks
      </span>
      <span v-if="plugin.components.mcpServers.length > 0" class="badge badge-mcp">
        <Plug :size="12" />
        MCP ({{ plugin.components.mcpServers.length }})
      </span>
    </div>

    <div class="plugin-card-actions">
      <button class="btn btn-primary" @click="copyInstallCommand">
        <Copy v-if="!copied" :size="14" />
        <Check v-else :size="14" />
        {{ copied ? (lang === 'en' ? 'Copied!' : '복사됨!') : (lang === 'en' ? 'Install' : '설치') }}
      </button>
      <a :href="`https://github.com/devstefancho/claude-plugins/tree/main/${plugin.id}`" target="_blank" class="btn btn-ghost">
        {{ lang === 'en' ? 'Details' : '상세' }}
        <ExternalLink :size="14" />
      </a>
    </div>
  </article>

  <!-- List View -->
  <article v-else class="plugin-card plugin-card-list">
    <!-- Left: Icon -->
    <span class="plugin-list-icon">
      <component :is="getCategoryIcon(plugin.category)" :size="18" />
    </span>

    <!-- Center: Main content -->
    <div class="plugin-list-main">
      <div class="plugin-list-title-row">
        <h3 class="plugin-card-title">{{ plugin.name }}</h3>
        <span class="plugin-card-version">v{{ plugin.version }}</span>
      </div>
      <p class="plugin-card-description">{{ plugin.description }}</p>
    </div>

    <!-- Right: Badges + Actions -->
    <div class="plugin-list-right">
      <div class="plugin-card-badges">
        <span v-if="plugin.components.skills.length > 0" class="badge badge-skill">
          <Brain :size="12" />
          {{ plugin.components.skills.length }}
        </span>
        <span v-if="plugin.components.commands.length > 0" class="badge badge-command">
          <Terminal :size="12" />
          {{ plugin.components.commands.length }}
        </span>
        <span v-if="plugin.components.hooks" class="badge badge-hook">
          <Webhook :size="12" />
        </span>
        <span v-if="plugin.components.mcpServers.length > 0" class="badge badge-mcp">
          <Plug :size="12" />
          {{ plugin.components.mcpServers.length }}
        </span>
      </div>
      <div class="plugin-card-actions">
        <button class="btn btn-primary btn-sm" @click="copyInstallCommand">
          <Copy v-if="!copied" :size="14" />
          <Check v-else :size="14" />
          {{ copied ? (lang === 'en' ? 'Copied!' : '복사됨!') : (lang === 'en' ? 'Install' : '설치') }}
        </button>
        <a :href="`https://github.com/devstefancho/claude-plugins/tree/main/${plugin.id}`" target="_blank" class="btn btn-ghost btn-sm">
          {{ lang === 'en' ? 'Details' : '상세' }}
          <ExternalLink :size="14" />
        </a>
      </div>
    </div>
  </article>
</template>
