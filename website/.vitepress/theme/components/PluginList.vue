<script setup lang="ts">
import { ref, computed } from 'vue'
import pluginData from '../../../data/plugins.json'

const props = defineProps<{
  lang?: 'ko' | 'en'
}>()

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

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedComponent = ref('')

const categories = pluginData.categories
const plugins = pluginData.plugins as Plugin[]

const categoryNames = {
  'code-review': { ko: '코드 리뷰 & 품질', en: 'Code Review & Quality' },
  'workflow': { ko: '개발 워크플로우', en: 'Development Workflow' },
  'specification': { ko: '사양 & 계획', en: 'Specification & Planning' },
  'utility': { ko: '유틸리티', en: 'Utilities' },
  'infrastructure': { ko: '인프라', en: 'Infrastructure' }
}

const filteredPlugins = computed(() => {
  return plugins.filter(plugin => {
    // Search filter
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      const matchesSearch =
        plugin.name.toLowerCase().includes(query) ||
        plugin.description.toLowerCase().includes(query) ||
        plugin.features.some(f => f.toLowerCase().includes(query))
      if (!matchesSearch) return false
    }

    // Category filter
    if (selectedCategory.value && plugin.category !== selectedCategory.value) {
      return false
    }

    // Component filter
    if (selectedComponent.value) {
      switch (selectedComponent.value) {
        case 'skills':
          if (plugin.components.skills.length === 0) return false
          break
        case 'commands':
          if (plugin.components.commands.length === 0) return false
          break
        case 'hooks':
          if (!plugin.components.hooks) return false
          break
        case 'mcp':
          if (plugin.components.mcpServers.length === 0) return false
          break
      }
    }

    return true
  })
})

const getCategoryLabel = (categoryId: string) => {
  const lang = props.lang || 'ko'
  return categoryNames[categoryId]?.[lang] || categoryId
}

const labels = computed(() => {
  const lang = props.lang || 'ko'
  return {
    searchPlaceholder: lang === 'ko' ? '플러그인 검색...' : 'Search plugins...',
    allCategories: lang === 'ko' ? '모든 카테고리' : 'All Categories',
    allComponents: lang === 'ko' ? '모든 컴포넌트' : 'All Components',
    pluginCount: lang === 'ko'
      ? `총 ${filteredPlugins.value.length}개의 플러그인`
      : `${filteredPlugins.value.length} plugins found`
  }
})
</script>

<template>
  <div class="plugin-list">
    <div class="plugin-list-filters">
      <input
        type="text"
        v-model="searchQuery"
        :placeholder="labels.searchPlaceholder"
      />

      <select v-model="selectedCategory">
        <option value="">{{ labels.allCategories }}</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ getCategoryLabel(cat.id) }}
        </option>
      </select>

      <select v-model="selectedComponent">
        <option value="">{{ labels.allComponents }}</option>
        <option value="skills">Skills</option>
        <option value="commands">Commands</option>
        <option value="hooks">Hooks</option>
        <option value="mcp">MCP Servers</option>
      </select>
    </div>

    <p class="plugin-count">{{ labels.pluginCount }}</p>

    <div class="plugin-grid">
      <PluginCard
        v-for="plugin in filteredPlugins"
        :key="plugin.id"
        :plugin="plugin"
        :lang="lang"
      />
    </div>
  </div>
</template>
