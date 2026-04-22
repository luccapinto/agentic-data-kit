"""
sync_agents.py
==============
Sincroniza a pasta `.agent` (Fonte da Verdade — Antigravity) para:
  - `.github/`  → GitHub Copilot
  - `.claude/`  → Claude Code CLI

Mapeamento:
  🟣 SOURCE  : .agent/
  ⚪ COPILOT : .github/agents/*.agent.md | .github/skills/ | .github/prompts/*.prompt.md | .github/copilot-instructions.md
  🟠 CLAUDE  : .claude/agents/*.md      | .claude/skills/ | .claude/workflows/           | .claude/CLAUDE.md
"""

import re
import shutil
import sys
import codecs
from pathlib import Path

# Fix Windows encoding issues with emojis
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import yaml  # pip install pyyaml

# ---------------------------------------------------------------------------
# Caminhos raiz
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

# 🟣 Fonte da Verdade (Antigravity)
SOURCE = ROOT / ".agent"
AGENTS_SRC    = SOURCE / "agents"
SKILLS_SRC    = SOURCE / "skills"
WORKFLOWS_SRC = SOURCE / "workflows"
RULES_SRC     = SOURCE / "rules" / "rules.md"

# ⚪ Destino Copilot (.github)
COPILOT           = ROOT / ".github"
COPILOT_AGENTS    = COPILOT / "agents"
COPILOT_SKILLS    = COPILOT / "skills"
COPILOT_PROMPTS   = COPILOT / "prompts"
COPILOT_RULES     = COPILOT / "copilot-instructions.md"

# 🟠 Destino Claude (.claude)
CLAUDE            = ROOT / ".claude"
CLAUDE_AGENTS     = CLAUDE / "agents"
CLAUDE_SKILLS     = CLAUDE / "skills"
CLAUDE_WORKFLOWS  = CLAUDE / "workflows"
CLAUDE_MD         = CLAUDE / "CLAUDE.md"

# 🔵 Destino OpenCode (.opencode)
OPENCODE          = ROOT / ".opencode"
OPENCODE_AGENTS   = OPENCODE / "agents"
OPENCODE_SKILLS   = OPENCODE / "skills"
OPENCODE_COMMANDS = OPENCODE / "commands"
OPENCODE_AGENTS_MD = OPENCODE / "AGENTS.md"


# ---------------------------------------------------------------------------
# Helpers compartilhados
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Separa YAML frontmatter do corpo. Retorna ({}, texto) se não houver."""
    pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
    match = pattern.match(text)
    if match:
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
        return meta, text[match.end():]
    return {}, text


def first_sentence(text: str) -> str:
    """Primeira linha significativa do corpo (ignora títulos # e separadores)."""
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---"):
            clean = re.sub(r"[*_`>\[\]]", "", line).strip()
            if clean:
                return clean[:120]
    return "Agent logic"


def to_title_case(slug: str) -> str:
    """'data-scientist' → 'Data Scientist'."""
    return slug.replace("-", " ").replace("_", " ").title()


def clean_dirs(*dirs: Path) -> None:
    """Remove diretórios gerenciados (sem recriar — cada função cria o seu)."""
    for d in dirs:
        if d.exists():
            shutil.rmtree(d)
            print(f"  🗑️  Limpou: {d.relative_to(ROOT)}")


def copy_tree(src: Path, dest: Path, label: str) -> None:
    """copytree seguro: exige que dest NÃO exista (clean_dirs deve rodar antes)."""
    if src.exists():
        shutil.copytree(src, dest)
        count = sum(1 for f in dest.rglob("*") if f.is_file())
        print(f"  ✅  {count} arquivo(s) copiados → {label}")
    else:
        print(f"  ⚠️  Pasta não encontrada: {src.relative_to(ROOT)}")


# ===========================================================================
# ⚪ BLOCO COPILOT (.github)
# ===========================================================================

def copilot_sync_agents() -> None:
    """Agentes: injeta YAML padronizado + muda extensão para .agent.md."""
    COPILOT_AGENTS.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(AGENTS_SRC.glob("*.md")):
        raw = src_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)

        stem = src_file.stem
        name        = meta.get("name")        or to_title_case(stem)
        description = meta.get("description") or first_sentence(body)
        role        = first_sentence(body)

        new_meta   = {"name": name, "description": description, "role": role}
        yaml_block = yaml.dump(new_meta, allow_unicode=True, default_flow_style=False).strip()
        output     = f"---\n{yaml_block}\n---\n\n{body.lstrip()}"

        dest_file = COPILOT_AGENTS / f"{stem}.agent.md"
        dest_file.write_text(output, encoding="utf-8")
        print(f"  ✅  {src_file.name}  →  {dest_file.name}")


