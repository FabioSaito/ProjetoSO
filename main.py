import settings
from ME_functions import *
import math

class JobT(object):
    def __init__(self, name, arrivalTime, processTime, memoryReq, state, memPosition, timeExit, timeArriveProcessor) -> None:
        super().__init__()
        self.name = name
        self.arrivalTime = arrivalTime
        self.processTime = processTime
        self.memoryReq = memoryReq
        self.state = state
        self.memPosition = memPosition
        self.timeExit = timeExit
        self.timeArriveProcessor = timeArriveProcessor

    def process_job(self, time):
        self.processTime -= time

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
            if len(jobQueue) and settings.number_of_processors > (len(jobReadyToProcess) + len(jobExecution)):
                # Insere o Job da Fila de Espera para a memoria: 2 -> 3
                positionAvailable, spaceAvailable = check_max_free_space(self.policy, jobQueue[0])
                # print("espaco :", spaceAvailable, "posicao:", positionAvailable)
                # print("tam job :", jobQueue[0].memoryReq, "espaco disponivel:", spaceAvailable)
                if (jobQueue[0].memoryReq <= spaceAvailable):
                    temp_job = jobQueue.pop(0)
                    temp_job.memPosition = positionAvailable
                    jobReadyToProcess.append(temp_job)
                    self.load_job(temp_job)
    # def allocateJob(self):
    #     # PRECISA IMPLEMENTAR A VERIFICACAO DE MULTIPROGRAMACAO
    #     for (index, item) in enumerate(jobQueue):
    #         # Insere o Job da Fila de Espera para a memoria: 2 -> 3
    #         positionAvailable, spaceAvailable = check_max_free_space(self.policy, jobQueue[0])
    #         # print("espaco :", spaceAvailable, "posicao:", positionAvailable)
    #         # print("tam job :", jobQueue[0].memoryReq, "espaco disponivel:", spaceAvailable)
    #         if (jobQueue[0].memoryReq <= spaceAvailable):
    #             temp_job = jobQueue.pop(0)
    #             temp_job.memPosition = positionAvailable
    #             jobReadyToProcess.append(temp_job)
    #             self.load_job(temp_job)

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
        temp_job_to_processor = jobReadyToProcess.pop(0)
        temp_job_to_processor.timeArriveProcessor = settings.time

        jobExecution.append(temp_job_to_processor)
    for (index, item) in enumerate(jobExecution):
        quantum_time = 1/len(jobExecution)
        print("time_slice:", quantum_time, "- jobs em execucao:", len(jobExecution))
        item.process_job(quantum_time)
        print("| processando:", item.name, "- tempo restante:", item.processTime, "|")
        # Termina o processamento do Job
        if item.processTime <= 0:
            item.timeExit = settings.time + 1
            jobExecutionOver.append(jobExecution.pop(index))
            print("Processamento do :", item.name, "finalizado!")

# def handle_processor_execution():
#     if len(jobReadyToProcess) and settings.number_of_processors > len(jobExecution):
#         jobExecution.append(jobReadyToProcess.pop(0))
#     for (index, item) in enumerate(jobExecution):
#         item.process_job()
#         print("| processando:", item.name, "- tempo restante:", item.processTime, "|")
#         # Termina o processamento do Job
#         if item.processTime == 0:
#             jobExecutionOver.append(jobExecution.pop(index))
#             print("Processamento do :", item.name, "finalizado!")

