import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const rootDir = path.join(__dirname, '..')

// 카테고리 매핑
const categoryMapping = {
  'code-style-plugin': 'code-review',
  'code-quality-plugin': 'code-review',
  'scaffold-claude-feature': 'code-review',
  'git-commit-plugin': 'workflow',
  'pr-create-plugin': 'workflow',
  'git-worktree-plugin': 'workflow',
  'simple-sdd-plugin': 'specification',
  'spec-manager-plugin': 'specification',
  'session-reporter-plugin': 'utility',
  'stop-notification-plugin': 'utility',
  'worktrace-plugin': 'utility',
  'frontend-plugin': 'code-review',
  'smart-commit-plugin': 'workflow',
  'test-commit-push-pr-clean-plugin': 'workflow',
  'common-mcp-plugin': 'infrastructure'
}

const categories = {
  'code-review': {
    id: 'code-review',
    name: { ko: '코드 리뷰 & 품질', en: 'Code Review & Quality' },
    icon: '🎨'
  },
  'workflow': {
    id: 'workflow',
    name: { ko: '개발 워크플로우', en: 'Development Workflow' },
    icon: '🔄'
  },
  'specification': {
    id: 'specification',
    name: { ko: '사양 & 계획', en: 'Specification & Planning' },
    icon: '📋'
  },
  'utility': {
    id: 'utility',
    name: { ko: '유틸리티', en: 'Utilities' },
    icon: '🛠️'
  },
  'infrastructure': {
    id: 'infrastructure',
    name: { ko: '인프라', en: 'Infrastructure' },
    icon: '🏗️'
  }
}

function getPluginDirectories() {
  const items = fs.readdirSync(rootDir)
  const pluginDirs = []

  for (const item of items) {
    const itemPath = path.join(rootDir, item)
    const pluginJsonPath = path.join(itemPath, '.claude-plugin', 'plugin.json')

    if (fs.statSync(itemPath).isDirectory() && fs.existsSync(pluginJsonPath)) {
      pluginDirs.push(item)
    }
  }

  return pluginDirs
}

function parsePluginJson(pluginDir) {
  const pluginJsonPath = path.join(rootDir, pluginDir, '.claude-plugin', 'plugin.json')
  const content = fs.readFileSync(pluginJsonPath, 'utf-8')
  return JSON.parse(content)
}

function getComponents(pluginDir) {
  const components = {
    skills: [],
    commands: [],
    hooks: false,
    mcpServers: []
  }

  const pluginPath = path.join(rootDir, pluginDir)

  // Check for skills
  const skillsDir = path.join(pluginPath, 'skills')
  if (fs.existsSync(skillsDir)) {
    const skillItems = fs.readdirSync(skillsDir)
    for (const item of skillItems) {
      const skillPath = path.join(skillsDir, item)
      if (fs.statSync(skillPath).isDirectory() &&
          fs.existsSync(path.join(skillPath, 'SKILL.md'))) {
        components.skills.push(item)
      }
    }
  }

  // Check for commands
  const commandsDir = path.join(pluginPath, 'commands')
  if (fs.existsSync(commandsDir)) {
    const cmdFiles = fs.readdirSync(commandsDir).filter(f => f.endsWith('.md'))
    components.commands = cmdFiles.map(f => f.replace('.md', ''))
  }

  // Check for hooks
  const hooksPath = path.join(pluginPath, 'hooks', 'hooks.json')
  if (fs.existsSync(hooksPath)) {
    components.hooks = true
  }

  // Check for MCP servers
  const mcpPath = path.join(pluginPath, '.mcp.json')
  if (fs.existsSync(mcpPath)) {
    try {
      const mcpContent = fs.readFileSync(mcpPath, 'utf-8')
      const mcpConfig = JSON.parse(mcpContent)
      if (mcpConfig.mcpServers) {
        components.mcpServers = Object.keys(mcpConfig.mcpServers)
      }
    } catch (e) {
      console.error(`Error parsing MCP config for ${pluginDir}:`, e)
    }
  }

  return components
}

function extractFeatures(pluginDir) {
  const readmePath = path.join(rootDir, pluginDir, 'README.md')
  const features = []

  if (!fs.existsSync(readmePath)) {
    return features
  }

  const content = fs.readFileSync(readmePath, 'utf-8')
  const lines = content.split('\n')

  // 기능 섹션 찾기
  let inFeatureSection = false
  for (const line of lines) {
    // 기능, Features, 주요 기능 등의 헤더 찾기
    if (line.match(/^#+\s*(기능|Features?|주요\s*기능|핵심\s*기능)/i)) {
      inFeatureSection = true
      continue
    }

    // 다른 헤더를 만나면 종료
    if (inFeatureSection && line.match(/^#+\s/)) {
      break
    }

    // 체크마크나 불릿 포인트 찾기
    if (inFeatureSection) {
      const match = line.match(/^[\s]*[-*✅•]\s*\*?\*?(.+?)\*?\*?\s*$/)
      if (match && match[1].trim()) {
        const feature = match[1].trim()
          .replace(/\*\*/g, '')
          .replace(/`/g, '')
        if (feature.length > 0 && feature.length < 100) {
          features.push(feature)
        }
      }
    }

    // 최대 5개까지만
    if (features.length >= 5) break
  }

  return features
}

function generatePluginData() {
  const pluginDirs = getPluginDirectories()
  const plugins = []

  for (const dir of pluginDirs) {
    try {
      const metadata = parsePluginJson(dir)
      const components = getComponents(dir)
      const features = extractFeatures(dir)
      const categoryId = categoryMapping[dir] || 'utility'

      plugins.push({
        id: dir,
        name: metadata.name || dir,
        version: metadata.version || '1.0.0',
        description: metadata.description || '',
        author: typeof metadata.author === 'object' ? metadata.author.name : (metadata.author || 'Unknown'),
        category: categoryId,
        components,
        features,
        installCommand: `/plugin install ${dir}@devstefancho-claude-plugins`,
        uninstallCommand: `/plugin uninstall ${dir}@devstefancho-claude-plugins`,
        readmePath: `${dir}/README.md`,
        hasReadme: fs.existsSync(path.join(rootDir, dir, 'README.md'))
      })
    } catch (e) {
      console.error(`Error processing plugin ${dir}:`, e)
    }
  }

  // 이름순 정렬
  plugins.sort((a, b) => a.name.localeCompare(b.name))

  const data = {
    marketplace: {
      name: 'devstefancho-claude-plugins',
      repo: 'devstefancho/claude-plugins',
      installCommand: '/plugin marketplace add devstefancho/claude-plugins'
    },
    plugins,
    categories: Object.values(categories)
  }

  // Write to website/data
  const outputPath = path.join(rootDir, 'website', 'data', 'plugins.json')
  fs.writeFileSync(outputPath, JSON.stringify(data, null, 2))

  console.log(`Generated plugin data for ${plugins.length} plugins`)
  console.log(`Output: ${outputPath}`)
}

generatePluginData()
