from ME_functions import *
class jobT(object):
    def __init__(self, name, arrivalTime, processTime, memoryReq) -> None:
        super().__init__()
        self.name = name
        self.arrivalTime = arrivalTime
        self.processTime = processTime
        self.memoryReq = memoryReq

    def process_job(self):
        self.processTime -= 1


def aloca_mem(job, position):
    memory_space[position:position + job.memoryReq] = [job.name] * job.memoryReq


memory_space = [0] * 128
nucleos_processador = 1

if __name__ == '__main__':
    job1 = jobT('job1', 5, 15, 16)
    job2 = jobT('job2', 4, 17, 32)
    job3 = jobT('job3', 3, 7, 64)
    job4 = jobT('job4', 1, 23, 16)
    job5 = jobT('job5', 2, 52, 128)

    jobList = [job1, job2, job3, job4, job5]

    jobList = sorted(jobList, key=lambda x: x.name)

    for item in jobList:
        print(item.name, item.processTime)

    positionT = 10
    aloca_mem(job1, positionT)

    # for time in range(1000):
    #     print(time)

    print(memory_space)


