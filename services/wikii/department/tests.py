from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .models import Activity, Department, Position
from wikii.tests import WikiiTests
from address.models import Address, Country


class ActivityTests(WikiiTests):
    def setUp(self):
        super(self.__class__, self).setUp()

    def test_get_activity_detail_when_get_by_existing_id_then_returns_it(self):
        existing_id = self.activity_instance_education.pk
        response = self.client.get(
            reverse("activity_by_id", kwargs={"id": existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["name"],
                response.data["data"]["description"],
                response.data["data"]["owner_id"],
            },
            {
                self.activity_instance_education.name,
                self.activity_instance_education.description,
                self.activity_instance_education.owner_id,
            },
        )

    def test_get_activity_detail_when_get_by_non_existing_id_then_returns_404(self):
        non_existing_id = 9999
        response = self.client.get(
            reverse("activity_by_id", kwargs={"id": non_existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Activity was not found."},
        )

    def test_get_activities_list_when_get_wout_name_filter_then_returns_two_items(self):
        response = self.client.get(reverse("activities"))

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 2)

    def test_get_activities_list_when_get_by_esisting_name_filter_then_returns_it(self):
        response = self.client.get(reverse("activities"), data={"name": "Образование"})

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            response.data["data"][0]["id"], self.activity_instance_education.pk
        )

    def test_create_activity_when_get_right_data_then_returns_201(self):
        response_before_creating_new_instance = self.client.get(reverse("activities"))
        response_for_creating_new_instance = self.client.post(
            reverse("activities"), data=self.activity_data_good
        )
        response_after_creating_new_instance = self.client.get(reverse("activities"))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"OK", "201 CREATED"},
        )
        self.assertEqual(
            1 + len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )
        self.assertEqual(
            {
                response_after_creating_new_instance.data["data"][-1]["name"],
                response_after_creating_new_instance.data["data"][-1]["description"],
                response_after_creating_new_instance.data["data"][-1]["owner_id"],
            },
            {
                self.activity_data_good["name"],
                self.activity_data_good["description"],
                self.activity_data_good["owner_id"],
            },
        )

    def test_create_activity_when_get_fail_data_then_returns_400(self):
        response_before_creating_new_instance = self.client.get(reverse("activities"))
        response_for_creating_new_instance = self.client.post(
            reverse("activities"), data=self.activity_data_fail
        )
        response_after_creating_new_instance = self.client.get(reverse("activities"))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )
        self.assertEqual(
            len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )

    def test_change_activity_when_get_right_data_and_existing_instance_then_returns_200(
        self,
    ):
        existing_id = self.activity_instance_education.pk
        response = self.client.put(
            reverse("activity_by_id", kwargs={"id": existing_id}),
            data=self.activity_data_good,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["name"],
                response.data["data"]["description"],
                response.data["data"]["owner_id"],
            },
            {
                self.activity_data_good["name"],
                self.activity_data_good["description"],
                self.activity_data_good["owner_id"],
            },
        )

    def test_change_activity_when_get_right_data_and_non_existing_instance_then_returns_404(
        self,
    ):
        non_existing_id = 9999
        response = self.client.put(
            reverse("activity_by_id", kwargs={"id": non_existing_id}),
            data=self.activity_data_good,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Activity was not found."},
        )

    def test_change_activity_when_get_fail_data_and_existing_instance_then_returns_400(
        self,
    ):
        existing_id = self.activity_instance_education.pk
        response = self.client.put(
            reverse("activity_by_id", kwargs={"id": existing_id}),
            data=self.activity_data_fail,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )

    def test_delete_activity_when_get_existing_instance_then_it_deleting_and_returns_204(
        self,
    ):
        existing_id = self.activity_instance_education.pk
        response = self.client.delete(
            reverse("activity_by_id", kwargs={"id": existing_id})
        )
        response_after_deleting = self.client.get(
            reverse("activity_by_id", kwargs={"id": existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "204 NO DATA"},
        )
        self.assertEqual(
            {
                response_after_deleting.data["status"],
                response_after_deleting.data["message"],
            },
            {"ERROR", "404 Not Found. The specified Activity was not found."},
        )

    def test_delete_activity_when_get_non_existing_instance_then_returns_404(self):
        non_existing_primary_key = 9999
        response = self.client.delete(
            reverse("activity_by_id", kwargs={"id": non_existing_primary_key})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Activity was not found."},
        )


class DepartmentTests(WikiiTests):
    def setUp(self):
        super(self.__class__, self).setUp()

    def test_get_department_detail_when_get_by_existing_id_then_returns_it(self):
        existing_id = self.department_instance_administration_of_study_center.pk
        response = self.client.get(
            reverse("department_by_id", kwargs={"id": existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["name"],
                response.data["data"]["description"],
                response.data["data"]["activity_id"],
                response.data["data"]["owner_type"],
                response.data["data"]["address"],
                response.data["data"]["owner_id"],
            },
            {
                self.department_instance_administration_of_study_center.name,
                self.department_instance_administration_of_study_center.description,
                self.department_instance_administration_of_study_center.activity_id.pk,
                self.department_instance_administration_of_study_center.owner_type,
                self.department_instance_administration_of_study_center.address.pk,
                self.department_instance_administration_of_study_center.owner_id,
            },
        )
    
    def test_get_department_detail_when_get_by_non_existing_id_then_returns_404(self):
        non_existing_id = 9999
        response = self.client.get(
            reverse("department_by_id", kwargs={"id": non_existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Department was not found."},
        )

    def test_get_departments_list_when_get_wout_name_filter_then_returns_three_items(self):
        response = self.client.get(reverse("departments"))

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 3)

    def test_get_departments_list_when_get_by_existing_name_filter_then_returns_it(
        self,
    ):
        response = self.client.get(
            reverse("departments"), data={"name": "Центр подготовки к ЕГЭ"}
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            response.data["data"][0]["id"], self.address_instance_red_square.pk
        )

    def test_get_departments_list_when_get_by_existing_parent_id_filter_then_returns_it(
        self,
    ):
        response = self.client.get(reverse("departments"), data={"parent_id": 1})
        
        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 2)

    def test_get_departments_list_when_get_by_non_existing_name_filter_then_returns_empty_list(
        self,
    ):
        non_existing_name = "Несуществующее название подразделения"
        response = self.client.get(
            reverse("departments"), data={"name": non_existing_name}
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 0)

    def test_get_departments_list_when_get_by_non_existing_parent_id_filter_then_returns_empty_list(
        self,
    ):
        non_existing_parent_id = 9999
        response = self.client.get(
            reverse("departments"), data={"parent_id": non_existing_parent_id}
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 0)

    def test_create_department_when_get_right_data_then_returns_201(self):
        response_before_creating_new_instance = self.client.get(reverse("departments"))
        response_for_creating_new_instance = self.client.post(
            reverse("departments"), data=self.department_data_good_managment_of_military_factory
        )
        response_after_creating_new_instance = self.client.get(reverse("departments"))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"OK", "201 CREATED"},
        )
        self.assertEqual(
            1 + len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )
        self.assertEqual(
            {
                response_for_creating_new_instance.data["data"]["name"],
                response_for_creating_new_instance.data["data"]["activity_id"],
                response_for_creating_new_instance.data["data"]["owner_type"],
                response_for_creating_new_instance.data["data"]["address"],
                response_for_creating_new_instance.data["data"]["owner_id"],
            },
            {
                self.department_data_good_managment_of_military_factory["name"],
                self.department_data_good_managment_of_military_factory["activity_id"],
                self.department_data_good_managment_of_military_factory["owner_type"],
                self.department_data_good_managment_of_military_factory["address"],
                self.department_data_good_managment_of_military_factory["owner_id"],
            },
        )
    
    def test_create_department_when_created_instance_of_master_department_and_instance_of_slave_department_then_slave_obeys_to_master(self):
        response_for_creating_master_instance = self.client.post(
            reverse("departments"), data=self.department_data_good_managment_of_military_factory
        )
        response_for_recieving_masters_id = self.client.get(
            reverse("departments"), data={"name": self.department_data_good_managment_of_military_factory['name']}
        )
        masters_id = response_for_recieving_masters_id.data["data"][0]["id"]

        self.department_data_good_human_resources_division["parent_id"] = masters_id
        self.department_data_good_development_division["parent_id"] = masters_id

        response_for_creating_first_slave_instance = self.client.post(
            reverse("departments"), data=self.department_data_good_human_resources_division
        )
        response_for_creating_second_slave_instance = self.client.post(
            reverse("departments"), data=self.department_data_good_development_division
        )
        
        response_for_revieving_slaves = self.client.get(
            reverse("departments"), data={"parent_id": masters_id}
        )

        self.assertEqual(
            len(response_for_revieving_slaves.data['data']), 2
        )

    def test_create_department_when_get_fail_data_then_returns_400(self):
        for error_type in self.department_data_fail_dictionary_with_diff_types_of_errors:
            response_before_creating_new_instance = self.client.get(reverse("departments"))
            response_for_creating_new_instance = self.client.post(
                reverse("departments"), data=self.department_data_fail_dictionary_with_diff_types_of_errors[error_type]
            )
            response_after_creating_new_instance = self.client.get(reverse("departments"))

            self.assertEqual(
                {
                    response_for_creating_new_instance.data["status"],
                    response_for_creating_new_instance.data["message"],
                },
                {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
            )
            self.assertEqual(
                len(response_before_creating_new_instance.data["data"]),
                len(response_after_creating_new_instance.data["data"]),
            )

    def test_change_department_when_get_right_data_and_existing_instance_then_returns_200(
        self,
    ):
        existing_id = self.department_instance_administration_of_study_center.pk
        right_data = self.department_data_good_managment_of_military_factory
        response = self.client.put(
            reverse("department_by_id", kwargs={"id": existing_id}),
            data=right_data,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["name"],
                response.data["data"]["activity_id"],
                response.data["data"]["owner_type"],
                response.data["data"]["address"],
                response.data["data"]["owner_id"],
            },
            {
                self.department_data_good_managment_of_military_factory["name"],
                self.department_data_good_managment_of_military_factory["activity_id"],
                self.department_data_good_managment_of_military_factory["owner_type"],
                self.department_data_good_managment_of_military_factory["address"],
                self.department_data_good_managment_of_military_factory["owner_id"],
            },
        )

    def test_change_department_when_get_right_data_and_non_existing_instance_then_returns_404(
        self,
    ):
        non_existing_id = 9999
        right_data = self.department_data_good_managment_of_military_factory
        response = self.client.put(
            reverse("department_by_id", kwargs={"id": non_existing_id}),
            data=right_data,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Department was not found."},
        )

    def test_change_department_when_get_fail_data_and_existing_instance_then_returns_400(
        self,
    ):
        existing_id = self.address_instance_red_square.pk
        fail_data = self.department_data_fail_dictionary_with_diff_types_of_errors['non_existing_parent']
        response = self.client.put(
            reverse("department_by_id", kwargs={"id": existing_id}),
            data=fail_data,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )

    def test_delete_department_when_get_existing_instance_then_it_deleting_and_returns_204(
        self,
    ):
        existing_id = self.department_instance_administration_of_study_center.pk
        response = self.client.delete(
            reverse("department_by_id", kwargs={"id": existing_id})
        )
        response_after_deleting = self.client.get(
            reverse("department_by_id", kwargs={"id": existing_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "204 NO DATA"},
        )
        self.assertEqual(
            {response_after_deleting.data["status"], response_after_deleting.data["message"]},
            {"ERROR", "404 Not Found. The specified Department was not found."},
        )

    def test_delete_department_when_get_non_existing_instance_then_returns_404(self):
        non_existing_primary_key = 9999
        response = self.client.delete(
            reverse("department_by_id", kwargs={"id": non_existing_primary_key})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Department was not found."},
        )


class PositionTests(WikiiTests):
    def setUp(self):
        super(self.__class__, self).setUp()

    def test_get_position_detail_when_get_by_existing_position_and_department_id_then_returns_it(self):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        existing_position_id = self.position_instance_master_of_study_center.pk
        response = self.client.get(
            reverse("position_by_id", kwargs={"department_id": existing_department_id, "id": existing_position_id})
        )
        
        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["department_id"],
                response.data["data"]["name"],
                response.data["data"]["description"],
                response.data["data"]["owner_id"],
            },
            {
                self.position_instance_master_of_study_center.department_id.pk,
                self.position_instance_master_of_study_center.name,
                self.position_instance_master_of_study_center.description,
                self.position_instance_master_of_study_center.owner_id,
            },
        )

    def test_get_position_detail_when_get_by_non_existing_position_id_and_existing_department_id_then_returns_404(self):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        non_existing_position_id = 9999
        response = self.client.get(
            reverse("position_by_id", kwargs={"department_id": existing_department_id, "id": non_existing_position_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Position was not found."},
        )

    def test_get_position_detail_when_get_by_non_existing_department_id_and_existing_position_id_then_returns_400(self):
        non_existing_department_id = 9999
        existing_position_id = self.position_instance_master_of_study_center.pk
        response = self.client.get(
            reverse("position_by_id", kwargs={"department_id": non_existing_department_id, "id": existing_position_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "400 Bad Request. Invalid input department field."},
        )
    
    def test_get_positions_list_when_get_wout_name_filter_then_returns_three_items(self):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        response = self.client.get(reverse("positions", kwargs={"department_id": existing_department_id}))

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(len(response.data["data"]), 3)

    def test_get_positions_list_when_get_by_existing_name_filter_then_returns_it(self):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        existing_name_filter = self.position_instance_master_of_study_center.name
        response = self.client.get(
            reverse("positions", kwargs={"department_id": existing_department_id}),
            data={"name": existing_name_filter}
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            response.data["data"][0]["id"], self.position_instance_master_of_study_center.pk
        )

    def test_get_positions_list_when_get_by_non_existing_name_filter_then_returns_it(self):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        non_existing_name_filter = "Non-existing-name"
        response = self.client.get(
            reverse("positions", kwargs={"department_id": existing_department_id}),
            data={"name": non_existing_name_filter}
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            len(response.data["data"]), 0
        )

    def test_create_position_when_get_right_data_then_returns_201(self):
        existing_department_id = self.department_instance_education_division_of_study_center.pk
        response_before_creating_new_instance = self.client.get(reverse("positions", kwargs={"department_id": existing_department_id}))
        response_for_creating_new_instance = self.client.post(
            reverse("positions", kwargs={"department_id": existing_department_id}), data=self.position_data_good
        )
        response_after_creating_new_instance = self.client.get(reverse("positions", kwargs={"department_id": existing_department_id}))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"OK", "201 CREATED"},
        )
        self.assertEqual(
            1 + len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )
    
    def test_create_position_when_get_fail_data_then_returns_400(self):
        existing_department_id = self.department_instance_education_division_of_study_center.pk
        response_before_creating_new_instance = self.client.get(reverse("positions", kwargs={"department_id": existing_department_id}))
        response_for_creating_new_instance = self.client.post(
            reverse("positions", kwargs={"department_id": existing_department_id}), data=self.position_data_fail
        )
        response_after_creating_new_instance = self.client.get(reverse("positions", kwargs={"department_id": existing_department_id}))

        self.assertEqual(
            {
                response_for_creating_new_instance.data["status"],
                response_for_creating_new_instance.data["message"],
            },
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )
        self.assertEqual(
            len(response_before_creating_new_instance.data["data"]),
            len(response_after_creating_new_instance.data["data"]),
        )

    def test_change_position_when_get_right_data_and_existing_instance_then_returns_200(
        self,
    ):
        existing_department_id = self.department_instance_education_division_of_study_center.pk
        existing_position_id = self.position_instance_bio_teacher_of_study_center.pk
        response = self.client.put(
            reverse("position_by_id", kwargs={"department_id": existing_department_id, "id": existing_position_id}),
            data=self.position_data_good,
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "200 OK"},
        )
        self.assertEqual(
            {
                response.data["data"]["name"],
                response.data["data"]["description"],
                response.data["data"]["owner_id"],
            },
            {
                self.position_data_good["name"],
                self.position_data_good["description"],
                self.position_data_good["owner_id"],
            },
        )

    def test_change_position_when_get_right_data_and_non_existing_department_and_existing_position_id_then_returns_400(
        self,
    ):
        non_existing_department_id = 9999
        existing_position_id = self.position_instance_master_of_study_center.pk
        response = self.client.put(
            reverse("position_by_id", kwargs={"department_id": non_existing_department_id, "id": existing_position_id}),
            data=self.position_data_good
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "400 Bad Request. Invalid input department field."},
        )

    def test_change_position_when_get_right_data_and_non_existing_position_and_existing_department_id_then_returns_404(self):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        non_existing_position_id = 9999
        response = self.client.put(
            reverse("position_by_id", kwargs={"department_id": existing_department_id, "id": non_existing_position_id}),
            data=self.position_data_good
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Position was not found."},
        )
    
    def test_change_position_when_get_fail_data_and_existing_position_and_department_id_then_returns_400(self):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        existing_position_id = self.position_instance_master_of_study_center.pk
        response = self.client.put(
            reverse("position_by_id", kwargs={"department_id": existing_department_id, "id": existing_position_id}),
            data=self.position_data_fail
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "400 Bad Request. Invalid input or missing required fields."},
        )

    def test_delete_position_when_get_existing_department_and_position_id_then_it_deleting_and_returns_204(
        self,
    ):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        existing_position_id = self.position_instance_master_of_study_center.pk
        response = self.client.delete(
            reverse("position_by_id", kwargs={"department_id": existing_department_id, "id": existing_position_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"OK", "204 NO DATA"},
        )

    def test_delete_position_when_get_non_existing_department_and_existing_position_id_then_returns_400(self):
        non_existing_department_id = 9999
        existing_position_id = self.position_instance_master_of_study_center.pk
        response = self.client.delete(
            reverse("position_by_id", kwargs={"department_id": non_existing_department_id, "id": existing_position_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "400 Bad Request. Invalid input department field."},
        )

    def test_delete_position_when_get_non_existing_position_and_existing_department_id_then_returns_404(self):
        existing_department_id = self.position_instance_master_of_study_center.department_id.pk
        non_existing_position_id = 9999
        response = self.client.delete(
            reverse("position_by_id", kwargs={"department_id": existing_department_id, "id": non_existing_position_id})
        )

        self.assertEqual(
            {response.data["status"], response.data["message"]},
            {"ERROR", "404 Not Found. The specified Position was not found."},
        )
