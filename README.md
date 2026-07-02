# ProtheusQuiz — PWA

Quiz gamificado para dominar as 100 tabelas do TOTVS Protheus, agora como **app instalável (PWA)**, com 3 temas: **Preto**, **Noite** e **Branco**.

Site estático puro — sem build, sem dependências de servidor. Roda direto no navegador e pode ser "baixado" (instalado) como app no celular ou no computador.

## Estrutura do projeto

```
.
├── index.html              # App completo (HTML + CSS + JS)
├── manifest.json           # Manifesto PWA (nome, ícones, cores)
├── sw.js                   # Service worker (cache offline)
├── icons/                  # Ícones do app (192, 512, maskable, apple-touch)
├── vercel.json             # Configuração de headers para a Vercel
├── package.json            # Scripts auxiliares (dev local)
└── .gitignore
```

## Rodando localmente

```bash
npm run dev
```

Isso sobe um servidor estático em `http://localhost:3000`. **Importante:** o service worker só é registrado em `localhost` ou HTTPS — abrir o `index.html` direto com `file://` não instala o app.

## Publicando no GitHub

```bash
git init
git add .
git commit -m "ProtheusQuiz PWA: temas preto/noite/branco + instalação como app"
git branch -M main
git remote add origin <URL_DO_SEU_REPOSITORIO>
git push -u origin main
```

## Deploy na Vercel

### Opção 1 — CLI

```bash
npm i -g vercel
vercel login
vercel          # deploy de preview
vercel --prod   # deploy de produção
```

### Opção 2 — Dashboard

1. Acesse [vercel.com/new](https://vercel.com/new) e importe o repositório do GitHub.
2. Framework preset: **Other** (site estático, sem build command).
3. Build Command: deixe em branco. Output Directory: `.` (raiz).
4. Deploy.

Depois do deploy, a Vercel gera automaticamente HTTPS — requisito para o app poder ser instalado (PWA).

## Como "instalar" o app

- **Android/Chrome/Edge:** ao abrir o site, aparece o botão **"⬇ Instalar app"** no cabeçalho, ou o menu do navegador oferece "Instalar app" / "Adicionar à tela inicial".
- **iPhone/Safari:** toque em Compartilhar → **Adicionar à Tela de Início** (o iOS não expõe o prompt automático de instalação).
- **Desktop (Chrome/Edge):** ícone de instalação na barra de endereço, ou o botão no cabeçalho.

## Temas

O seletor de tema fica no cabeçalho (três bolinhas: preto / azul-escuro / branco). A escolha é salva no `localStorage` e é reaplicada automaticamente na próxima visita, inclusive quando o app está instalado.

## Regenerando os ícones (opcional)

Os ícones em `icons/` foram gerados com `gen_icons.py` (requer Pillow: `pip install pillow`). Rode `python3 gen_icons.py` para recriá-los se quiser mudar as cores/tamanhos.
