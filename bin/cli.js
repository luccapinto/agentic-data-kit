#!/usr/bin/env node
import { Command } from 'commander';
import fs from 'fs-extra';
import path from 'path';
import chalk from 'chalk';
import figlet from 'figlet';
import gradient from 'gradient-string';
import boxen from 'boxen';
import { select } from '@inquirer/prompts';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const program = new Command();
const packageJson = JSON.parse(
    fs.readFileSync(path.join(__dirname, '../package.json'), 'utf-8')
);

// Brand gradient: blue → sky → teal (mirrors the DESIGN.md accent family).
const brand = gradient(['#5B8DEF', '#38BDF8', '#0E7C66']);

/** Big, gradient ASCII banner with graceful fallbacks for narrow terminals. */
function printBanner() {
    const cols = process.stdout.columns || 80;
    try {
        if (cols >= 60) {
            const art =
                figlet.textSync('AGENTIC', { font: 'ANSI Shadow' }) + '\n' +
                figlet.textSync('DATA KIT', { font: 'ANSI Shadow' });
            console.log('\n' + brand.multiline(art));
        } else {
            console.log('\n' + chalk.bold(brand('AGENTIC DATA KIT')));
        }
    } catch {
        console.log('\n' + chalk.cyanBright.bold('AGENTIC DATA KIT'));
    }
    console.log(chalk.bold('  Drop one folder. Get a team of AI data specialists.'));
    console.log(
        chalk.dim(`  5 agents · 8 skills · 3 workflows · 4 platforms`) +
        chalk.dim(`  ·  v${packageJson.version}\n`)
    );
}

/** Framed success box with tailored next steps. */
function printSuccess(label, steps) {
    const content =
        chalk.green.bold(`✓ Installed for ${label}`) + '\n\n' +
        steps.map((s) => `${chalk.cyan('›')} ${s}`).join('\n');
    console.log(
        boxen(content, {
            padding: 1,
            margin: { top: 1, bottom: 1, left: 0, right: 0 },
            borderColor: 'green',
            borderStyle: 'round',
            title: '✨ Ready',
            titleAlignment: 'center',
        })
    );
}

const NEXT_STEPS = {
    antigravity: {
        label: 'Antigravity (source of truth)',
        steps: [
            `Your source of truth lives in ${chalk.bold('.agent/')}.`,
            `Run ${chalk.bold('python scripts/sync_agents.py')} after any change to fan out to every tool.`,
        ],
    },
    copilot: {
        label: 'GitHub Copilot',
        steps: [
            `Use ${chalk.bold('@')} triggers in Copilot Chat (e.g. ${chalk.bold('@data-engineer')}).`,
            `Agents, skills and prompts now live in ${chalk.bold('.github/')}.`,
        ],
    },
    claude: {
        label: 'Claude Code',
        steps: [
            `Run ${chalk.bold('claude')} in your terminal to meet your new specialists.`,
            `Try: ${chalk.italic('"Build a Medallion pipeline for customer data"')}.`,
        ],
    },
    opencode: {
        label: 'OpenCode',
        steps: [
            `Root ${chalk.bold('AGENTS.md')} + everything else in ${chalk.bold('.opencode/')}.`,
            `Your project now follows the OpenCode standard.`,
        ],
    },
};

program
    .name('agentic-data-kit')
    .description('CLI to bootstrap the Agentic Data Kit')
    .version(packageJson.version);

program
    .command('init')
    .description('Install the Agentic Data Kit into your project')
    .option('-p, --path <dest>', 'Specific directory to install to', '.')
    .option('-t, --target <framework>', 'Target framework (antigravity, copilot, claude, opencode)')
    .option('-f, --force', 'Overwrite existing folders')
    .action(async (options) => {
        printBanner();

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
            console.error(chalk.red(`✗ Invalid target '${targetFramework}'. Choose 'antigravity', 'copilot', 'claude', or 'opencode'.`));
            process.exit(1);
        }

        const sourceDir = path.resolve(__dirname, '..');
        const agentSourceDir = path.join(sourceDir, targetFolder);

        // Final destination directory
        const agentDestDir = path.join(destDir, targetFolder);

        try {
            if (!await fs.pathExists(agentSourceDir)) {
                console.error(chalk.red(`✗ Source ${targetFolder} directory not found in the package.`));
                if (targetFramework !== 'antigravity') {
                    console.log(chalk.yellow(`  Did you run 'python scripts/sync_agents.py' to generate the ${targetFolder} folder before publishing?`));
                }
                process.exit(1);
            }

            const alreadyExists = targetFramework === 'opencode'
                ? (await fs.pathExists(agentDestDir) || await fs.pathExists(path.join(destDir, 'AGENTS.md')))
                : await fs.pathExists(agentDestDir);

            if (alreadyExists) {
                if (options.force) {
                    console.log(chalk.yellow(`⚠ Force flag used — overwriting existing ${targetFramework} setup...`));
                    await fs.remove(agentDestDir);
                    if (targetFramework === 'opencode') {
                        await fs.remove(path.join(destDir, 'AGENTS.md'));
                    }
                } else {
                    const errorMsg = targetFramework === 'opencode'
                        ? `✗ Already initialized for OpenCode (found .opencode folder or AGENTS.md). Use --force to overwrite.`
                        : `✗ ${targetFolder} directory already exists. Use --force to overwrite.`;
                    console.error(chalk.red(errorMsg));
                    process.exit(1);
                }
            }

            process.stdout.write(chalk.dim(`  Installing ${targetFramework} setup… `));
            await fs.copy(agentSourceDir, agentDestDir);

            // OpenCode special handling: move AGENTS.md to root
            if (targetFramework === 'opencode') {
                const agentsMdPath = path.join(agentDestDir, 'AGENTS.md');
                const rootAgentsMdPath = path.join(destDir, 'AGENTS.md');
                if (await fs.pathExists(agentsMdPath)) {
                    await fs.move(agentsMdPath, rootAgentsMdPath, { overwrite: true });
                }
            }
            console.log(chalk.green('done'));

            const info = NEXT_STEPS[targetFramework];
            printSuccess(info.label, info.steps);

        } catch (err) {
            console.error(chalk.red(`\n✗ Failed to initialize the kit: ${err.message}`));
            process.exit(1);
        }
    });

// Bare invocation (`npx @luccapinto/agentic-data-kit`) → show the banner + help.
if (!process.argv.slice(2).length) {
    printBanner();
    program.outputHelp();
    process.exit(0);
}

program.parse();
