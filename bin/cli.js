#!/usr/bin/env node
const { Command } = require('commander');
const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');

const program = new Command();
const packageJson = require('../package.json');

program
    .name('agentic-ai-kit')
    .description('CLI to bootstrap the Agentic AI Kit')
    .version(packageJson.version);

program
    .command('init')
    .description('Install the .agent folder into your project')
    .option('-p, --path <dest>', 'Specific directory to install to', '.')
    .option('-f, --force', 'Overwrite existing .agent folder')
    .action(async (options) => {
        const destDir = path.resolve(process.cwd(), options.path);
        const agentDestDir = path.join(destDir, '.agent');

        // We assume the CLI is running from the global/local node_modules/agentic-ai-kit/bin
        const sourceDir = path.resolve(__dirname, '..');
        const agentSourceDir = path.join(sourceDir, '.agent');

        console.log(chalk.blue('Initializing Agentic AI Kit...'));

        try {
            if (!await fs.pathExists(agentSourceDir)) {
                console.error(chalk.red('Error: Source .agent directory not found in the package.'));
                process.exit(1);
            }

            if (await fs.pathExists(agentDestDir)) {
                if (options.force) {
                    console.log(chalk.yellow('Force flag used. Overwriting existing .agent folder...'));
                    await fs.remove(agentDestDir);
                } else {
                    console.error(chalk.red('Error: .agent directory already exists. Use --force to overwrite.'));
                    process.exit(1);
                }
            }

            console.log(chalk.gray(`Copying .agent from ${agentSourceDir} to ${agentDestDir}...`));
            await fs.copy(agentSourceDir, agentDestDir);

            // Copying GEMINI.md or AGENT_FLOW.md if they exist in the root
            const filesToCopy = ['GEMINI.md', 'AGENT_FLOW.md'];
            for (const file of filesToCopy) {
                const fileSource = path.join(sourceDir, file);
                const fileDest = path.join(destDir, file);
                if (await fs.pathExists(fileSource)) {
                    await fs.copy(fileSource, fileDest, { overwrite: options.force });
                    console.log(chalk.gray(`Copied ${file}`));
                }
            }

            console.log(chalk.green('✨ Successfully installed Agentic AI Kit!'));
            console.log(chalk.cyan('\nGet started by reading the setup instructions or invoking an agent.'));
        } catch (err) {
            console.error(chalk.red(`\nFailed to initialize the kit: ${err.message}`));
            process.exit(1);
        }
    });

program.parse();
