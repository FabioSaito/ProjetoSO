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
        # if self.policy == 'FirstFit':
        #     # print
        # elif self.policy == 'BestFit':
        #     # print
        # elif self.policy == 'WorstFit':
        #     # print()
        # else
        #     print("Politica de alocacao invalida")
        position, space = check_max_free_space(self.policy, job)
        # print("Maior espaco encontrado:", space, "Na posicao:", position)

        aloca_mem(job,position)


    def remove_job(self, job):
        print("antes", settings.memory_space)
        desaloca_mem(job)
        jobExecutionOver.remove(job)
        job.state = 'Job Successfully Executed!'
        print("depois", settings.memory_space)

    def allocateJob(self):
        # PRECISA IMPLEMENTAR A VERIFICACAO DE MULTIPROGRAMACAO
        # job.memoryReq len(jobQueue)
        for (index, item) in enumerate(jobQueue):
            # Insere o Job da Fila de Espera para a memoria: 2 -> 3
            positionAvailable, spaceAvailable = check_max_free_space(self.policy, jobQueue[0])
            print("espaco :", spaceAvailable, "posicao:", positionAvailable)
            print("tam job :", jobQueue[0].memoryReq, "espaco disponivel:", spaceAvailable)
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
            if (job.memoryReq == blank_count and policy == 'FirstFit'):
                return blank_count_position, blank_count
        else:
            if blank_count > blank_count_max:
                blank_count_position_max = blank_count_position
                blank_count_max = blank_count
            blank_count = 0

        if blank_count > blank_count_max:
            blank_count_position_max = blank_count_position
            blank_count_max = blank_count
        # print(content, "|" , blank_count_position_max, blank_count_max)
    return blank_count_position_max, blank_count_max

"""def check_max_free_space():
    # settings.memory_space[0] = 1
    # settings.memory_space[15] = 1
    # settings.memory_space[28] = 1
    blank_count = 0
    blank_count_max = 0
    blank_count_position = 0
    blank_count_position_max = 0

    for (index, content) in enumerate(settings.memory_space):
        if content == 0:
            if blank_count == 0:
                blank_count_position = index
            blank_count += 1
        else:
            if blank_count > blank_count_max:
                blank_count_position_max = blank_count_position
                blank_count_max = blank_count
            blank_count = 0
        # print(content, "|" , blank_count_position_max, blank_count_max)
    return blank_count_position_max, blank_count_max
"""

def imprima_lista(listToPrint, listName):
    printList = []
    for item in listToPrint:
        printList.insert(len(printList), item.name)
    print("Lista",listName, ":" , printList)

def handle_processor_execution():
    if len(jobReadyToProcess) and settings.number_of_processors > len(jobExecution):
        jobExecution.append(jobReadyToProcess.pop(0))


    for (index, item) in enumerate(jobExecution):
        item.process_job()
        print("-- processando:", item.name, "- tempo restante:", item.processTime)

        # Termina o processamento do Job
        if item.processTime == 0:
            jobExecutionOver.append(jobExecution.pop(index))
            print("-- processamento do :", item.name, "finalizado!")


def handle_memory_allocation():
    print()



    """for item in jobExecution:
        item.process_job()
        print("-- processando:", item.name, "- tempo restante:", item.processTime)
        # Termina o processamento do Job
        if item.processTime == 0:
            # jobExecution.remove(item)
            jobExecutionOver.append(jobExecution.pop(item))
            print("-- processamento do :", item.name, "finalizado!")
        # print(item.name)"""


