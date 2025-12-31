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
  const lang = props.lang || 'ko'
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
  <div class="plugin-card">
    <div class="plugin-card-header">
      <h3 class="plugin-card-title">{{ plugin.name }}</h3>
      <span class="plugin-card-version">v{{ plugin.version }}</span>
    </div>

    <p class="plugin-card-description">{{ plugin.description }}</p>

    <ul v-if="plugin.features.length > 0" class="plugin-card-features">
      <li v-for="feature in plugin.features.slice(0, 3)" :key="feature">
        {{ feature }}
      </li>
    </ul>

    <div class="plugin-card-badges">
      <span v-if="plugin.components.skills.length > 0" class="badge badge-skill">
        <Brain :size="14" />
        Skills ({{ plugin.components.skills.length }})
      </span>
      <span v-if="plugin.components.commands.length > 0" class="badge badge-command">
        <Terminal :size="14" />
        Commands ({{ plugin.components.commands.length }})
      </span>
      <span v-if="plugin.components.hooks" class="badge badge-hook">
        <Webhook :size="14" />
        Hooks
      </span>
      <span v-if="plugin.components.mcpServers.length > 0" class="badge badge-mcp">
        <Plug :size="14" />
        MCP ({{ plugin.components.mcpServers.length }})
      </span>
      <span class="badge badge-category">
        <component :is="getCategoryIcon(plugin.category)" :size="14" />
        {{ getCategoryName(plugin.category) }}
      </span>
    </div>

    <div class="plugin-card-actions">
      <button class="btn btn-primary" @click="copyInstallCommand">
        <Copy v-if="!copied" :size="16" />
        <Check v-else :size="16" />
        {{ lang === 'en' ? 'Copy' : '복사' }}
      </button>
      <a :href="`https://github.com/devstefancho/claude-plugins/tree/main/${plugin.id}`" target="_blank" class="btn btn-outline">
        <ExternalLink :size="16" />
        {{ lang === 'en' ? 'Details' : '상세' }}
      </a>
    </div>
  </div>
</template>
