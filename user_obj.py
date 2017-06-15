class User(object):
    def __init__(self,userName,password):
        self.userName = userName
        self.password = password
    def __str__(self):
        return str('userName=%s,password=%s' % (self.userName,self.password))


if __name__ == '__main__':
    user1 = User('heishan','123')
    print user1.__str__()