This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `src/app/page.tsx`. The page auto-updates as you edit the file.

## Local commands

From the `nextjs/` directory:

| Command | Description |
|---------|-------------|
| `make dev` | Start the dev server (`npm run dev`) using the project `.npmrc` |
| `make lint` | Run ESLint |
| `make build` | Build the Docker image (`nextjs-hello`) |
| `make up` | Start the app with Docker Compose (reads `nextjs/.env.local`) |
| `make up-build` | Build the image and start Compose (reads `nextjs/.env.local`) |
| `make down` | Stop Compose containers |
| `make logs` | Follow Compose logs |

Equivalent without Make:

```bash
npm run dev
npm run lint
npm run build
npm start   # after npm run build
```

## Installing packages later

This project uses **`nextjs/.npmrc`** to install from the public npm registry (`https://registry.npmjs.org/`), not your global `~/.npmrc` (e.g. a private Nexus mirror).

When adding dependencies, run install from `nextjs/` with the project config:

```bash
NPM_CONFIG_USERCONFIG="$(pwd)/.npmrc" npm install <package>
```

Examples:

```bash
NPM_CONFIG_USERCONFIG="$(pwd)/.npmrc" npm install lodash
NPM_CONFIG_USERCONFIG="$(pwd)/.npmrc" npm install -D @types/lodash
```

Or use Make for dev/lint (which already sets the same env vars):

```bash
make dev
```

Commit the updated `package.json` and `package-lock.json` after installing. Docker builds copy `.npmrc` and use the public registry as well.

## Docker and `.env.local`

Create `nextjs/.env.local` from the template (same file as local dev):

```bash
cp .env.example .env.local
# set GEMINI_API_KEY=...
```

`docker compose` loads **`nextjs/.env.local`** into the container via `env_file` (see `docker-compose.yml`). You do not need to pass `GEMINI_API_KEY` on the command line.

```bash
make up-build
```

If `.env.local` is missing, Compose still starts; set `GEMINI_API_KEY` there before using Translate.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
