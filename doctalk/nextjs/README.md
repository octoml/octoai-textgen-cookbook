# DocTalk Demo 🦙

A Next.js-based demo showcasing Llama2 using various docs sources. It utilizes the [OctoAI Design System](https://github.com/octoml/design-system).

## Built with 🛠️

-   Next.js
-   TypeScript
-   Tailwind
-   Zustand

## Consuming OctoML Design System 🍽️

Your host system/repository have a few security prerequisites for consumption of the OctoML Design System.

First, you need to export a GitHub Personal Access token with `read:packages` rights from your system under the variable name `NPM_TOKEN`. To do this:

-   Go to [Github Tokens](https://github.com/settings/tokens)
-   Create a **classic** access token
-   Set the permissions to `read:packages`
-   Save a copy.

Source this as `NPM_TOKEN` from your shell.

Second, you need to add an `.npmrc` file to the root of your project with the following information:

```
@octoml:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NPM_TOKEN}
```

With these in place, you should now be able to install all of the packages (including the Design System) using the yarn command.

## Run Locally 💻

Clone the cookbook repo from GitHub

```shell
git clone https://github.com/octoml/octoai-textgen-cookbook.git
```

Go to the frontend locally

```bash
cd doctalk/nextjs
```

Load in all the nodes_modules

```bash
yarn
```

Send it

```bash
yarn dev
```

## Contributing 👨🏽‍💻

**Commit Format** Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format for commit messages:

```vim
<type>(<scope>): <message>
```

where <type> is the change type (e.g., feat, fix), <scope> (optional) specifies the change's scope, and <message> briefly describes the change.
