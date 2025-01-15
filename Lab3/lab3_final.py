class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__user_account = []
        self.__user_card = []
    @property
    def get_account(self):
        return self.__user_account
    @get_account.setter
    def add_account(self, account):
        self.__user_account.append(account)
    
    def add_atm_card(self, atm_card):
        self.__user_card.append(atm_card)

    
class Account:
    def __init__(self, account_number: str, owner: User , balance: int):
        self.__account_number = account_number
        self.__owner = owner
        self.__balance = balance
        self.__transaction = []
        self.__atmcard = None
    @property
    def get_card(self):
        return self.__atmcard
    @get_card.setter
    def add_card(self, card):
        self.__atmcard = card
    @property
    def get_balance(self):
        return self.__balance
    @get_balance.setter
    def update_balance(self, amount):
        self.__balance += amount
    @property
    def get_account_number(self):
        return self.__account_number
    @property
    def get_transaction(self):
        return self.__transaction
    @get_transaction.setter
    def add_transaction(self, transaction):
        self.__transaction.append(transaction)
        
    def deposit(self, amount, machine_id):
        if amount <= 0:
            return "error"
        self.__balance += amount
        self.add_transaction=Transaction("D", machine_id, amount, self.__balance)
        return "success"

    def withdraw(self, amount, machine_id):
        if amount <= 0:
            return "error"
        if amount > self.__balance:
            return "error not enough money in your account"
        self.__balance -= amount
        self.add_transaction=Transaction("W", machine_id, amount, self.__balance)
        return "success"

    def transfer(self, destination_account, amount, machine_id):
        if amount <= 0:
            return "error"
        if amount > self.__balance:
            return "error not enough money in your account"
        self.__balance -= amount
        destination_account.update_balance=amount
        self.add_transaction=Transaction("TW", machine_id, amount, self.__balance)
        destination_account.add_transaction=Transaction("TD", machine_id, amount, destination_account.get_balance)
        return "success"


    

    

    

class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin
    @property
    def get_pin(self):
        return self.__pin
    @property
    def get_card_number(self):
        return self.__card_number
    
class ATMMachine:
    dailywithdraw = 40000

    def __init__(self, machine_id: str, initial_amount: float = 1000000):
        self.__machine_id = machine_id
        self.__initial_amount = initial_amount
    def insert_card(self, bank, card, pin):
        if pin != card.get_pin:
            return "Invalid Pin"
        for user in bank.get_user:
            for account in user.get_account:
                if account.get_card == card:
                    return account
        return None

    def deposit(self, account: Account, amount):
        result = account.deposit(amount, self.__machine_id)
        if result == "success":
            self.__initial_amount += amount
        return result

    def withdraw(self, account: Account, amount):
        if amount > self.__initial_amount:
            return "ATM has insufficient funds"
        if amount > self.dailywithdraw:
            return "error excess limit daily withdraw 40k"
        result = account.withdraw(amount, self.__machine_id)
        if result == "success":
            self.__initial_amount -= amount
            self.dailywithdraw -= amount
        return result

    def transfer(self, account: Account, destination_account: Account, amount):
        result = account.transfer(destination_account, amount, self.__machine_id)
        return result
    
    @property
    def get_machine_id(self):
        return self.__machine_id
    @property
    def get_balance(self):
        return self.__initial_amount
    
    
    
class Transaction:
    def __init__(self, Type: str, machine: ATMMachine, Transac_amount: int , After_amount: int):
        self.__Type = Type
        self.__Transac_amount = Transac_amount
        self.__After_amount = After_amount
        self.__machine = machine
    @property
    def get_type(self):
        return self.__Type
    @property
    def get_amount(self):
        return self.__Transac_amount
    @property
    def get_after_amount(self):
        return self.__After_amount
    @property
    def get_machine(self):
        return self.__machine
     
    

