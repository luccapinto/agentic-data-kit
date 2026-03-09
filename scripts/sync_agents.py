"""
sync_agents.py
==============
Sincroniza a pasta `.agent` (fonte da verdade) com `.github` (GitHub Copilot).

Mapeamento:
  .agent/agents/*.md        →  .github/agents/*.agent.md
  .agent/skills/            →  .github/skills/   (cópia recursiva)
  .agent/workflows/*.md     →  .github/prompts/*.prompt.md
  .agent/rules/rules.md     →  .github/copilot-instructions.md
"""

import re
import shutil
from pathlib import Path

import yaml  # pip install pyyaml

# ---------------------------------------------------------------------------
# Configuração de caminhos
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
ORIGIN = ROOT / ".agent"
DEST = ROOT / ".github"

AGENTS_SRC = ORIGIN / "agents"
SKILLS_SRC = ORIGIN / "skills"
WORKFLOWS_SRC = ORIGIN / "workflows"
RULES_SRC = ORIGIN / "rules" / "rules.md"

AGENTS_DEST = DEST / "agents"
SKILLS_DEST = DEST / "skills"
PROMPTS_DEST = DEST / "prompts"
INSTRUCTIONS_DEST = DEST / "copilot-instructions.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Separa o YAML frontmatter do corpo do arquivo.

    Returns:
        (meta_dict, body_string) — meta_dict é {} se não houver frontmatter.
    """
    pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
    match = pattern.match(text)
    if match:
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
        body = text[match.end():]
        return meta, body
    return {}, text


def first_sentence(text: str) -> str:
    """Extrai a primeira frase significativa do texto (ignora cabeçalhos #)."""
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---"):
            # Remove formatação Markdown inline básica
            clean = re.sub(r"[*_`>\[\]]", "", line).strip()
            if clean:
                # Trunca em 120 caracteres para não deixar o campo muito longo
                return clean[:120]
    return "Agent logic"


def to_title_case(slug: str) -> str:
    """Converte 'data-scientist' → 'Data Scientist'."""
    return slug.replace("-", " ").replace("_", " ").title()


def clean_dirs(*dirs: Path) -> None:
    """Remove os diretórios de destino (sem recriar — cada função cria o seu)."""
    for d in dirs:
        if d.exists():
            shutil.rmtree(d)
            print(f"  🗑️  Limpou: {d.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# 1. Agentes
# ---------------------------------------------------------------------------
def sync_agents() -> None:
    print("\n📦 Sincronizando AGENTES...")
    AGENTS_DEST.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(AGENTS_SRC.glob("*.md")):
        raw = src_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)

        stem = src_file.stem  # ex: "data-scientist"
        name = meta.get("name") or to_title_case(stem)
        description = meta.get("description") or first_sentence(body)
        role = first_sentence(body)

        # Monta novo cabeçalho YAML (sem model, sem tools, sem skills)
        new_meta = {"name": name, "description": description, "role": role}
        yaml_block = yaml.dump(new_meta, allow_unicode=True, default_flow_style=False).strip()
        output = f"---\n{yaml_block}\n---\n\n{body.lstrip()}"

        dest_file = AGENTS_DEST / f"{stem}.agent.md"
        dest_file.write_text(output, encoding="utf-8")
        print(f"  ✅  {src_file.name}  →  {dest_file.name}")


# ---------------------------------------------------------------------------
# 2. Skills
# ---------------------------------------------------------------------------
def sync_skills() -> None:
    print("\n🛠️  Sincronizando SKILLS...")
    if SKILLS_SRC.exists():
        # copytree requer que o destino NÃO exista — clean_dirs já removeu
        shutil.copytree(SKILLS_SRC, SKILLS_DEST)
        count = sum(1 for _ in SKILLS_DEST.rglob("*") if _.is_file())
        print(f"  ✅  {count} arquivo(s) copiados de skills/")
    else:
        print(f"  ⚠️  Pasta de skills não encontrada: {SKILLS_SRC}")


# ---------------------------------------------------------------------------
# 3. Prompts (Workflows)
# ---------------------------------------------------------------------------
def sync_prompts() -> None:
    print("\n📝 Sincronizando PROMPTS (workflows)...")
    PROMPTS_DEST.mkdir(parents=True, exist_ok=True)
    for src_file in sorted(WORKFLOWS_SRC.glob("*.md")):
        raw = src_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)

        stem = src_file.stem  # ex: "brainstorm"
        name = stem  # usa o nome do arquivo como nome do prompt
        description = meta.get("description") or f"Workflow: {to_title_case(stem)}"

        # NÃO inclui o campo `model` — Copilot usará o padrão do usuário
        new_meta = {"name": name, "description": description}
        yaml_block = yaml.dump(new_meta, allow_unicode=True, default_flow_style=False).strip()

        # Contexto padrão do Copilot + conteúdo original
        context_block = "**Contexto:** {{selection}}\n"
        output = f"---\n{yaml_block}\n---\n\n{context_block}\n{body.lstrip()}"

        dest_file = PROMPTS_DEST / f"{stem}.prompt.md"
        dest_file.write_text(output, encoding="utf-8")
        print(f"  ✅  {src_file.name}  →  {dest_file.name}")


# ---------------------------------------------------------------------------
# 4. Copilot Instructions (rules)
# ---------------------------------------------------------------------------
def sync_rules() -> None:
    print("\n📋 Sincronizando REGRAS GLOBAIS...")
    if not RULES_SRC.exists():
        print(f"  ⚠️  Arquivo de regras não encontrado: {RULES_SRC}")
        return

    rules_content = RULES_SRC.read_text(encoding="utf-8")
    header = "<!-- Auto-generated by scripts/sync_agents.py — NÃO EDITE MANUALMENTE -->\n\n"
    INSTRUCTIONS_DEST.write_text(header + rules_content, encoding="utf-8")
    print(f"  ✅  rules.md  →  copilot-instructions.md")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("🔄 Iniciando sincronização: .agent → .github")
    print(f"   Origem  : {ORIGIN.relative_to(ROOT)}")
    print(f"   Destino : {DEST.relative_to(ROOT)}")

    # Garante que .github existe
    DEST.mkdir(parents=True, exist_ok=True)

    # Limpeza dos diretórios gerenciados (skills NÃO entra aqui — copytree exige ausência)
    # .github/workflows é preservado automaticamente pois não está na lista
    print("\n🗑️  Limpando diretórios anteriores...")
    clean_dirs(AGENTS_DEST, SKILLS_DEST, PROMPTS_DEST)

    # Executa sincronizações
    sync_agents()
    sync_skills()
    sync_prompts()
    sync_rules()

    print("\n✨ Sincronização concluída com sucesso!")
    print(f"   Agentes  : {AGENTS_DEST.relative_to(ROOT)}")
    print(f"   Skills   : {SKILLS_DEST.relative_to(ROOT)}")
    print(f"   Prompts  : {PROMPTS_DEST.relative_to(ROOT)}")
    print(f"   Regras   : {INSTRUCTIONS_DEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
