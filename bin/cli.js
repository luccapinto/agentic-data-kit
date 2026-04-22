#!/usr/bin/env node
import { Command } from 'commander';
import fs from 'fs-extra';
import path from 'path';
import chalk from 'chalk';
import { select } from '@inquirer/prompts';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const program = new Command();
const packageJson = JSON.parse(
    fs.readFileSync(path.join(__dirname, '../package.json'), 'utf-8')
);

program
    .name('agentic-data-kit')
    .description('CLI to bootstrap the Agentic Data Kit')
    .version(packageJson.version);

program
    .command('init')
    .description('Install the Agentic Data Kit into your project')
    .option('-p, --path <dest>', 'Specific directory to install to', '.')
    .option('-t, --target <framework>', 'Target framework (antigravity, copilot, claude)')
    .option('-f, --force', 'Overwrite existing folders')
    .action(async (options) => {
        const destDir = path.resolve(process.cwd(), options.path);

        let targetFramework = options.target;

        if (!targetFramework) {
            targetFramework = await select({
                message: 'Which AI assistant are you using?',
                choices: [
                    {
                        name: 'GitHub Copilot (VS Code)',
                        value: 'copilot',
                        description: 'Installs the .github folder'
                    },
                    {
                        name: 'Claude Code (CLI)',
                        value: 'claude',
                        description: 'Installs the .claude folder'
                    },
                    {
                        name: 'Antigravity (Autonomous Agents & Sync Engine)',
                        value: 'antigravity',
                        description: 'Installs the .agent folder (Source of truth)'
                    },
                    {
                        name: 'OpenCode (Standard Agentic Format)',
                        value: 'opencode',
                        description: 'Installs AGENTS.md to root and /agents, /skills, /commands folders'
                    }
                ]
            });
        }

        // Map the user choice to the actual folder name in the repo
        const folderMapping = {
            'antigravity': '.agent',
            'copilot': '.github',
            'claude': '.claude',
            'opencode': '.opencode'
        };

        const targetFolder = folderMapping[targetFramework];

        if (!targetFolder) {
            console.error(chalk.red(`Error: Invalid target '${targetFramework}'. Choose 'antigravity', 'copilot', 'claude', or 'opencode'.`));
            process.exit(1);
        }

        const sourceDir = path.resolve(__dirname, '..');
        const agentSourceDir = path.join(sourceDir, targetFolder);
        
        // Final destination directory
        const agentDestDir = path.join(destDir, targetFolder);

        console.log(chalk.blue('\nInitializing Agentic Data Kit...'));

        try {
            if (!await fs.pathExists(agentSourceDir)) {
                console.error(chalk.red(`Error: Source ${targetFolder} directory not found in the package.`));
                if (targetFramework !== 'antigravity') {
                    console.log(chalk.yellow(`Did you run 'python scripts/sync_agents.py' to generate the ${targetFolder} folder before publishing?`));
                }
                process.exit(1);
            }

            const alreadyExists = targetFramework === 'opencode'
                ? (await fs.pathExists(agentDestDir) || await fs.pathExists(path.join(destDir, 'AGENTS.md')))
                : await fs.pathExists(agentDestDir);

            if (alreadyExists) {
                if (options.force) {
                    console.log(chalk.yellow(`Force flag used. Overwriting existing ${targetFramework} setup...`));
                    await fs.remove(agentDestDir);
                    if (targetFramework === 'opencode') {
                        await fs.remove(path.join(destDir, 'AGENTS.md'));
                    }
                } else {
                    const errorMsg = targetFramework === 'opencode'
                        ? `Error: Agentic Data Kit already initialized for OpenCode (found .opencode folder or AGENTS.md). Use --force to overwrite.`
                        : `Error: ${targetFolder} directory already exists. Use --force to overwrite.`;
                    console.error(chalk.red(errorMsg));
                    process.exit(1);
                }
            }

            console.log(chalk.gray(`Installing ${targetFramework} setup...`));
            await fs.copy(agentSourceDir, agentDestDir);

            // OpenCode special handling: move AGENTS.md to root
            if (targetFramework === 'opencode') {
                const agentsMdPath = path.join(agentDestDir, 'AGENTS.md');
                const rootAgentsMdPath = path.join(destDir, 'AGENTS.md');
                if (await fs.pathExists(agentsMdPath)) {
                    await fs.move(agentsMdPath, rootAgentsMdPath, { overwrite: true });
                }
            }

            console.log(chalk.green(`\n✨ Successfully installed Agentic Data Kit for ${targetFramework}!`));

            if (targetFramework === 'antigravity') {
                console.log(chalk.cyan('Ready! Your source of truth is now in the .agent/ folder. run scripts/sync_agents.py after modifications.'));
            } else if (targetFramework === 'copilot') {
                console.log(chalk.cyan('Ready! Use @ triggers in GitHub Copilot Chat (e.g. @data-engineer) in your editor.'));
            } else if (targetFramework === 'claude') {
                console.log(chalk.cyan('Ready! Open your terminal and run `claude` to interact with your new specialists.'));
            } else if (targetFramework === 'opencode') {
                console.log(chalk.cyan('Ready! Your project now follows the OpenCode standard with AGENTS.md at the root and everything else in .opencode/.'));
            }

            console.log('\n');

        } catch (err) {
            console.error(chalk.red(`\nFailed to initialize the kit: ${err.message}`));
            process.exit(1);
        }
    });

program.parse();