class Bank:
    def __init__(self, name:str):
        self.__name = name
        self.__bank_all_user = []
        self.__bank_all_atmmachine = []
    @property
    def get_user(self):
        return self.__bank_all_user
    
    def set_user(self, user):
        self.__bank_all_user = user
        
    def get_atm(self, machine_id):
        for machine in self.__bank_all_atmmachine:
            if machine.get_machine_id == machine_id:
                return machine
        return None
    
    def set_atm_machine(self, atmmachine):
        self.__bank_all_atmmachine = atmmachine
    

    
    
# กำหนดรูปแบบของ user ดังนี้ {รหัสประชาชน : [ชื่อ, หมายเลขบัญชี, จำนวนเงิน, หมายเลข ATM ]}

all_users = []  
all_accounts = []  
all_cards = [] 
all_atm = [] 
def add_data():
    user ={'1-1101-12345-12-0':['Harry Potter','1234567890','12345',20000],
       '1-1101-12345-13-0':['Hermione Jean Granger','0987654321','12346',1000]}
    atm = {'1001':1000000,'1002':200000}
    for machine_id, initial_amount in atm.items():
        atm_instance = ATMMachine(machine_id,initial_amount)
        all_atm.append(atm_instance)
    for citizen_id, data in user.items():
        name, account_number, card_number, balance = data  # แยกข้อมูลออกมา
        
  
        user_instance = User(citizen_id, name)
        all_users.append(user_instance)
        
        account_instance = Account(account_number, user_instance, int(balance))
        all_accounts.append(account_instance)
        
        
        card_instance = ATMCard(card_number, account_instance, '1234')  
        all_cards.append(card_instance)

        user_instance.add_account = account_instance
        account_instance.add_card = card_instance
        user_instance.add_atm_card(atm_instance)
    
    
add_data()

meenmoney = Bank(name = "meenmoney")
meenmoney.set_user(all_users)
meenmoney.set_atm_machine(all_atm)

def test_todolist():
# TODO 1 : จากข้อมูลใน user ให้สร้าง instance โดยมีข้อมูล
# TODO :   key:value โดย key เป็นรหัสบัตรประชาชน และ value เป็นข้อมูลของคนนั้น ประกอบด้วย
# TODO :   [ชื่อ, หมายเลขบัญชี, หมายเลขบัตร ATM, จำนวนเงินในบัญชี]
# TODO :   return เป็น instance ของธนาคาร
# TODO :   และสร้าง instance ของเครื่อง ATM จำนวน 2 เครื่อง

# TODO 2 : เขียน method ที่ทำหน้าที่สอดบัตรเข้าเครื่อง ATM มี parameter 2 ตัว ได้แก่ 1) instance ของธนาคาร
# TODO     2) atm_card เป็นหมายเลขของ atm_card
# TODO     return ถ้าบัตรถูกต้องจะได้ instance ของ account คืนมา ถ้าไม่ถูกต้องได้เป็น None
# TODO     ควรเป็น method ของเครื่อง ATM
    atm_card = all_cards[0]
    atm_machine = meenmoney.get_atm('1001')
    account = atm_machine.insert_card(meenmoney, atm_card, atm_card.get_pin)
    destination_account = all_accounts[1]
    print(account)
    print("")

# TODO 3 : เขียน method ที่ทำหน้าที่ฝากเงิน โดยรับ parameter 3 ตัว คือ 1) instance ของเครื่อง atm
# TODO     2) instance ของ account 3) จำนวนเงิน
# TODO     การทำงาน ให้เพิ่มจำนวนเงินในบัญชี และ สร้าง transaction ลงในบัญชี
# TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
# TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0
    deposit = atm_machine.deposit(account, 500)
    print(deposit)
    print(account.get_balance)
    print("")

# TODO 4 : เขียน method ที่ทำหน้าที่ถอนเงิน โดยรับ parameter 3 ตัว คือ 1) instance ของเครื่อง atm
# TODO     2) instance ของ account 3) จำนวนเงิน
# TODO     การทำงาน ให้ลดจำนวนเงินในบัญชี และ สร้าง transaction ลงในบัญชี
# TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
# TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0 และ ไม่ถอนมากกว่าเงินที่มี
    withdraw = atm_machine.withdraw(account, 1000)
    print(withdraw)
    print(account.get_balance)
    print("")

