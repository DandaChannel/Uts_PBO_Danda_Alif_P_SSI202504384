import json
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    @abstractmethod
    def get_report(self): pass

class Bonus(ABC):
    @abstractmethod
    def hitung(self, gaji): pass
class Perf2026(Bonus):
    def hitung(self, g): return g * 0.25
class Senior10(Bonus):
    def hitung(self, g): return g * 0.10
class Lead2026(Bonus):
    def hitung(self, g): return g * 0.30
class NoBonus(Bonus):
    def hitung(self, g): return 0

class Employee(BaseProcessor):
    def __init__(self, d):
        self.emp_id = d['emp_id']; self.name = d['name']; self.base_salary = d['base_salary']; self.bonus_code = d['bonus_code']
        if self.bonus_code == 'PERF2026': self.bonus = Perf2026()
        elif self.bonus_code == 'SENIOR10': self.bonus = Senior10()
        elif self.bonus_code == 'LEAD2026': self.bonus = Lead2026()
        else: self.bonus = NoBonus()
    def hitung_gaji(self): return self.base_salary + self.bonus.hitung(self.base_salary)
    def get_report(self): return self.emp_id

class PermanentEmployee(Employee):
    def hitung_gaji(self): return self.base_salary + (self.base_salary * 0.20) + self.bonus.hitung(self.base_salary)
    def get_report(self): return f"[TETAP] {self.emp_id} - {self.name} | {self.bonus_code} | TOTAL Rp {self.hitung_gaji():,.0f}"
class ContractEmployee(Employee):
    def get_report(self): return f"[KONTRAK] {self.emp_id} - {self.name} | TOTAL Rp {self.hitung_gaji():,.0f}"

class Sensor(BaseProcessor):
    def __init__(self, d): self.__dict__.update(d)
class DangerSensor(Sensor):
    def get_report(self):
        op = self.operator_id if self.operator_id else "TIDAK ADA OPERATOR! AUTO SHUTDOWN"
        return f"!!! DANGER !!! {self.sensor_id} {self.location} {self.temperature}C Operator:{op}"
class WarningSensor(Sensor):
    def get_report(self): return f"[WARNING] {self.sensor_id} {self.location} {self.temperature}C"
class NormalSensor(Sensor):
    def get_report(self): return f"[NORMAL] {self.sensor_id} {self.location} {self.temperature}C Aman"

print("=== LAPORAN KARYAWAN ===")
with open('Employee.json') as f:
    for e in json.load(f)['employees']:
        obj = PermanentEmployee(e) if e['is_permanent'] else ContractEmployee(e)
        print(obj.get_report())

print("\n=== LAPORAN SENSOR ===")
with open('sensor_logs.json') as f:
    for s in json.load(f)['readings']:
        if s['status']=='DANGER': obj = DangerSensor(s)
        elif s['status']=='WARNING': obj = WarningSensor(s)
        else: obj = NormalSensor(s)
        print(obj.get_report())