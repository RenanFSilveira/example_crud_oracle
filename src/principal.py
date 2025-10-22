import os
import time
from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_paciente import ControllerPaciente
from controller.controller_medico import ControllerMedico
from controller.controller_consulta import ControllerConsulta 

# Função auxiliar para limpar o console
def limpar_console(segundos=0):
    """
    Função auxiliar para limpar o console após um pequeno atraso (se fornecido).
    """
    time.sleep(segundos)
    # Comando para limpar o console (funciona em Windows e Linux/Mac)
    os.system('cls' if os.name == 'nt' else 'clear')

# Instanciação dos objetos globais
tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_paciente = ControllerPaciente()
ctrl_medico = ControllerMedico()
ctrl_consulta = ControllerConsulta()

def reports(opcao_relatorio:int=0):
    """
    Orquestra a execução dos relatórios solicitados pelo usuário.
    """
    if opcao_relatorio == 1:
        # 1 - Consultas por Especialidade (Sumarização)
        relatorio.get_relatorio_sumarizacao() 
        input("Digite qualquer tecla para continuar.")
    elif opcao_relatorio == 2:
        # 2 - Consultas Agendadas Detalhadas (Junção)
        relatorio.get_relatorio_juncao() 
        input("Digite qualquer tecla para continuar.")
    elif opcao_relatorio == 0:
        return
    else:
        print("Opção inválida.")
    
    limpar_console(1) # Limpa o console após a exibição do relatório

def inserir(opcao_inserir:int=0):
    """
    Orquestra a inserção de registros nas entidades.
    """
    if opcao_inserir == 1:
        ctrl_paciente.inserir_paciente()
    elif opcao_inserir == 2:
        ctrl_medico.inserir_medico()
    elif opcao_inserir == 3:
        ctrl_consulta.inserir_consulta()
    
    limpar_console(1)

def atualizar(opcao_atualizar:int=0):
    """
    Orquestra a atualização de registros nas entidades.
    """
    if opcao_atualizar == 1:
        ctrl_paciente.atualizar_paciente()
    elif opcao_atualizar == 2:
        ctrl_medico.atualizar_medico()
    elif opcao_atualizar == 3:
        ctrl_consulta.atualizar_consulta()
    
    limpar_console(1)

def excluir(opcao_excluir:int=0):
    """
    Orquestra a exclusão de registros nas entidades.
    """
    if opcao_excluir == 1:
        ctrl_paciente.excluir_paciente()
    elif opcao_excluir == 2:
        ctrl_medico.excluir_medico()
    elif opcao_excluir == 3:
        ctrl_consulta.excluir_consulta()
    
    limpar_console(1)

def run():
    """
    Função principal que inicia e mantém o ciclo de execução do sistema.
    """
    # Exibe a splash screen inicial
    limpar_console()
    print(tela_inicial.get_updated_screen())
    limpar_console(3) # Espera 3 segundos e limpa para exibir o menu principal

    while True:
        limpar_console()
        print(config.MENU_PRINCIPAL)
        
        try:
            opcao = int(input("Escolha uma opção [1-5]: "))
        except ValueError:
            print("Digite um número válido.")
            limpar_console(1)
            continue

        limpar_console(1)

        if opcao == 1: # Relatórios
            print(config.MENU_RELATORIOS)
            try:
                opcao_relatorio = int(input("Escolha uma opção [0-2]: "))
            except ValueError:
                print("Digite um número válido.")
                limpar_console(1)
                continue
            
            limpar_console(1)
            reports(opcao_relatorio)
            
        elif opcao == 2: # Inserir
            print(config.MENU_ENTIDADES)
            try:
                opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            except ValueError:
                print("Digite um número válido.")
                limpar_console(1)
                continue

            inserir(opcao_inserir)
            
        elif opcao == 3: # Atualizar
            print(config.MENU_ENTIDADES)
            try:
                opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            except ValueError:
                print("Digite um número válido.")
                limpar_console(1)
                continue

            atualizar(opcao_atualizar)
            
        elif opcao == 4: # Excluir
            print(config.MENU_ENTIDADES)
            try:
                opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            except ValueError:
                print("Digite um número válido.")
                limpar_console(1)
                continue
            
            excluir(opcao_excluir)
            
        elif opcao == 5: # Sair
            print("Obrigado por utilizar o sistema!")
            limpar_console(2)
            exit(0)

        else:
            print("Opção incorreta. Pressione Enter para tentar novamente...")
            input() # Pausa
            
if __name__ == "__main__":
    run()