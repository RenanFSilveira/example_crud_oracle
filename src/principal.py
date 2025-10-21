from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_paciente import Controller_Paciente
from controller.controller_medico import Controller_Medico
from controller.controller_consulta import Controller_Consulta
tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_paciente = Controller_Paciente()
ctrl_medico = Controller_Medico()
ctrl_consulta = Controller_Consulta()

def reports(opcao_relatorio:int=0):
    if opcao_relatorio == 1:
        relatorio.get_relatorio_consultas_por_medico()   
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_consultas_detalhado()    
    elif opcao_relatorio == 0:
        return
    else:
        print("Opção inválida.")

def inserir(opcao_inserir:int=0):
    if opcao_inserir == 1:
        ctrl_paciente.inserir_paciente()
    elif opcao_inserir == 2:
        ctrl_medico.inserir_medico()
    elif opcao_inserir == 3:
        ctrl_consulta.inserir_consulta()

def atualizar(opcao_atualizar:int=0):
    if opcao_atualizar == 1:
        ctrl_paciente.atualizar_paciente()
    elif opcao_atualizar == 2:
        ctrl_medico.atualizar_medico()
    elif opcao_atualizar == 3:
        ctrl_consulta.atualizar_consulta()

def excluir(opcao_excluir:int=0):
    if opcao_excluir == 1:
        ctrl_paciente.excluir_paciente()
    elif opcao_excluir == 2:
        ctrl_medico.excluir_medico()
    elif opcao_excluir == 3:
        ctrl_consulta.excluir_consulta()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        try:
            opcao = int(input("Escolha uma opção [1-5]: "))
        except ValueError:
            print("Digite um número válido.")
            config.clear_console(1)
            continue

        config.clear_console(1)

        if opcao == 1: # Relatórios
            print(config.MENU_RELATORIOS)
            try:
                opcao_relatorio = int(input("Escolha uma opção [0-2]: "))
            except ValueError:
                print("Digite um número válido.")
                config.clear_console(1)
                continue
            config.clear_console(1)
            reports(opcao_relatorio)
            config.clear_console(1)

        elif opcao == 2: # Inserir
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            inserir(opcao_inserir)
            config.clear_console()

        elif opcao == 3: # Atualizar
            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            atualizar(opcao_atualizar)
            config.clear_console()

        elif opcao == 4: # Excluir
            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            excluir(opcao_excluir)
            config.clear_console()

        elif opcao == 5: # Sair
            print("Obrigado por utilizar o sistema!")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()