import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

// https://vitepress.dev/reference/site-config
let config = defineConfig({
  base: "/",
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
    outline: {
      level: [2, 4]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/timerring/bilitool' }
    ]
  },
    // optionally, you can pass MermaidConfig
    mermaid: {
      // refer for options:
      // https://mermaid.js.org/config/setup/modules/mermaidAPI.html#mermaidapi-configuration-defaults
    },
    // optionally set additional config for plugin itself with MermaidPluginConfig
    mermaidPlugin: {
      // set additional css class for mermaid container
      class: "mermaid"
    }
})

config = withMermaid(config) 

export default config