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
const packageRoot = path.resolve(__dirname, '..');

const program = new Command();
const packageJson = JSON.parse(
    fs.readFileSync(path.join(packageRoot, 'package.json'), 'utf-8')
);

// Brand gradient: blue → sky → teal (mirrors the DESIGN.md accent family).
const brand = gradient(['#5B8DEF', '#38BDF8', '#0E7C66']);

/**
 * Install targets. `folder` is copied as-is; `rootFiles` are copied from the package root
 * into the destination root. `exclude` lists paths (relative to `folder`) that ship in the
 * repo but must not land in the user's project.
 */
const TARGETS = {
    claude: {
        name: 'Claude Code',
        folder: '.claude',
        description: 'Installs the .claude folder (agents, skills, commands, CLAUDE.md)',
        steps: [
            `Run ${chalk.bold('claude')} in your project; the pbi-* skills load when a request matches.`,
            `Try: ${chalk.italic('"Add a Total Sales measure and a card for it in Sales.pbip"')}.`,
        ],
    },
    copilot: {
        name: 'GitHub Copilot (VS Code)',
        folder: '.github',
        exclude: ['workflows'],
        description: 'Installs agents, skills, prompts and copilot-instructions.md into .github',
        steps: [
            `Skills, prompts and the ${chalk.bold('pbi-visual-reviewer')} agent now live in ${chalk.bold('.github/')}.`,
            `Run ${chalk.bold('/validate-pbi')} in Copilot Chat to check a PBIP project.`,
        ],
    },
    cursor: {
        name: 'Cursor',
        folder: '.cursor',
        description: 'Installs the .cursor folder (always-on rule, commands, skills)',
        steps: [
            `Rules, commands and skills now live in ${chalk.bold('.cursor/')}.`,
            `No subagents here: run the visual review in a fresh chat with only the screenshots.`,
        ],
    },
    opencode: {
        name: 'OpenCode',
        folder: '.opencode',
        rootFiles: ['AGENTS.md'],
        description: 'Installs .opencode (agents, skills, commands) and the root AGENTS.md',
        steps: [
            `Root ${chalk.bold('AGENTS.md')} + agents, skills and commands in ${chalk.bold('.opencode/')}.`,
            `Call the reviewer with ${chalk.bold('@pbi-visual-reviewer')}.`,
        ],
    },
    antigravity: {
        name: 'Antigravity (source of truth)',
        folder: '.agent',
        rootFiles: ['scripts/sync_agents.py'],
        description: 'Installs the .agent folder (source of truth) and scripts/sync_agents.py',
        steps: [
            `Your source of truth lives in ${chalk.bold('.agent/')}.`,
            `Run ${chalk.bold('python3 scripts/sync_agents.py')} (needs PyYAML) to fan it out to every other tool.`,
        ],
    },
};

function countKit() {
    const src = path.join(packageRoot, '.agent');
    const list = (dir, pred) => (fs.existsSync(dir) ? fs.readdirSync(dir, { withFileTypes: true }).filter(pred).length : 0);
    return {
        agents: list(path.join(src, 'agents'), (e) => e.isFile() && e.name.endsWith('.md')),
        skills: list(path.join(src, 'skills'), (e) => e.isDirectory()),
        workflows: list(path.join(src, 'workflows'), (e) => e.isFile() && e.name.endsWith('.md')),
    };
}

const plural = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`;

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
    const kit = countKit();
    console.log(chalk.bold('  Power BI as code, with Desktop open. Skills for every AI assistant.'));
    console.log(
        chalk.dim(
            `  ${plural(kit.agents, 'agent')} · ${plural(kit.skills, 'skill')} · ` +
            `${plural(kit.workflows, 'workflow')} · ${plural(Object.keys(TARGETS).length, 'platform')}`
        ) +
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

function fail(message, hint) {
    console.error(chalk.red(`✗ ${message}`));
    if (hint) console.log(chalk.yellow(`  ${hint}`));
    process.exit(1);
}

program
    .name('agentic-data-kit')
    .description('CLI to bootstrap the Agentic Data Kit')
    .version(packageJson.version);

program
    .command('init')
    .description('Install the Agentic Data Kit into your project')
    .option('-p, --path <dest>', 'Specific directory to install to', '.')
    .option('-t, --target <framework>', `Target framework (${Object.keys(TARGETS).join(', ')})`)
    .option('-f, --force', 'Overwrite existing folders')
    .action(async (options) => {
        printBanner();

        const destDir = path.resolve(process.cwd(), options.path);
        let targetKey = options.target;
        if (!targetKey) {
            targetKey = await select({
                message: 'Which AI assistant are you using?',
                choices: Object.entries(TARGETS).map(([value, t]) => ({
                    name: t.name,
                    value,
                    description: t.description,
                })),
            });
        }

        const target = TARGETS[targetKey];
        if (!target) {
            fail(`Invalid target '${targetKey}'. Choose one of: ${Object.keys(TARGETS).join(', ')}.`);
        }

        const sourceFolder = path.join(packageRoot, target.folder);
        const destFolder = path.join(destDir, target.folder);
        const rootFiles = target.rootFiles || [];
        // .github is shared with the user's own files (workflows, templates): only the kit's
        // generated entries are checked, removed and copied — never the whole folder.
        const shared = target.folder === '.github';
        const entries = shared
            ? (await fs.readdir(sourceFolder).catch(() => [])).filter((e) => !(target.exclude || []).includes(e))
            : null;

        try {
            if (!(await fs.pathExists(sourceFolder))) {
                fail(
                    `Source ${target.folder} directory not found in the package.`,
                    targetKey !== 'antigravity' ? `Run 'python3 scripts/sync_agents.py' before publishing.` : undefined
                );
            }

            const installed = shared
                ? entries.map((e) => path.join(destFolder, e))
                : [destFolder];
            const existing = [];
            for (const p of [...installed, ...rootFiles.map((f) => path.join(destDir, f))]) {
                if (await fs.pathExists(p)) existing.push(path.relative(destDir, p) || p);
            }

            if (existing.length) {
                if (!options.force) {
                    fail(`Already initialized for ${target.name} (found ${existing.join(', ')}). Use --force to overwrite.`);
                }
                console.log(chalk.yellow(`⚠ Force flag used — overwriting ${existing.join(', ')}...`));
                for (const p of existing) await fs.remove(path.join(destDir, p));
            }

            process.stdout.write(chalk.dim(`  Installing ${targetKey} setup… `));
            const noBytecode = (src) => !path.relative(sourceFolder, src).split(path.sep).includes('__pycache__');
            if (shared) {
                for (const e of entries) {
                    await fs.copy(path.join(sourceFolder, e), path.join(destFolder, e), { filter: noBytecode });
                }
            } else {
                await fs.copy(sourceFolder, destFolder, { filter: noBytecode });
            }
            for (const f of rootFiles) {
                await fs.copy(path.join(packageRoot, f), path.join(destDir, f));
            }
            console.log(chalk.green('done'));

            printSuccess(target.name, target.steps);
        } catch (err) {
            fail(`Failed to initialize the kit: ${err.message}`);
        }
    });

// Bare invocation (`npx @luccapinto/agentic-data-kit`) → show the banner + help.
if (!process.argv.slice(2).length) {
    printBanner();
    program.outputHelp();
    process.exit(0);
}

program.parse();