def copilot_sync_skills() -> None:
    """Skills: cópia recursiva exata."""
    copy_tree(SKILLS_SRC, COPILOT_SKILLS, COPILOT_SKILLS.relative_to(ROOT))


def copilot_sync_prompts() -> None:
    """Workflows → Prompt Files (.prompt.md) sem campo model."""
    COPILOT_PROMPTS.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(WORKFLOWS_SRC.glob("*.md")):
        raw = src_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)

        stem        = src_file.stem
        description = meta.get("description") or f"Workflow: {to_title_case(stem)}"
        new_meta    = {"name": stem, "description": description}
        yaml_block  = yaml.dump(new_meta, allow_unicode=True, default_flow_style=False).strip()

        context_block = "**Contexto:** {{selection}}\n"
        output = f"---\n{yaml_block}\n---\n\n{context_block}\n{body.lstrip()}"

        dest_file = COPILOT_PROMPTS / f"{stem}.prompt.md"
        dest_file.write_text(output, encoding="utf-8")
        print(f"  ✅  {src_file.name}  →  {dest_file.name}")


def copilot_sync_rules() -> None:
    """Rules → copilot-instructions.md."""
    if not RULES_SRC.exists():
        print(f"  ⚠️  rules.md não encontrado: {RULES_SRC}")
        return
    header = "<!-- Auto-generated by scripts/sync_agents.py — NÃO EDITE MANUALMENTE -->\n\n"
    COPILOT_RULES.write_text(header + RULES_SRC.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"  ✅  rules.md  →  copilot-instructions.md")


# ===========================================================================
# 🟠 BLOCO CLAUDE (.claude)
# ===========================================================================

def claude_sync_agents() -> None:
    """Agentes: cópia direta dos .md originais (Claude não precisa de YAML especial)."""
    CLAUDE_AGENTS.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(AGENTS_SRC.glob("*.md")):
        dest_file = CLAUDE_AGENTS / src_file.name
        shutil.copy2(src_file, dest_file)
        print(f"  ✅  {src_file.name}  →  {dest_file.relative_to(ROOT)}")


def claude_sync_skills() -> None:
    """Skills: cópia recursiva exata."""
    copy_tree(SKILLS_SRC, CLAUDE_SKILLS, CLAUDE_SKILLS.relative_to(ROOT))


def claude_sync_workflows() -> None:
    """Workflows: cópia recursiva exata."""
    copy_tree(WORKFLOWS_SRC, CLAUDE_WORKFLOWS, CLAUDE_WORKFLOWS.relative_to(ROOT))


def claude_build_claude_md() -> None:
    """CLAUDE.md = rules.md + seção de comandos dinâmicos gerada dos workflows."""
    if not RULES_SRC.exists():
        print(f"  ⚠️  rules.md não encontrado, CLAUDE.md não será gerado.")
        return

    rules_content = RULES_SRC.read_text(encoding="utf-8")

    # Constrói bloco de comandos a partir dos workflows disponíveis
    commands_lines: list[str] = []
    for wf_file in sorted(WORKFLOWS_SRC.glob("*.md")):
        raw = wf_file.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(raw)
        stem        = wf_file.stem
        description = meta.get("description") or to_title_case(stem)
        commands_lines.append(
            f"- **/{stem}**: {description} "
            f"— Load context from `.claude/workflows/{wf_file.name}` and follow its steps."
        )

    commands_block = "\n".join(commands_lines)

    claude_md_content = (
        "<!-- Auto-generated by scripts/sync_agents.py — NÃO EDITE MANUALMENTE -->\n\n"
        + rules_content.rstrip()
        + "\n\n---\n\n"
        + "## ⚡ Custom Commands & Workflows\n\n"
        + "The following slash commands are available. When triggered, load the referenced\n"
        + "workflow file and follow its instructions step by step.\n\n"
        + commands_block
        + "\n"
    )

    CLAUDE_MD.write_text(claude_md_content, encoding="utf-8")
    print(f"  ✅  CLAUDE.md gerado com {len(commands_lines)} comando(s)")


# ===========================================================================
# 🔵 BLOCO OPENCODE (.opencode)
# ===========================================================================

def opencode_sync_agents() -> None:
    """Agentes: cópia direta para .opencode/agents/."""
    OPENCODE_AGENTS.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(AGENTS_SRC.glob("*.md")):
        dest_file = OPENCODE_AGENTS / src_file.name
        shutil.copy2(src_file, dest_file)
        print(f"  ✅  {src_file.name}  →  {dest_file.relative_to(ROOT)}")


def opencode_sync_skills() -> None:
    """Skills: cópia recursiva exata de todas as pastas de skills."""
    copy_tree(SKILLS_SRC, OPENCODE_SKILLS, OPENCODE_SKILLS.relative_to(ROOT))


