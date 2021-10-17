import settings
from ME_functions import *
import math


class JobT(object):
    def __init__(self, name, arrivalTime, processTime, memoryReq, state, memPosition) -> None:
        super().__init__()
        self.name = name
        self.arrivalTime = arrivalTime
        self.processTime = processTime
        self.memoryReq = memoryReq
        self.state = state
        self.memPosition = memPosition

    def process_job(self):
        self.processTime -= 1

class memoryManager(object):
    def __init__(self, name, policy) -> None:
        super().__init__()
        self.name = name
        self.policy = policy

    # É o LOADER de fato, apenas recebe o job e insere na posicao de memoria, sem verificar nada
    def load_job(self, job):
        position, space = check_max_free_space(self.policy, job)
        aloca_mem(job,position)

    def remove_job(self, job):
        desaloca_mem(job)
        jobExecutionOver.remove(job)
        job.state = 'Job Successfully Executed!'
        # print("depois", settings.memory_space)

    def allocateJob(self):
        # PRECISA IMPLEMENTAR A VERIFICACAO DE MULTIPROGRAMACAO
        for (index, item) in enumerate(jobQueue):
            # Insere o Job da Fila de Espera para a memoria: 2 -> 3
            positionAvailable, spaceAvailable = check_max_free_space(self.policy, jobQueue[0])
            # print("espaco :", spaceAvailable, "posicao:", positionAvailable)
            # print("tam job :", jobQueue[0].memoryReq, "espaco disponivel:", spaceAvailable)
            if (jobQueue[0].memoryReq <= spaceAvailable):
                temp_job = jobQueue.pop(0)
                temp_job.memPosition = positionAvailable
                jobReadyToProcess.append(temp_job)
                self.load_job(temp_job)

def check_max_free_space(policy, job):
    blank_count = 0
    blank_count_max = 0
    blank_count_position = 0
    blank_count_position_max = 0

    for (index, content) in enumerate(settings.memory_space):
        if content == 0:
            if blank_count == 0:
                blank_count_position = index
            blank_count += 1
            if (job.memoryReq == blank_count and policy == 'First-Fit'):
                return blank_count_position, blank_count
        else:
            if blank_count > blank_count_max:
                blank_count_position_max = blank_count_position
                blank_count_max = blank_count
            blank_count = 0

        if blank_count > blank_count_max:
            blank_count_position_max = blank_count_position
            blank_count_max = blank_count
    return blank_count_position_max, blank_count_max

def imprima_lista(listToPrint, listName):
    printList = []
    for item in listToPrint:
        printList.insert(len(printList), item.name)
    print(listName, ":" , printList)

def handle_processor_execution():
    if len(jobReadyToProcess) and settings.number_of_processors > len(jobExecution):
        jobExecution.append(jobReadyToProcess.pop(0))
    for (index, item) in enumerate(jobExecution):
        item.process_job()
        print("| processando:", item.name, "- tempo restante:", item.processTime, "|")
        # Termina o processamento do Job
        if item.processTime == 0:
            jobExecutionOver.append(jobExecution.pop(index))
            print("Processamento do :", item.name, "finalizado!")


def handle_memory_allocation():
    print()

typeProcessList = {
  "1": "FIFO",
  "2": "Jobs mais curtos"
}
typeMemoryList = {
  "1": "AlocacaoContiguaSimples",
  "2": "First-Fit",
  "3": "Worst-Fit"
}
if __name__ == '__main__':
    settings.init()

    multiProgram = getMultProgram()
    typeProcess = getTypeProcess()
    typeMemory = getTypeMemory()
    # multiProgram = "1"
    # typeProcess = "1"
    # typeMemory = "1"

    print("\nInciando uma simulação para as seguintes configurações: ")
    print("Prioridade de processamento:", typeProcessList[typeProcess])
    print("Alocacao de memoria:", typeMemoryList[typeMemory])
    print("Grau de multiprogracao:", multiProgram)

    #################### NUMERO DE PROCESSADORES ####################
    settings.number_of_processors = int(multiProgram)

    job0 = JobT('Partida', 0, 0, 0, 'wEntry', -1) # Job de controle da simulação
    job1 = JobT('job1', 4, 394, 1, 'wEntry', -1)
    job2 = JobT('job2', 342, 3, 1, 'wEntry', -1)
    job3 = JobT('job3', 4, 28, 1, 'wEntry', -1)
    job4 = JobT('job4', 177, 47, 1, 'wEntry', -1)
    job5 = JobT('job5', 72, 377, 1, 'wEntry', -1)
    job6 = JobT('job6', 229, 201, 1, 'wEntry', -1)

    # job1 = JobT('job1', 10, 120, 5, 'wEntry', -1)
    # job2 = JobT('job2', 15, 60, 25, 'wEntry', -1)
    # job3 = JobT('job3', 30, 15, 3, 'wEntry', -1)

    job999 = JobT('Final', 1299, 999, 999, 'wEntry', -1) # Job de controle da simulação

    memManager = memoryManager('Gerenciador de Memoria', typeMemoryList[typeMemory])

    #################### FILAS DE CONTROLE ####################
    # Todos os jobs a serem executados
    jobList = [job0, job1, job2, job3, job4, job5, job6, job999]
    # 2-> 3
    jobQueue = []
    # 3-> 4
    jobReadyToProcess = []
    # 4
    jobExecution = []
    # 4-> 5
    jobExecutionOver = []

    """ -------------------------------------------------------------------------------------
        INICIO DA SIMULACAO
        -------------------------------------------------------------------------------------
    """
    while settings.time < 1300:
        print("\n ------------------------------------------ time", settings.time)
        print("mapa de memoria:", settings.memory_space)
        for item in jobList:
            if item.arrivalTime == settings.time:
                if (item.name == 'Partida'):
                    print("Inicio da Simulacao!")
                elif (item.name == 'Final'):
                    print("Final da Simulacao!")
                    # print("Saindo...")
                    # exit()
                else:
                    jobQueue.insert(len(jobQueue), item)
                    if (typeProcess == "1"):  # FIFO
                        jobQueue = sorted(jobQueue, key=lambda x: x.arrivalTime)
                    elif (typeProcess == "2"):  # Job mais curto
                        jobQueue = sorted(jobQueue, key=lambda x: x.processTime)
                # imprima_lista(jobQueue, "Fila de Espera para entrar no sistema")


        #################### GERENCIADOR DE MEMORIA ####################
        if len(jobQueue)> 0:
            imprima_lista(jobQueue, "Jobs na fila para serem alocados em memória")
            memManager.allocateJob()

        #################### GERENCIADOR DE PROCESSAMENTO ####################
        if (len(jobReadyToProcess) + len(jobExecution)) > 0:
            # print("processando jobs:")
            handle_processor_execution()
            imprima_lista(jobExecution, "Jobs em execução")

        #################### FIM DE PROCESSAMENTO ####################
        for item in jobExecutionOver:
            # print("nome do job:", item.name)
            memManager.remove_job(item)

        settings.time += 1


    """
    # PAGINACAO DE MEMORIA
    jobInProcess = job1
    numberOfPages = math.ceil(jobInProcess.memoryReq / len(memory_space))
    print("Numero de paginas a serem criadas: ", numberOfPages)
    print("Tamanho da pagina criada: ", jobInProcess.memoryReq / numberOfPages)
    """
