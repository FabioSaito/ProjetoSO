import settings
from ME_functions import *
import math


class jobT(object):
    def __init__(self, name, arrivalTime, processTime, memoryReq, state) -> None:
        super().__init__()
        self.name = name
        self.arrivalTime = arrivalTime
        self.processTime = processTime
        self.memoryReq = memoryReq
        self.state = state

    def process_job(self):
        self.processTime -= 1


def imprimaListaJobs(listToPrint):
    printList = []
    for item in listToPrint:
        printList.insert(len(printList), item.name)
    print("Lista: ", printList)



if __name__ == '__main__':
    settings.init()

    # multiProgram = getMultProgram()
    # typeProcess = getTypeProcess()
    typeProcess = "1"
    # typeMemory = getTypeMemory()

    # print("multiProgram: ", multiProgram)
    print("typeProcess: ", typeProcess)

    # job(name, arrivalTime, processTime, memoryReq, state)
    job0 = jobT('Partida', 0, 0, 0, 'wEntry')
    job1 = jobT('job1', 50, 15, 60, 'wEntry')
    job2 = jobT('job2', 43, 17, 32, 'wEntry')
    job3 = jobT('job3', 36, 7, 64, 'wEntry')
    job4 = jobT('job4', 10, 23, 16, 'wEntry')
    job5 = jobT('job5', 200, 52, 28, 'wEntry')
    job6 = jobT('job6', 34, 55, 65, 'wEntry')
    job999 = jobT('Final', 999, 999, 999, 'wEntry')

    jobList = [job0, job1, job2, job3, job4, job5, job6, job999]
    jobQueue = []

    if (typeProcess == "1"):  # FIFO
        jobList = sorted(jobList, key=lambda x: x.arrivalTime)
    elif (typeProcess == "2"):  # Job mais curto
        jobList = sorted(jobList, key=lambda x: x.memoryReq)

    print("print depois")
    for item in jobList:
        print(item.name, item.arrivalTime, item.memoryReq)

    currentJob = 1
    # jobC = jobQueue[currentJob]

    """ _______________________________________________________________________________________
        INICIO DA SIMULACAO
        _______________________________________________________________________________________
    """
    while settings.time < 1000:
        for item in jobList:
            if item.arrivalTime == settings.time:
                if (item.name == 'Partida'):
                    print("Inicio da Simulacao!")
                elif (item.name == 'Final'):
                    print("Final da Simulacao!")
                    exit()
                else:
                    jobQueue.insert(len(jobQueue), item)
                # print("Job Chegou!", item.name, item.arrivalTime, time)
                imprimaListaJobs(jobQueue)
        printaProc()
        settings.number_of_processors = 2
        printaProc()
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

        # LOADER
        # aloca_mem(job1, positionT)
        # print(memory_space)

        print("time1", settings.time)
        settings.time += 1

    # print("job4 - antes", jobList[3].name,  jobList[3].processTime)
    # jobList[3].processTime = jobList[3].processTime -1
    # print("job4 - depois", jobList[3].name,  jobList[3].processTime)

    """
    # PAGINACAO DE MEMORIA
    jobInProcess = job1
    numberOfPages = math.ceil(jobInProcess.memoryReq / len(memory_space))
    print("Numero de paginas a serem criadas: ", numberOfPages)
    print("Tamanho da pagina criada: ", jobInProcess.memoryReq / numberOfPages)
    """