if __name__ == '__main__':
    settings.init()
    settings.memory_space[1] = 1
    # settings.memory_space[12] = 1
    settings.memory_space[28] = 1

    # multiProgram = getMultProgram()
    # typeProcess = getTypeProcess()
    typeProcess = "1"
    # typeMemory = getTypeMemory()

    # print("multiProgram: ", multiProgram)
    print("typeProcess: ", typeProcess)

    ################################## NUMERO DE PROCESSADORES ##########################################
    settings.number_of_processors = 1

    # job0 = job(name, arrivalTime, processTime, memoryReq, state, memPosition)
    job0 = JobT('Partida', 0, 0, 0, 'wEntry', -1)

    # job1 = jobT('job1', 50, 15, 60, 'wEntry')
    # job2 = jobT('job2', 43, 17, 32, 'wEntry')
    # job3 = jobT('job3', 36, 7, 64, 'wEntry')
    # job4 = jobT('job4', 5, 23, 16, 'wEntry')
    # job5 = jobT('job5', 200, 52, 28, 'wEntry')
    # job6 = jobT('job6', 34, 55, 65, 'wEntry')

    job1 = JobT('job1', 10, 120, 5, 'wEntry', -1)
    job2 = JobT('job2', 15, 60, 25, 'wEntry', -1)
    job3 = JobT('job3', 30, 15, 3, 'wEntry', -1)

    job999 = JobT('Final', 249, 999, 999, 'wEntry', -1)

    memManager = memoryManager('Gerenciador de Memoria', 'FirstFit')
    # memManager = memoryManager('Gerenciador de Memoria', 'WorstFit')

    jobList = [job0, job1, job2, job3, job999]
    # 2-> 3
    jobQueue = []
    # 3-> 4
    jobReadyToProcess = []
    # 4
    jobExecution = []
    # 4-> 5
    jobExecutionOver = []

    # if (typeProcess == "1"):  # FIFO
    #     jobList = sorted(jobList, key=lambda x: x.arrivalTime)
    # elif (typeProcess == "2"):  # Job mais curto
    #     jobList = sorted(jobList, key=lambda x: x.processTime)


    print("print depois")
    for item in jobList:
        print(item.name, item.arrivalTime, item.memoryReq)

    currentJob = 1
    # jobC = jobQueue[currentJob]

    """ _______________________________________________________________________________________
        INICIO DA SIMULACAO
        _______________________________________________________________________________________
    """
    while settings.time < 250:
        print("\n ------------------------------------------time", settings.time)
        print(settings.memory_space)
        for item in jobList:
            if item.arrivalTime == settings.time:
                if (item.name == 'Partida'):
                    print("Inicio da Simulacao!")
                elif (item.name == 'Final'):
                    print("Final da Simulacao!")
                    # exit()
                else:
                    jobQueue.insert(len(jobQueue), item)
                    if (typeProcess == "1"):  # FIFO
                        jobQueue = sorted(jobQueue, key=lambda x: x.arrivalTime)
                    elif (typeProcess == "2"):  # Job mais curto
                        jobQueue = sorted(jobQueue, key=lambda x: x.processTime)
                # print("Job Chegou!", item.name, item.arrivalTime, time)
                imprima_lista(jobQueue, "Fila de Espera para entrar no sistema")


        ########################################## LOADER ##########################################

        if len(jobQueue)> 0:
            imprima_lista(jobQueue, "memManager.allocateJob()")
            memManager.allocateJob()

        ########################################## PROCESSADOR ##########################################
        if (len(jobReadyToProcess) + len(jobExecution)) > 0:
            print("processando jobs:")
            handle_processor_execution()
            imprima_lista(jobExecution, "fila de execucao")

        ########################################## Fim De Processamento ##########################################
        for item in jobExecutionOver:
            print("nome do job:", item.name)
            memManager.remove_job(item)


        # for item in jobQueue:
        #     if (item.jobState == 'executing'):
        #         item.process_job()

        # print(item.name, item.arrivalTime, item.memoryReq)

        # if jobC.processTime == 0 :
        #     #print("job finalizado||", jobC.processTime, jobC.name)
        #     currentJob += 1
        #     jobC = jobQueue[currentJob]

        # print("Job em processamento:", jobC.name, "- tempo restante:", jobC.processTime)
        # jobC.process_job()

        settings.time += 1


    """
    # PAGINACAO DE MEMORIA
    jobInProcess = job1
    numberOfPages = math.ceil(jobInProcess.memoryReq / len(memory_space))
    print("Numero de paginas a serem criadas: ", numberOfPages)
    print("Tamanho da pagina criada: ", jobInProcess.memoryReq / numberOfPages)
    """
