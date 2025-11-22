"""
Gerenciador de Tarefas
Implementa criação, gestão, arquivamento e relatórios de tarefas conforme especificado.
Arquivos usados:
 - tarefas.json
 - tarefas_arquivadas.json
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# -------------------------
# Declaração de variáveis globais
# -------------------------
TASKS_FILE = "tarefas.json"
ARCHIVE_FILE = "tarefas_arquivadas.json"

# A lista principal de tarefas (cada tarefa é um dict)
tarefas: List[Dict[str, Any]] = []

# Controle de IDs: será calculado ao carregar os dados
next_id: int = 1

# Constantes do sistema
PRIORIDADES = ["Urgente", "Alta", "Média", "Baixa"]
ORIGENS = ["E-mail", "Telefone", "Chamado do Sistema"]
STATUS_PENDENTE = "Pendente"
STATUS_FAZENDO = "Fazendo"
STATUS_CONCLUIDA = "Concluída"
STATUS_ARQUIVADO = "Arquivado"
STATUS_EXCLUIDA = "Excluída"

# -------------------------
# Funções de persistência / inicialização
# -------------------------
def carregar_arquivos_iniciais():
    """
    Verifica existência dos arquivos necessários e cria-os se ausentes.
    Em seguida carrega tarefas.json para a lista global tarefas e inicializa next_id.
    """
    global tarefas, next_id
    print("Executando a função carregar_arquivos_iniciais")
    # Criar arquivos se não existirem
    for fname in (TASKS_FILE, ARCHIVE_FILE):
        if not os.path.exists(fname):
            try:
                with open(fname, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Erro ao criar arquivo {fname}: {e}")

    # Carregar tarefas
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:
        print(f"Erro ao ler {TASKS_FILE}: {e}")
        raw = []

    # Converter datas ISO -> datetime para uso interno
    tarefas = []
    max_id = 0
    for item in raw:
        # copia para evitar mutação do json diretamente
        t = dict(item)
        # parse data_criacao e data_conclusao se existirem
        if t.get("data_criacao"):
            try:
                t["data_criacao"] = datetime.fromisoformat(t["data_criacao"])
            except Exception:
                t["data_criacao"] = None
        if t.get("data_conclusao"):
            try:
                t["data_conclusao"] = datetime.fromisoformat(t["data_conclusao"])
            except Exception:
                t["data_conclusao"] = None
        tarefas.append(t)
        if isinstance(t.get("id"), int) and t["id"] > max_id:
            max_id = t["id"]

    next_id = max_id + 1

def salvar_dados():
    """
    Salva a lista global de tarefas em tarefas.json convertendo datetimes para strings ISO.
    """
    print("Executando a função salvar_dados")
    serializavel = []
    for t in tarefas:
        item = dict(t)
        if isinstance(item.get("data_criacao"), datetime):
            item["data_criacao"] = item["data_criacao"].isoformat()
        if isinstance(item.get("data_conclusao"), datetime):
            item["data_conclusao"] = item["data_conclusao"].isoformat()
        serializavel.append(item)
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(serializavel, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar {TASKS_FILE}: {e}")

def registrar_em_arquivo_arquivadas(itens: List[Dict[str, Any]]):
    """
    Recebe lista de tarefas (com datetimes convertidos) e adiciona ao arquivo tarefas_arquivadas.json.
    Este arquivo deve acumular histórico.
    """
    print("Executando a função registrar_em_arquivo_arquivadas")
    # Ler arquivo existente
    try:
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            existente = json.load(f)
    except Exception:
        existente = []

    # Preparar itens serializáveis
    a_adicionar = []
    for t in itens:
        item = dict(t)
        if isinstance(item.get("data_criacao"), datetime):
            item["data_criacao"] = item["data_criacao"].isoformat()
        if isinstance(item.get("data_conclusao"), datetime):
            item["data_conclusao"] = item["data_conclusao"].isoformat()
        a_adicionar.append(item)

    existente.extend(a_adicionar)
    try:
        with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
            json.dump(existente, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao escrever {ARCHIVE_FILE}: {e}")

# -------------------------
# Funções utilitárias de validação e busca
# -------------------------
def validar_prioridade(valor: str) -> Optional[str]:
    """
    Valida se a prioridade está dentro de PRIORIDADES.
    Retorna a string padronizada se válida, ou None se inválida.
    """
    print("Executando a função validar_prioridade")
    for p in PRIORIDADES:
        if valor.strip().lower() == p.lower():
            return p
    return None

def validar_origem(valor: str) -> Optional[str]:
    """
    Valida a origem da tarefa (E-mail, Telefone, Chamado do Sistema).
    """
    print("Executando a função validar_origem")
    for o in ORIGENS:
        if valor.strip().lower() == o.lower():
            return o
    return None

def encontrar_tarefa_por_id(tid: int) -> Optional[Dict[str, Any]]:
    """
    Retorna a tarefa com o id fornecido ou None se não encontrada.
    """
    print("Executando a função encontrar_tarefa_por_id")
    for t in tarefas:
        if t.get("id") == tid:
            return t
    return None

# -------------------------
# Operações do ciclo de vida (cada uma em função separada)
# -------------------------
def criar_tarefa():
    """
    Cria uma nova tarefa solicitando informações ao usuário,
    valida os dados e adiciona a tarefa à lista global de tarefas.
    Parâmetros: nenhum
    Retorno: nenhum
    """
    global tarefas, next_id
    print("Executando a função criar_tarefa")
    titulo = input("Título (obrigatório): ").strip()
    while not titulo:
        print("Título obrigatório. Informe novamente.")
        titulo = input("Título (obrigatório): ").strip()

    descricao = input("Descrição (opcional): ").strip()

    # Mostrar opções de prioridade
    print("Prioridades disponíveis: " + ", ".join(PRIORIDADES))
    prioridade_raw = input("Prioridade (obrigatório): ").strip()
    prioridade = validar_prioridade(prioridade_raw)
    while prioridade is None:
        print("Prioridade inválida. Opções válidas: " + ", ".join(PRIORIDADES))
        prioridade_raw = input("Prioridade (obrigatório): ").strip()
        prioridade = validar_prioridade(prioridade_raw)

    # Mostrar opções de origem
    print("Origens disponíveis: " + ", ".join(ORIGENS))
    origem_raw = input("Origem da Tarefa (obrigatório): ").strip()
    origem = validar_origem(origem_raw)
    while origem is None:
        print("Origem inválida. Opções válidas: " + ", ".join(ORIGENS))
        origem_raw = input("Origem da Tarefa (obrigatório): ").strip()
        origem = validar_origem(origem_raw)

    # Criar objeto tarefa
    tarefa = {
        "id": next_id,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "status": STATUS_PENDENTE,
        "origem": origem,
        "data_criacao": datetime.now(),
        "data_conclusao": None
    }
    tarefas.append(tarefa)
    print(f"Tarefa criada com ID {next_id}.")
    next_id += 1

def verificar_urgencia_e_pegar():
    """
    Verificação de urgência: busca a primeira tarefa com prioridade máxima (Urgente).
    Se nenhuma, busca pela próxima prioridade (Alta, Média, Baixa) na ordem.
    Depois de selecionar, atualiza status para "Fazendo" e retorna a tarefa.
    """
    print("Executando a função verificar_urgencia_e_pegar")
    # Ordem de prioridades: da mais alta à mais baixa
    for p in PRIORIDADES:
        for t in tarefas:
            if t["prioridade"] == p and t["status"] == STATUS_PENDENTE:
                t["status"] = STATUS_FAZENDO
                print(f"Tarefa selecionada (ID {t['id']}): {t['titulo']} - Prioridade: {p}")
                return t
    print("Não há tarefas pendentes para iniciar.")
    return None

def atualizar_prioridade():
    """
    Permite alterar a prioridade de uma tarefa após validar.
    """
    print("Executando a função atualizar_prioridade")
    try:
        tid = int(input("Informe o ID da tarefa a alterar prioridade: ").strip())
    except ValueError:
        print("ID inválido (deve ser numérico).")
        return
    t = encontrar_tarefa_por_id(tid)
    if not t:
        print("Tarefa não encontrada.")
        return
    print(f"Tarefa encontrada: {t['titulo']} (Prioridade atual: {t['prioridade']})")
    print("Prioridades válidas: " + ", ".join(PRIORIDADES))
    novo_raw = input("Nova prioridade: ").strip()
    novo = validar_prioridade(novo_raw)
    if novo is None:
        print("Prioridade inválida. Operação cancelada.")
        return
    t["prioridade"] = novo
    print(f"Prioridade da tarefa ID {tid} atualizada para {novo}.")

def concluir_tarefa():
    """
    Marca uma tarefa como concluída, registra data de conclusão e muda o status.
    """
    print("Executando a função concluir_tarefa")
    try:
        tid = int(input("Informe o ID da tarefa a concluir: ").strip())
    except ValueError:
        print("ID inválido.")
        return
    t = encontrar_tarefa_por_id(tid)
    if not t:
        print("Tarefa não encontrada.")
        return
    if t["status"] == STATUS_CONCLUIDA:
        print("Tarefa já está concluída.")
        return
    t["status"] = STATUS_CONCLUIDA
    t["data_conclusao"] = datetime.now()
    print(f"Tarefa ID {tid} marcada como '{STATUS_CONCLUIDA}' em {t['data_conclusao'].isoformat()}.")

def arquivar_tarefas_antigas():
    """
    Procura tarefas com status 'Concluída' há mais de uma semana e as arquiva:
    - Atualiza status para 'Arquivado'
    - Registra no arquivo tarefas_arquivadas.json
    - Remove da lista ativa (mas mantém histórico no arquivo)
    """
    global tarefas
    print("Executando a função arquivar_tarefas_antigas")
    agora = datetime.now()
    para_arquivar = []
    restantes = []
    for t in tarefas:
        if t.get("status") == STATUS_CONCLUIDA and isinstance(t.get("data_conclusao"), datetime):
            if agora - t["data_conclusao"] > timedelta(days=7):
                # marcar como arquivado
                t_copy = dict(t)
                t_copy["status"] = STATUS_ARQUIVADO
                para_arquivar.append(t_copy)
                # não adicionar a 'restantes' -> será removida da lista ativa
            else:
                restantes.append(t)
        else:
            restantes.append(t)
    if para_arquivar:
        # Registrar no arquivo de arquivadas
        registrar_em_arquivo_arquivadas(para_arquivar)
        tarefas = restantes
        print(f"{len(para_arquivar)} tarefas concluídas há mais de uma semana foram arquivadas.")
    else:
        print("Nenhuma tarefa para arquivar no momento.")

def excluir_tarefa_logica():
    """
    Marca uma tarefa com status 'Excluída' (exclusão lógica). Não remove da lista.
    """
    print("Executando a função excluir_tarefa_logica")
    try:
        tid = int(input("Informe o ID da tarefa a excluir (lógica): ").strip())
    except ValueError:
        print("ID inválido.")
        return
    t = encontrar_tarefa_por_id(tid)
    if not t:
        print("Tarefa não encontrada.")
        return
    t["status"] = STATUS_EXCLUIDA
    print(f"Tarefa ID {tid} marcada como '{STATUS_EXCLUIDA}'.")

# -------------------------
# Relatórios
# -------------------------
def relatorio_todas():
    """
    Exibe todas as tarefas no console. Para tarefas concluídas calcula tempo de execução.
    """
    print("Executando a função relatorio_todas")
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    for t in tarefas:
        print("-" * 40)
        print(f"ID: {t.get('id')}")
        print(f"Título: {t.get('titulo')}")
        print(f"Descrição: {t.get('descricao')}")
        print(f"Prioridade: {t.get('prioridade')}")
        print(f"Status: {t.get('status')}")
        print(f"Origem: {t.get('origem')}")
        dc = t.get("data_criacao")
        if isinstance(dc, datetime):
            print(f"Data de Criação: {dc.isoformat()}")
        else:
            print(f"Data de Criação: {dc}")
        if t.get("status") == STATUS_CONCLUIDA and isinstance(t.get("data_conclusao"), datetime):
            fim = t["data_conclusao"]
            print(f"Data de Conclusão: {fim.isoformat()}")
            # Calcular tempo de execução
            inicio = t.get("data_criacao")
            if isinstance(inicio, datetime):
                duracao = fim - inicio
                dias = duracao.days
                horas = duracao.seconds // 3600
                minutos = (duracao.seconds % 3600) // 60
                print(f"Tempo de execução: {dias} dias, {horas} horas, {minutos} minutos")
            else:
                print("Tempo de execução: dados de data incompletos.")
        else:
            if t.get("data_conclusao"):
                # pode haver string se carregado incorretamente
                print(f"Data de Conclusão: {t.get('data_conclusao')}")
        print("-" * 40)

def relatorio_arquivados():
    """
    Exibe lista de tarefas arquivadas a partir do arquivo tarefas_arquivadas.json.
    Tarefas excluídas não devem ser listadas aqui (arquivo de arquivadas NÃO recebe excluídas).
    """
    print("Executando a função relatorio_arquivados")
    try:
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            arquivadas = json.load(f)
    except Exception as e:
        print(f"Erro ao ler {ARCHIVE_FILE}: {e}")
        arquivadas = []

    if not arquivadas:
        print("Nenhuma tarefa arquivada registrada.")
        return

    for t in arquivadas:
        print("-" * 40)
        print(f"ID (original): {t.get('id')}")
        print(f"Título: {t.get('titulo')}")
        print(f"Descrição: {t.get('descricao')}")
        print(f"Prioridade: {t.get('prioridade')}")
        print(f"Status: {t.get('status')}")
        print(f"Origem: {t.get('origem')}")
        print(f"Data de Criação: {t.get('data_criacao')}")
        if t.get("data_conclusao"):
            print(f"Data de Conclusão: {t.get('data_conclusao')}")
        print("-" * 40)

# -------------------------
# Menu principal e fluxo
# -------------------------
def mostrar_menu():
    """
    Exibe todas as opções do sistema.
    """
    print("Executando a função mostrar_menu")
    print("\n=== Gerenciador de Tarefas ===")
    print("1 - Criar tarefa")
    print("2 - Verificar urgência e pegar próxima tarefa (iniciar)")
    print("3 - Atualizar prioridade de uma tarefa")
    print("4 - Concluir tarefa")
    print("5 - Arquivar tarefas concluídas há mais de 1 semana (limpeza automática)")
    print("6 - Excluir tarefa (lógica)")
    print("7 - Relatório: todas as tarefas")
    print("8 - Relatório: arquivadas")
    print("9 - Salvar e Sair")
    print("0 - Salvar e sair (forçado)")
    print("=============================")

def opcao_valida(op: str) -> bool:
    """
    Valida se a opção do menu existe.
    """
    print("Executando a função opcao_valida")
    validas = {str(i) for i in range(0, 10)}
    return op in validas

def menu_principal():
    """
    Corpo principal do programa: loop do menu e execução das funcionalidades.
    """
    print("Executando a função menu_principal")
    carregar_arquivos_iniciais()
    while True:
        mostrar_menu()
        opc = input("Escolha uma opção: ").strip()
        if not opcao_valida(opc):
            print("Opção inválida. Escolha uma das opções exibidas.")
            continue

        # Mapear opções para funções
        if opc == "1":
            criar_tarefa()
        elif opc == "2":
            verificar_urgencia_e_pegar()
        elif opc == "3":
            atualizar_prioridade()
        elif opc == "4":
            concluir_tarefa()
        elif opc == "5":
            arquivar_tarefas_antigas()
        elif opc == "6":
            excluir_tarefa_logica()
        elif opc == "7":
            relatorio_todas()
        elif opc == "8":
            relatorio_arquivados()
        elif opc in ("9", "0"):
            # Antes de sair, arquivar tarefas antigas também para manter consistência
            arquivar_tarefas_antigas()
            salvar_dados()
            print("Dados salvos. Encerrando o programa.")
            exit(0)

        # Após cada ação, pedir para salvar automaticamente (opcional) ou apenas continuar.
        # Para robustez, captura de exceções no loop principal poderia ser adicionada.
        # Aqui usando try/except para evitar crash por erro inesperado em qualquer função.
        try:
            # pequena limpeza automática a cada iteração: arquivar antigas
            arquivar_tarefas_antigas()
        except Exception as e:
            print(f"Erro durante limpeza automática: {e}")

# -------------------------
# Execução do script
# -------------------------
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Salvando dados antes de sair...")
        try:
            arquivar_tarefas_antigas()
            salvar_dados()
        except Exception as e:
            print(f"Erro ao salvar na saída: {e}")
        exit(0)
