import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "bilitool",
  description: "Official documentation",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/getting-start' }
    ],

    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Getting Started', link: '/getting-start' },
          { text: 'Installation', link: '/installation' },
          { text: 'Login', link: '/login' },
          { text: 'Check', link: '/check' },
          { text: 'Logout', link: '/logout' },
          { text: 'Upload', link: '/upload' },
          { text: 'Download', link: '/download' },
          { text: 'List', link: '/list' },
          { text: 'Show', link: '/show' },
          { text: 'Convert', link: '/convert' },
          { text: 'IP', link: '/ip' },
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/timerring/bilitool' }
    ]
  }
})