def opencode_sync_commands() -> None:
    """Commands: workflows copiados para .opencode/commands/."""
    OPENCODE_COMMANDS.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(WORKFLOWS_SRC.glob("*.md")):
        dest_file = OPENCODE_COMMANDS / src_file.name
        shutil.copy2(src_file, dest_file)
        print(f"  ✅  {src_file.name}  →  {dest_file.relative_to(ROOT)}")


def opencode_sync_agents_md() -> None:
    """AGENTS.md: Cópia do rules.md para a pasta .opencode/."""
    if not RULES_SRC.exists():
        print(f"  ⚠️  rules.md não encontrado para AGENTS.md")
        return
    shutil.copy2(RULES_SRC, OPENCODE_AGENTS_MD)
    print(f"  ✅  rules.md  →  {OPENCODE_AGENTS_MD.relative_to(ROOT)}")


# ===========================================================================
# Main
# ===========================================================================
def main() -> None:
    print("=" * 60)
    print("🟣 Antigravity Sync  —  .agent → .github + .claude")
    print("=" * 60)
    print(f"   Fonte    : {SOURCE.relative_to(ROOT)}")
    print(f"   Copilot  : {COPILOT.relative_to(ROOT)}")
    print(f"   Claude   : {CLAUDE.relative_to(ROOT)}")
    print(f"   OpenCode : {OPENCODE.relative_to(ROOT)}")

    # Garante que os destinos-raiz existam
    COPILOT.mkdir(parents=True, exist_ok=True)
    CLAUDE.mkdir(parents=True, exist_ok=True)
    OPENCODE.mkdir(parents=True, exist_ok=True)

    # Limpeza — skills NÃO entra (copytree exige ausência do dest)
    # .github/workflows é preservado (não está na lista)
    print("\n🗑️  Limpando diretórios anteriores...")
    clean_dirs(
        COPILOT_AGENTS, COPILOT_SKILLS, COPILOT_PROMPTS,
        CLAUDE_AGENTS,  CLAUDE_SKILLS,  CLAUDE_WORKFLOWS,
        OPENCODE_AGENTS, OPENCODE_SKILLS, OPENCODE_COMMANDS
    )

    # ------------------------------------------------------------------
    print("\n⚪ [COPILOT] Sincronizando para .github/...")
    # ------------------------------------------------------------------
    print("  📦 Agentes:")
    copilot_sync_agents()
    print("  🛠️  Skills:")
    copilot_sync_skills()
    print("  📝 Prompts:")
    copilot_sync_prompts()
    print("  📋 Regras:")
    copilot_sync_rules()

    # ------------------------------------------------------------------
    print("\n🟠 [CLAUDE] Sincronizando para .claude/...")
    # ------------------------------------------------------------------
    print("  📦 Agentes:")
    claude_sync_agents()
    print("  🛠️  Skills:")
    claude_sync_skills()
    print("  📝 Workflows:")
    claude_sync_workflows()
    print("  📋 CLAUDE.md:")
    claude_build_claude_md()

    # ------------------------------------------------------------------
    print("\n🔵 [OPENCODE] Sincronizando para .opencode/...")
    # ------------------------------------------------------------------
    print("  📦 Agentes:")
    opencode_sync_agents()
    print("  🛠️  Skills:")
    opencode_sync_skills()
    print("  📝 Commands:")
    opencode_sync_commands()
    print("  📋 AGENTS.md:")
    opencode_sync_agents_md()

    # Summary
    print("\n" + "=" * 60)
    print("✨ Sincronização concluída!")
    print(f"   ⚪ Copilot agents  : {COPILOT_AGENTS.relative_to(ROOT)}")
    print(f"   ⚪ Copilot skills  : {COPILOT_SKILLS.relative_to(ROOT)}")
    print(f"   ⚪ Copilot prompts : {COPILOT_PROMPTS.relative_to(ROOT)}")
    print(f"   ⚪ Copilot rules   : {COPILOT_RULES.relative_to(ROOT)}")
    print(f"   🟠 Claude agents   : {CLAUDE_AGENTS.relative_to(ROOT)}")
    print(f"   🟠 Claude skills   : {CLAUDE_SKILLS.relative_to(ROOT)}")
    print(f"   🟠 Claude workflows: {CLAUDE_WORKFLOWS.relative_to(ROOT)}")
    print(f"   🟠 CLAUDE.md       : {CLAUDE_MD.relative_to(ROOT)}")
    print(f"   🔵 OpenCode agents : {OPENCODE_AGENTS.relative_to(ROOT)}")
    print(f"   🔵 OpenCode skills : {OPENCODE_SKILLS.relative_to(ROOT)}")
    print(f"   🔵 OpenCode cmd    : {OPENCODE_COMMANDS.relative_to(ROOT)}")
    print(f"   🔵 AGENTS.md       : {OPENCODE_AGENTS_MD.relative_to(ROOT)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
