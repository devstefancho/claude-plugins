import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Claude Plugins',
  description: 'Claude Code Plugin Marketplace',

  locales: {
    root: {
      label: 'English',
      lang: 'en',
      themeConfig: {
        nav: [
          { text: 'Home', link: '/' },
          { text: 'Plugins', link: '/plugins/' },
          { text: 'Guide', link: '/guide/getting-started' }
        ],
        sidebar: {
          '/guide/': [
            {
              text: 'Getting Started',
              items: [
                { text: 'Introduction', link: '/guide/getting-started' },
                { text: 'Installation', link: '/guide/installation' }
              ]
            }
          ],
          '/plugins/': [
            {
              text: 'Plugins',
              items: [
                { text: 'All Plugins', link: '/plugins/' }
              ]
            }
          ]
        }
      }
    },
    ko: {
      label: '한국어',
      lang: 'ko',
      link: '/ko/',
      themeConfig: {
        nav: [
          { text: '홈', link: '/ko/' },
          { text: '플러그인', link: '/ko/plugins/' },
          { text: '가이드', link: '/ko/guide/getting-started' }
        ],
        sidebar: {
          '/ko/guide/': [
            {
              text: '시작하기',
              items: [
                { text: '소개', link: '/ko/guide/getting-started' },
                { text: '설치 방법', link: '/ko/guide/installation' }
              ]
            }
          ],
          '/ko/plugins/': [
            {
              text: '플러그인',
              items: [
                { text: '전체 목록', link: '/ko/plugins/' }
              ]
            }
          ]
        },
        outline: {
          label: '목차'
        },
        docFooter: {
          prev: '이전',
          next: '다음'
        }
      }
    }
  },

  themeConfig: {
    logo: '/logo.svg',

    socialLinks: [
      { icon: 'github', link: 'https://github.com/devstefancho/claude-plugins' }
    ],

    search: {
      provider: 'local'
    },

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024 devstefancho'
    }
  },

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],

  markdown: {
    lineNumbers: true
  }
})