#TODO 5 : เขียน method ที่ทำหน้าที่โอนเงิน โดยรับ parameter 4 ตัว คือ 1) instance ของเครื่อง atm
# TODO     2) instance ของ account ตนเอง 3) instance ของ account ที่โอนไป 4) จำนวนเงิน
# TODO     การทำงาน ให้ลดจำนวนเงินในบัญชีตนเอง และ เพิ่มเงินในบัญชีคนที่โอนไป และ สร้าง transaction ลงในบัญชี
# TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
# TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0 และ ไม่ถอนมากกว่าเงินที่มี
    transfer = atm_machine.transfer(account, destination_account, 1000)
    print(transfer)
    print(account.get_balance)
    print(destination_account.get_balance)
    print("")

def test_Case():
    machine1 = all_atm[0]
    user_harry = all_users[0]
    harry_atm_card = all_cards[0]
    machine2 = all_atm[1]
    user_hermione = all_users[1]
    hermione_atm_card = all_cards[1]
    
# Test case #1 : ทดสอบ การ insert บัตร โดยค้นหาเครื่อง atm เครื่องที่ 1 และบัตร atm ของ harry
# และเรียกใช้ function หรือ method จากเครื่อง ATM
# ผลที่คาดหวัง : พิมพ์ หมายเลข account ของ harry อย่างถูกต้อง และ พิมพ์หมายเลขบัตร ATM อย่างถูกต้อง
# Ans : 12345, 1234567890, Success
    print("test1")
    acc_harry = machine1.insert_card(meenmoney, harry_atm_card, harry_atm_card.get_pin)
    print("Answer", harry_atm_card.get_card_number, acc_harry.get_account_number)
# Test case #2 : ทดสอบฝากเงินเข้าในบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 1000 บาท
# ให้เรียกใช้ method ที่ทำการฝากเงิน
# ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Hermione ก่อนฝาก หลังฝาก และ แสดง transaction
# Hermione account before test : 1000
# Hermione account after test : 2000
    print("\ntest2")
    acc_hermione = machine2.insert_card(meenmoney, hermione_atm_card, hermione_atm_card.get_pin)
    print("Hermione account before test : ",acc_hermione.get_balance)
    machine2.deposit(acc_hermione, 1000)
    print("Hermione account after test : ",acc_hermione.get_balance)
# Test case #3 : ทดสอบฝากเงินเข้าในบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน -1 บาท
# ผลที่คาดหวัง : แสดง Error
    print("\ntest3")
    print(machine2.deposit(acc_hermione, -1))

# Test case #4 : ทดสอบการถอนเงินจากบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 500 บาท
# ให้เรียกใช้ method ที่ทำการถอนเงิน
# ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Hermione ก่อนถอน หลังถอน และ แสดง transaction
# Hermione account before test : 2000
# Hermione account after test : 1500
    print("\ntest4")
    print("Hermione account before test : ",acc_hermione.get_balance)
    machine2.withdraw(acc_hermione, 500)
    print("Hermione account after test : ",acc_hermione.get_balance)
# Test case #5 : ทดสอบถอนเงินจากบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 2000 บาท
# ผลที่คาดหวัง : แสดง Error
    print("\ntest5")
    print(machine2.withdraw(acc_hermione, 2000))
# Test case #6 : ทดสอบการโอนเงินจากบัญชีของ Harry ไปยัง Hermione จำนวน 10000 บาท ในเครื่อง atm เครื่องที่ 2
# ให้เรียกใช้ method ที่ทำการโอนเงิน
# ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Harry ก่อนถอน หลังถอน และ แสดงจำนวนเงินในบัญชีของ Hermione ก่อนถอน หลังถอน แสดง transaction
# Harry account before test : 20000
# Harry account after test : 10000
# Hermione account before test : 1500
# Hermione account after test : 11500
    print("\ntest6")
    acc_harry = machine2.insert_card(meenmoney, harry_atm_card, harry_atm_card.get_pin)
    print("Harry account before test : ",acc_harry.get_balance)
    print("Hermione account before test : ",acc_hermione.get_balance)
    machine2.transfer(acc_harry, acc_hermione, 10000)
    print("Harry account after test : ",acc_harry.get_balance)
    print("Hermione account after test : ",acc_hermione.get_balance)
