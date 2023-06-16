import peoplemodel_random

if __name__ == '__main__':
    friendModel = peoplemodel_random.PeopleModel(200,30,30)
    for i in range(500):
        friendModel.step()
        if(i%10 ==1):
            print(f'10 batches passed')