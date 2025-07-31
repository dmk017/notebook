from rest_framework.test import APITestCase

from address.models import Address, Country
from department.models import Activity, Department, Position
from employee.models import Employee, EmployeePosition


class WikiiTests(APITestCase):
    def setUp(self):
        # Название поля:
        # self.*названиеМодели*_*названиеТипаДанных*_*информацияПроПоле*
        
        # Country
        self.country_instance_russia = Country.objects.create(name="Russia")
        self.country_instance_france = Country.objects.create(name="Frace")
        self.country_data_good = {"name": "UK"}
        self.country_data_fail = {"name123": "USA"}

        # Address
        self.address_instance_red_square = Address.objects.create(
            street="Красная площадь",
            city="Москва",
            country=self.country_instance_russia,
        )
        self.address_instance_eiffel_tower = Address.objects.create(
            street="12 Avenue Pierre Loti",
            city="Париж",
            country=self.country_instance_france,
        )
        self.address_data_good = {
            "street": "Мичуринский проспект",
            "city": "Москва",
            "country": self.country_instance_russia.pk,
            "description": "Широкий проспект",
            "owner_id": "OWNER_ID",
        }
        self.address_data_fail = {
            "street": "street",
            "city": "city",
            "is_deleted": True,
        }

        # Employee
        self.employee_instance_petrov = Employee.objects.create(
            surname="Petrov",
            name="Arsen",
            location=self.address_instance_red_square,
            owner_id="OWNER_ID"
        )
        self.employee_instance_ivanov = Employee.objects.create(
            surname="Ivanov",
            name="Ivan",
            lastname="Ivanovich",
            place_of_birth=self.address_instance_eiffel_tower,
            location=self.address_instance_eiffel_tower,
            owner_id="OWNER_ID"
        )
        self.employee_data_good = {
            "surname": "Alexeev",
            "name": "Alexey",
            "lastname": "Alexeevich",
            "place_of_birth": self.address_instance_eiffel_tower.pk,
            "location": self.address_instance_red_square.pk,
            "owner_id": "OWNER_ID"
        }
        self.employee_data_fail = {
            "name": "without required data"
        }

        # Activity
        self.activity_instance_education = Activity.objects.create(
            name="Образование",
            description="Обучение в какой-либо сфере",
            owner_id="OWNER_ID",
        )
        self.activity_instance_industry = Activity.objects.create(
            name="Тяжелая промышленность",
            description="Отрасль промышленности, которая специализируется на производстве крупных и сложных продуктов, таких как сталь, цемент, энергетическое оборудование и машины",
            owner_id="OWNER_ID"
        )
        self.activity_data_good = {
            "name": "new_activity_name",
            "description": "new_description",
            "owner_id": "OWNER_ID",
        }
        self.activity_data_fail = {
            "name_fail": "activity_name_fail",
            "description": "description",
            "owner_id": "OWNER_ID",
        }

        # Department
        self.department_instance_administration_of_study_center = Department.objects.create(
            name="Центр подготовки к ЕГЭ",
            description="Онлайн центр подготовки к сдаче экзаменов. Обязуется подготовить ребенка к сдаче экзамена на высокий балл.",
            activity_id=self.activity_instance_education,
            owner_type="PV",
            address=self.address_instance_red_square,
            owner_id="OWNER_ID",
        )
        self.department_instance_finance_division_of_study_center = Department.objects.create(
            name="Финансово-плановый отдел",
            description="Обычный финансово-планоый отдел.",
            activity_id=self.activity_instance_education,
            parent_id=self.department_instance_administration_of_study_center,
            owner_type="PV",
            address=self.address_instance_red_square,
            owner_id="OWNER_ID",
        )
        self.department_instance_education_division_of_study_center = Department.objects.create(
            name="Учебный отдел",
            description="Состоит из преподавателей, ведущих занятия.",
            activity_id=self.activity_instance_education,
            parent_id=self.department_instance_administration_of_study_center,
            owner_type="PV",
            address=self.address_instance_red_square,
            owner_id="OWNER_ID",
        )

        self.department_data_good_managment_of_military_factory = {
            "name": "Завод по производству военной техники",
            "activity_id": self.activity_instance_industry.pk,
            "owner_type": "GV",
            "address": self.address_instance_eiffel_tower.pk,
            "owner_id": "OWNER_ID",
        }
        self.department_data_good_human_resources_division = {
            "name": "Отдел кадров",
            "activity_id": self.activity_instance_industry.pk,
            "owner_type": "GV",
            "address": self.address_instance_eiffel_tower.pk,
            "owner_id": "OWNER_ID",
        }
        self.department_data_good_development_division = {
            "name": "Отдел разработок",
            "activity_id": self.activity_instance_industry.pk,
            "owner_type": "GV",
            "address": self.address_instance_eiffel_tower.pk,
            "owner_id": "OWNER_ID",
        }
        self.department_data_fail_dictionary_with_diff_types_of_errors = {
            "missing_required_fields": {
                "name": "Отдел.",
                "owner_type": "GV",
                "address": self.address_instance_eiffel_tower.pk,
                "owner_id": "OWNER_ID",
            },
            "non_existing_parent": {
                "name": "Отдел.",
                "parent_id": 404,
                "activity_id": self.activity_instance_industry.pk,
                "owner_type": "GV",
                "address": self.address_instance_eiffel_tower.pk,
                "owner_id": "OWNER_ID",
            },
            "non_existing_owner_type": {
                "name": "Отдел.",
                "activity_id": self.activity_instance_industry.pk,
                "owner_type": "IM NOT EXIST!!!",
                "address": self.address_instance_eiffel_tower.pk,
                "owner_id": "OWNER_ID",
            },
            "trying_to_set_id": {
                "id": 100000,
                "name": "Отдел.",
                "activity_id": self.activity_instance_industry.pk,
                "owner_type": "GV",
                "address": self.address_instance_eiffel_tower,
                "owner_id": "OWNER_ID",
            },
        }

        # Position
        self.position_instance_master_of_study_center = Position.objects.create(
            department_id=self.department_instance_administration_of_study_center,
            name="Предприниматель",
            description="Владелец бизнеса по обучению в онлайн-школе.",
            owner_id="OWNER_ID",
        )
        self.position_instance_manager_of_study_center = Position.objects.create(
            department_id=self.department_instance_administration_of_study_center,
            name="Управляющий",
            description="Осуществляет управление обучением. Нанимает преподавателей.",
            owner_id="OWNER_ID",
        )
        self.position_instance_bio_teacher_of_study_center = Position.objects.create(
            department_id=self.department_instance_education_division_of_study_center,
            name="Преподаватель биологии",
            description="Обучает студентов.",
            owner_id="OWNER_ID",
        )
        self.position_instance_math_teacher_of_study_center = Position.objects.create(
            department_id=self.department_instance_education_division_of_study_center,
            name="Преподаватель математики",
            description="Обучает студентов.",
            owner_id="OWNER_ID",
        )

        self.position_data_good = {
            "department_id": self.department_instance_education_division_of_study_center.pk,
            "name": "Преподаватель иностранного языка",
            "description": "Обучает студентов.",
            "owner_id": "OWNER_ID",
        }
        self.position_data_fail = {
            "department_id": self.department_instance_education_division_of_study_center.pk,
            "description": "",
        }

        # EmployeePosition
        self.employeeposition_instance_petrov_math_teacher = EmployeePosition.objects.create(
            employee_id=self.employee_instance_petrov,
            position_id=self.position_instance_math_teacher_of_study_center,
            owner_id="OWNER_ID"
        )
        self.employeeposition_instance_petrov_manager = EmployeePosition.objects.create(
            employee_id=self.employee_instance_petrov,
            position_id=self.position_instance_manager_of_study_center,
            owner_id="OWNER_ID"
        )
        self.employeeposition_instance_ivanov_master = EmployeePosition.objects.create(
            employee_id=self.employee_instance_ivanov,
            position_id=self.position_instance_master_of_study_center,
            owner_id="OWNER_ID"
        )

        self.employeeposition_data_good = {
            "position_id": self.position_instance_bio_teacher_of_study_center.pk,
            "owner_id": "OWNER_ID",
        }
        self.employeeposition_data_fail_wout_position_id = {
            "owner_id": "OWNER_ID",
        }
        self.employeeposition_data_fail_non_existing_position_id = {
            "position_id": 9999
        }
        self.employeeposition_data_fail_wout_owner_id = {
            "position_id": self.position_instance_bio_teacher_of_study_center.pk,
        }
        self.employeeposition_data_good_with_finish_date = {
            "finish_date": "2024-01-30",
            "owner_id": "OWNER_ID"
        }