# def handle_memory_allocation():
#     print()

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
    print("Grau de multiprogramação:", multiProgram)

    #################### NUMERO DE PROCESSADORES ####################
    settings.number_of_processors = int(multiProgram)
    # job = job(name, arrivalTime, processTime, memoryReq, state, memPosition, timeExit)
    job0 = JobT('Partida', 0, 0, 0, 'wEntry', -1, -9999, -9999) # Job de controle da simulação


    # job1 = JobT('job1', 4, 394, 1, 'wEntry', -1, -9999, -9999)
    # job2 = JobT('job2', 342, 3, 1, 'wEntry', -1, -9999, -9999)
    # job3 = JobT('job3', 4, 28, 1, 'wEntry', -1, -9999, -9999)
    # job4 = JobT('job4', 177, 47, 1, 'wEntry', -1, -9999, -9999)
    # job5 = JobT('job5', 72, 377, 1, 'wEntry', -1, -9999, -9999)
    # job6 = JobT('job6', 229, 201, 1, 'wEntry', -1, -9999, -9999)


    # job1 = JobT('job1', 10, 120, 5, 'wEntry', -1)
    # job2 = JobT('job2', 15, 60, 25, 'wEntry', -1)
    # job3 = JobT('job3', 30, 15, 3, 'wEntry', -1)

    # job1 = JobT('job1', 600, 120, 1, 'wEntry', -1, -9999, -9999)
    # job2 = JobT('job2', 606, 60, 1, 'wEntry', -1, -9999, -9999)
    # job3 = JobT('job3', 615, 15, 1, 'wEntry', -1, -9999, -9999)
    #
    job1 = JobT('job1', 600, 18, 1, 'wEntry', -1, -9999, -9999)
    job2 = JobT('job2', 612, 30, 1, 'wEntry', -1, -9999, -9999)
    job3 = JobT('job3', 624,  6, 1, 'wEntry', -1, -9999, -9999)
    job4 = JobT('job4', 630, 24, 1, 'wEntry', -1, -9999, -9999)
    job5 = JobT('job5', 648,  6, 1, 'wEntry', -1, -9999, -9999)

    job999 = JobT('Final', 1299, 999, 999, 'wEntry', -1, -9999, -9999) # Job de controle da simulação

    memManager = memoryManager('Gerenciador de Memoria', typeMemoryList[typeMemory])

    #################### FILAS DE CONTROLE ####################
    # Todos os jobs a serem executados
    # jobList = [job0, job1, job2, job3, job4, job5, job6, job999]
    jobList = [job0, job1, job2, job3, job4, job5, job999]

    # 2
    jobQueue = []
    # 3
    jobReadyToProcess = []
    # 4
    jobExecution = []
    # 5
    jobExecutionOver = []

    """ -------------------------------------------------------------------------------------
        INICIO DA SIMULACAO
        -------------------------------------------------------------------------------------
    """
    while settings.time < 1300:
        print("\n ------------------------------------------ time", settings.time)

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

        print("mapa de memoria:", settings.memory_space)
        # imprima_lista(jobList, "- Fila 1")
        # imprima_lista(jobQueue, "- Fila 2")
        # imprima_lista(jobReadyToProcess, "- Fila 3")
        # imprima_lista(jobExecution, "- Fila 4")
        # imprima_lista(jobExecutionOver, "- Fila 5")

        if settings.time == 1299:
            turnaround = 0
            t_ponderado = 0
            process_count = 0
            for item in jobList:
                if (item.name != 'Partida') and (item.name != 'Final'):
                    turnaround = turnaround + (item.timeExit - item.arrivalTime)
                    t_ponderado = t_ponderado + (turnaround/(item.timeExit - item.timeArriveProcessor))
                    print(item.name, "- finalizado em:", item.timeExit, "- T:", turnaround/60, "- W:", turnaround/60)
                    process_count += 1

            turnaround_medio = turnaround/process_count
            print("process_count:", process_count)
            print("turnaround_medio:", turnaround_medio/60)
            print("turnaround_medio)ponderado:", t_ponderado/60)
        settings.time += 1


    """
    # PAGINACAO DE MEMORIA
    jobInProcess = job1
    numberOfPages = math.ceil(jobInProcess.memoryReq / len(memory_space))
    print("Numero de paginas a serem criadas: ", numberOfPages)
    print("Tamanho da pagina criada: ", jobInProcess.memoryReq / numberOfPages)
    """