# Test case #7 : แสดง transaction ของ Hermione ทั้งหมด 
# ผลที่คาดหวัง
# Hermione transaction : D-ATM:1002-1000-2000
# Hermione transaction : W-ATM:1002-500-1500
# Hermione transaction : TD-ATM:1002-10000-11500
    print("\ntest7")
    all_transaction = acc_hermione.get_transaction
    for Transactions in all_transaction:
        print(f"{Transactions.get_type}-ATM:{Transactions.get_machine}-{Transactions.get_amount}-{int(Transactions.get_after_amount)}")
# Test case #8 : ทดสอบการใส่ PIN ไม่ถูกต้อง 
# ให้เรียกใช้ method ที่ทำการ insert card และตรวจสอบ PIN
# atm_machine = bank.get_atm('1001')
# test_result = atm_machine.insert_card('12345', '9999')  # ใส่ PIN ผิด
# ผลที่คาดหวัง
# Invalid PIN
    print("\ntest8")
    print(machine2.insert_card(meenmoney, harry_atm_card, "9999"))
# Test case #9 : ทดสอบการถอนเงินเกินวงเงินต่อวัน (40,000 บาท)
# atm_machine = bank.get_atm('1001')
# account = atm_machine.insert_card('12345', '1234')  # PIN ถูกต้อง
# harry_balance_before = account.get_balance()
# print(f"Harry account before test: {harry_balance_before}")
# print("Attempting to withdraw 45,000 baht...")
# result = atm_machine.withdraw(account, 45000)
# print(f"Expected result: Exceeds daily withdrawal limit of 40,000 baht")
# print(f"Actual result: {result}")
# print(f"Harry account after test: {account.get_balance()}")
# print("-------------------------")
    print("\ntest9")
    acc_harry = machine2.insert_card(meenmoney, harry_atm_card, "1234")
    print("Harry account before test : ",acc_harry.get_balance)
    print("Attempting to withdraw 45,000 baht...")
    result = machine2.withdraw(acc_harry, 45000)
    print(f"Expected result: Exceeds daily withdrawal limit of 40,000 baht")
    print(f"Actual result: {result}")
    print(f"Harry account after test: {acc_harry.get_balance}")
# Test case #10 : ทดสอบการถอนเงินเมื่อเงินในตู้ ATM ไม่พอ
# atm_machine = bank.get_atm('1002')  # สมมติว่าตู้ที่ 2 มีเงินเหลือ 200,000 บาท
# account = atm_machine.insert_card('12345', '1234')
# print("Test case #10 : Test withdrawal when ATM has insufficient funds")
# print(f"ATM machine balance before: {atm_machine.get_balance()}")
# print("Attempting to withdraw 250,000 baht...")
# result = atm_machine.withdraw(account, 250000)
# print(f"Expected result: ATM has insufficient funds")
# print(f"Actual result: {result}")
# print(f"ATM machine balance after: {atm_machine.get_balance()}")
# print("-------------------------")
    print("\ntest10")
    account = machine2.insert_card(meenmoney, harry_atm_card, "1234")
    print("Test case #10 : Test withdrawal when ATM has insufficient funds")
    print(f"ATM machine balance before: {machine2.get_balance}")
    print("Attempting to withdraw 250,000 baht...")
    result = machine2.withdraw(account, 250000)
    print(f"Expected result: ATM has insufficient funds")
    print(f"Actual result: {result}")
    print(f"ATM machine balance after: {machine2.get_balance}")
test_Case()