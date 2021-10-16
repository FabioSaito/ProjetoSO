import settings
def aloca_mem(job, position):
    settings.memory_space[position:position + job.memoryReq] = [job.name] * job.memoryReq

def getMultProgram():
    varMult = input("Deseja multiprogramação? (s/n) \n")
    if (varMult == "n"):
        return 0
    elif (varMult == "s"):
        return input("Escolha seu grau multiprogramação: ")


def getTypeProcess():
    print("\nTipos de Processamento Disponiveis:")
    print("1 - FIFO:")
    print("2 - Jobs mais curtos:")
    varProcess = input("Escolha o tipo de administracao de processamento: ")
    return varProcess


def getTypeMemory():
    print("\nTipos de Processamento Disponiveis:")
    print("1 - Alocação Contígua Simples:")
    print("2 - Memória particionada estática, best-fit:")
    print("3 - Memória particionada estática, first-fit:")
    print("3 - Overlay:")
    varMemory = input("Escolha o tipo de administracao de processamento: ")
    return varMemory

def printaProc():
    print("number_of_processors: ", settings.number_of_processors, settings.time)
